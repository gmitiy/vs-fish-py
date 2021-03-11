from gpiozero import Motor, Button
from VL53L0X import VL53L0X, Vl53l0xAccuracyMode
import time, serial, multiprocessing

MOTOR_LEFT_PIN = "BOARD32"
MOTOR_RIGHT_PIN = "BOARD33"

BUTTON1_LANG = ""
BUTTON2_LANG = ""
BUTTON1_START = ""
BUTTON2_START = ""


# UP_LIMIT 200
# DOWN_LIMIT 500
levels = {
    1: 200,
    2: 275,
    3: 350,
    4: 425,
    5: 500
}

def getLevel(dist):
    for l in levels:
        if dist <= levels[l]:
            if l == 1:
                return 1
            return l if dist > (levels[l] + levels[l-1]) / 2 else l - 1 
    return list(levels)[-1]

def startVL53():
    vl53 = VL53L0X(i2c_bus=1, i2c_address=0x29)
    vl53.open()
    vl53.start_ranging(Vl53l0xAccuracyMode.BETTER)
    timing = vl53.get_timing()
    if timing < 20000:
        timing = 20000
    timing = timing / 1_000_000.0
    time.sleep(timing)
    return vl53, timing


def stopVL53(vl53: VL53L0X):
    try:
        vl53.stop_ranging()
        vl53.close()
        del(vl53)
    except:
        pass


class Controller:
    def __init__(self, port):
        self.com = serial.Serial()
        self.com.port = port

    def __del__(self):
        self.com.close()
        del(self.com)
        
    def init(self):
        if not self.com.is_open:
            self.com.open()

    def sendText(self, text: str) -> bool:
        for _ in range(3):
            self.reset_input()
            self.writeMsg(text)
            if self.readMsg(reset = False) == "@OK":
                return True
        return False

    def readMsg(self, reset = True) -> str:
        try:
            self.init()
            if reset: 
                self.com.reset_input_buffer()
            while True:
                for c in self.com.read():
                    if chr(c) == '$':
                        comand = self.com.read_until(expected = b';')
                        return comand[:-1].decode('UTF-8')
        except Exception as e:
            print(e)
            return None

    def reset_input(self):
        self.init()
        self.com.reset_input_buffer()

    def writeMsg(self, msg: str):
        try:
            self.init()
            msg = msg.replace('\n', '#')
            self.com.reset_output_buffer()
            self.com.write(str.encode(f"${msg};"))
            self.com.flush()
        except Exception as e:
            print(e)

class Electro:

    def __init__(self):
        # self.langB1 = Button(pin=BUTTON1_LANG, bounce_time=0.1)
        # self.langB2 = Button(pin=BUTTON2_LANG, bounce_time=0.1)
        # self.startB1 = Button(pin=BUTTON1_START, bounce_time=0.1)
        # self.startB2 = Button(pin=BUTTON2_START, bounce_time=0.1)
        self.motor = Motor(forward=MOTOR_LEFT_PIN, backward=MOTOR_RIGHT_PIN, pwm=False)
        self.controller1 = Controller("/dev/ttyUSB0")
        self.controller2 = Controller("/dev/ttyUSB1")
        
    def change_level(self, level):
        if not level in list(levels):
            return 
        vl53, delay = startVL53()
        try:
            p = multiprocessing.Process(target=self._change_level, args=(level, vl53, delay,)) 
            p.start()
            p.join(15)
            if p.is_alive():
                self.motor.stop()
                print("I kill changeLevel()")
                p.terminate()
                p.join()
        finally:
            self.motor.stop()
            stopVL53(vl53)

    def _change_level(self, level, vl53, delay):
        curLevel = getLevel(vl53.get_distance())
        if curLevel == level:
            return
        time.sleep(delay)
        dest_dist = levels[level]
        if curLevel > level:
            self.motor.backward()
            while vl53.get_distance() > dest_dist:
                time.sleep(delay)
        else:
            self.motor.forward()
            while vl53.get_distance() < dest_dist:
                time.sleep(delay)
        self.motor.stop()

ELECTRO = Electro()