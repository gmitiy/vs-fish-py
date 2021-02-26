from gpiozero import Motor
from VL53L0X import VL53L0X, Vl53l0xAccuracyMode
import time

MOTOR_LEFT_PIN = "BOARD32"
MOTOR_RIGHT_PIN = "BOARD33"

levels = {
    1: 100,
    2: 200,
    3: 300,
    4: 400,
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
    time.sleep(0.01)
    return vl53


def stopVL53(vl53: VL53L0X):
    try:
        vl53.stop_ranging()
        vl53.close()
        del(vl53)
    except:
        pass


class Electro:

    def __init__(self):
        self.motor = Motor(forward=MOTOR_LEFT_PIN, backward=MOTOR_RIGHT_PIN)
        
    def change_level(self, level):
        if not level in list(levels):
            return 
        try:
            vl53 = startVL53()
            curLevel = getLevel(vl53.get_distance())
            
            if curLevel == level:
                return

            time.sleep(0.01)
            dest_dist = levels[level]

            if curLevel > level:
                self.motor.backward()
                while vl53.get_distance() > dest_dist:
                    time.sleep(0.07)
            else:
                self.motor.forward()
                while vl53.get_distance() < dest_dist:
                    time.sleep(0.07)
            self.motor.stop()
             
        finally:
            stopVL53(vl53)


ELECTRO = Electro()