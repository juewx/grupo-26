import cyberpi 
import time
while True:
    if cyberpi.cervo.motor_angle(1) < 30:
        cyberpi.cervo.set_motor_angle(1,cyberpi.cervo.motor_angle(1)+5)
        time.sleep(0.1)
    elif cyberpi.cervo.motor_angle(1) >= 30:
        cyberpi.cervo.set_motor_angle(1,cyberpi.cervo.motor_angle(1)-5)
        time.sleep(0.1)