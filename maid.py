import  cyberpi
import time
import detesion_de_color

while True:
    if cyberpi.quad_rgb_sensor.is_line("L1",1) == True and cyberpi.quad_rgb_sensor.is_line("R1",1) == True:
        cyberpi.mbot2.drive_power(30, -30)
    #si ve a la por la izquierda perro
    elif cyberpi.quad_rgb_sensor.is_line("L1",1) == True and cyberpi.quad_rgb_sensor.is_line("R1",1)== False:
     cyberpi.mbot2.drive_power(0,-30)
    #hola
    elif cyberpi.quad_rgb_sensor.is_line("L1",1) == False and cyberpi.quad_rgb_sensor.is_line("R1",1) == True:
        cyberpi.mbot2.drive_power(30, -0)
    #aaaaa
    elif cyberpi.quad_rgb_sensor.is_line("L1",1) == False and cyberpi.quad_rgb_sensor.is_line("R1",1) == False:
        cyberpi.mbot2.drive_power(-30,30)

def main():
    # Solo sigue la línea si detecta rojo
    if detesion_de_color.detectar_color():
        # Aquí va el código para seguir la línea
        # Por ejemplo:
        print("¡Detectado rojo! Siguiendo la línea...")
        # Tu lógica de movimiento aquí
    else:
        print("No hay rojo. Detenido.")
        # Tu lógica para detener el robot aquí