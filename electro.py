import time, serial, multiprocessing, os, sys

from threading import Lock
from datetime import datetime
from gpiozero import Motor, Button, LED
from VL53L0X import VL53L0X, Vl53l0xAccuracyMode

def log(value):
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    print(now, value, flush=True)

MOTOR_LEFT_PIN = "BOARD32"
MOTOR_RIGHT_PIN = "BOARD33"

BUTTON1_LANG = "BOARD24"
BUTTON2_LANG = "BOARD26"
BUTTON_RESET = "BOARD23"

LED1 = "BOARD19"
LED2 = "BOARD21"


# UP_LIMIT 200
# DOWN_LIMIT 490
levels = {
    1: 262,
    2: 307,
    3: 358,
    4: 414,
    5: 465
}

def getLevel(dist):
    for l in levels:
        if dist <= levels[l]:
            if l == 1:
                return 1
            return l if dist > (levels[l] + levels[l-1]) / 2 else l - 1 
    return list(levels)[-1]

def startVL53():
    log("Start VL53")
    vl53 = VL53L0X(i2c_bus=1, i2c_address=0x29)
    vl53.open()
    vl53.start_ranging(Vl53l0xAccuracyMode.BETTER)
    timing = vl53.get_timing()
    if timing < 20000:
        timing = 20000
    timing = timing / 1_000_000.0
    time.sleep(timing)
    log("Start VL53 - DONE")
    return vl53, timing

def stopVL53(vl53: VL53L0X):
    try:
        log("Stop VL53")
        vl53.stop_ranging()
        vl53.close()
        del(vl53)
        log("Stop VL53 - DONE")
    except Exception as e:
        log(f"ERROR - VL53_Start: {str(e)}")

def getDistance(vl53: VL53L0X):
    distance = vl53.get_distance()
    if distance <= 0:
        log("VL53 distance error")
    return distance

class Controller:

    def __init__(self, port):
        self.w_lock = Lock()
        self.r_lock = Lock()
        self.port = port
        self.new_serial()
        
    def __del__(self):
        self.com.close()
        del(self.com)
        
    def new_serial(self):
        try:
            del(self.com)
        except:
            pass
        self.com = serial.Serial()
        self.com.port = self.port
        log(f"Controller - Create new serial. Port: {self.port}")

    def init(self):
        if not self.com.is_open:
            self.com.open()
            time.sleep(0.5)

    def reset_input(self):
        self.init()
        try:
            self.com.reset_input_buffer()
        except:
            self.new_serial()

    def reset_output(self):
        self.init()
        try:
            self.com.reset_output_buffer()
        except:
            self.new_serial()

    def readMsg(self, reset = True) -> str:
        with self.r_lock:
            try:
                self.init()
                if reset: 
                    self.reset_input()
                while True:
                    for c in self.com.read():
                        if chr(c) == '$':
                            comand = self.com.read_until(expected = b';')
                            return comand[:-1].decode('UTF-8')
            except Exception as e:
                log(f"ERROR - Controller - Read msg error: {e}")
                return None

    def writeMsg(self, msg: str):
        with self.w_lock:
            try:
                msg = msg.replace('\n', '#')
                self.reset_output()
                self.com.write(str.encode(f"${msg};"))
                self.com.flush()
            except Exception as e:
                log(f"ERROR - Controller - Write msg error: {e}")


class Electro:
    def __init__(self):
        log("Electro - Initialize")
        self.langB1 = Button(pin=BUTTON1_LANG, bounce_time=0.1)
        self.langB2 = Button(pin=BUTTON2_LANG, bounce_time=0.1)
        self.led1 = LED(LED1)
        self.led2 = LED(LED2)

        self.motor = Motor(forward=MOTOR_LEFT_PIN, backward=MOTOR_RIGHT_PIN, pwm=False)

        self.controller1 = Controller("/dev/ttyUSB0")
        self.controller2 = Controller("/dev/ttyUSB1")

        self.rebootB = Button(pin=BUTTON_RESET, bounce_time=0.1)
        self.rebootB.when_pressed = self.reboot
        log("Electro - Initialize - DONE")

    def reboot(self, silent = False):
        log(f"Electro - REBOOT. Silent: {silent}")
        if not silent:
            self.controller1.writeMsg(" -= NEW GAME =- #Loading...")
            self.controller2.writeMsg(" -= NEW GAME =- #Loading...")
        self.motor.stop()
        os.system("sh /home/pi/game/reboot.sh &")
        time.sleep(10)
        
    def change_level(self, level):
        if not level in list(levels):
            log(f"Electro - Level: {level} not in {list(levels)}")
            return 
        vl53, delay = startVL53()
        try:
            p = multiprocessing.Process(target=self._change_level, args=(level, vl53, delay,)) 
            log("Electro - Change level")
            p.start()
            p.join(11)
            if p.is_alive():
                self.motor.stop()
                log(f"I kill changeLevel to {level} after 11 seconds")
                p.terminate()
                p.join()
            else:
                log("Electro - Change level - DONE")
        finally:
            self.motor.stop()
            stopVL53(vl53)

    def _change_level(self, level, vl53, delay):
        curLevel = getLevel(getDistance(vl53))
        if curLevel == level:
            return
        time.sleep(delay)
        dest_dist = levels[level]
        if curLevel > level:
            self.motor.backward()
            while getDistance(vl53) > dest_dist:
                time.sleep(delay)
        else:
            self.motor.forward()
            while getDistance(vl53) < dest_dist:
                time.sleep(delay)
        self.motor.stop()


ELECTRO = Electro()

ver = 'b1.3'
if __name__ == "__main__":
    if len(sys.argv) == 3:
        if sys.argv[1] == "cl":
            lvl = sys.argv[2]
            log(f"Electro (CTL) - Change level to {lvl}")
            ELECTRO.change_level(int(lvl))
            log(f"Electro (CTL) - Change level to {lvl} - DONE")
        elif sys.argv[1] == "p1":
            text = sys.argv[2]
            log(f"Electro (CTL) - Player1 - Print text: '{text}'")
            for _ in range(3):
                ELECTRO.controller1.writeMsg(text)
            log(f"Electro (CTL) - Player1 - Print text - DONE")
        elif sys.argv[1] == "p2":
            text = sys.argv[2]
            log(f"Electro (CTL) - Player2 - Print text: '{text}'")
            for _ in range(3):
                ELECTRO.controller2.writeMsg(text)
            log(f"Electro (CTL) - Player2 - Print text - DONE")
    elif len(sys.argv) == 2:
        if sys.argv[1] == "gd":
            try:
                vl, _ = startVL53()
                log(f"Electro (CTL) - Current distance {vl.get_distance()}")
            finally:
                stopVL53(vl)
    else:
        log(f"Electro (CTL version: {ver}) - Commands: cl <lvl>, gd, p1 <msg>, p2 <msg>")
            