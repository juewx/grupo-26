import time
import cyberpi

def linea(velocidad_base):
    offset = cyberpi.quad_rgb_sensor.get_offset_track(1)
    velocidad_motor_derecha = -velocidad_base + (-offset * 0.5)
    velocidad_motor_izquierda = velocidad_base + (-offset * 0.6)
    cyberpi.mbot2.drive_speed(velocidad_motor_izquierda, velocidad_motor_derecha)

@cyberpi.event.is_press("a")
def press_a():
    while True:
        baño()
        
        grutita()
        cancer()
        despertar()
        linea(25)

def baño():
    sen_izquierda = cyberpi.quad_rgb_sensor.is_color("b", "L1", 1)
    sen_derecha = cyberpi.quad_rgb_sensor.is_color("b", "R1", 1)

    if sen_derecha or sen_izquierda:
        cyberpi.mbot2.drive_power(0, 0)
        time.sleep(0.2)
        cyberpi.mbot2.turn(5, 10)
        time.sleep(0.3)
        cyberpi.mbot2.servo_set(90, "s1")
        time.sleep(0.2)
        cyberpi.mbot2.servo_set(170, "s1")
        time.sleep(0.3)
        cyberpi.mbot2.servo_set(90,"s1")
        time.sleep(0.2)
        cyberpi.mbot2.servo_set(170, "s1")
        time.sleep(0.2)
        cyberpi.mbot2.servo_set(90, "s1")
        time.sleep(0.2)
        cyberpi.mbot2.drive_power(-40,40)
        time.sleep(0.8)
        cyberpi.mbot2.turn(-90, 25)
        time.sleep(0.2)

def cancer():
    sen_izquierda = cyberpi.quad_rgb_sensor.is_color("y", "L1", 1)
    sen_derecha = cyberpi.quad_rgb_sensor.is_color("y", "R1", 1)

    if sen_derecha == True or sen_izquierda == True:
    
     cyberpi.mbot2.turn(85,-10)    
     time.sleep(0.1)               
     

def grutita():
    sen_izquierda = cyberpi.quad_rgb_sensor.is_color("g", "L1", 1)
    sen_derecha = cyberpi.quad_rgb_sensor.is_color("g", "R1", 1)

    if sen_derecha == True or sen_izquierda == True:
        cyberpi.mbot2.drive_power(20,-20)
        time.sleep(0.5)
        cyberpi.mbot2.servo_set(92,"s3")
        time.sleep(0.2)
        cyberpi.mbot2.servo_set(70,"s3")
        time.sleep(0.2)
        cyberpi.mbot2.drive_power(-10,10)
        time.sleep(1.2)
        cyberpi.mbot2.turn(-120,20)
        time.sleep(0.1)
        cyberpi.mbot2.drive_power(20,-20)
        time.sleep(1.0)
        cyberpi.mbot2.drive_power(0,0)
        time.sleep(120)

def despertar():
    sen_izquierda = cyberpi.quad_rgb_sensor.is_color("r", "L1", 1)
    sen_derecha = cyberpi.quad_rgb_sensor.is_color("r", "R1", 1)

    if sen_derecha == True or sen_izquierda == True:
        cyberpi.mbot2.turn(60,20)
        time.sleep(0.1)
        cyberpi.mbot2.turn(-30,20)
        time.sleep(0.1)
        cyberpi.mbot2.turn(30,10)
        time.sleep(0.1)
        cyberpi.mbot2.servo_set(90, "s1")
        time.sleep(0.2)
        cyberpi.mbot2.servo_set(90, "s3")
        time.sleep(0.2)
        cyberpi.mbot2.straight(3,40)
        time.sleep(0.1)
        cyberpi.mbot2.turn(-10,8)