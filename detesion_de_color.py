import cyberpi
import time

def detectar_color():
    # Si detecta rojo en L1 o R1
    if cyberpi.quad_rgb_sensor.is_color("L1", "red") or cyberpi.quad_rgb_sensor.is_color("R1", "red"):
        cyberpi.led.set_bri(50)      # Enciende los ojos al 50%
        time.sleep(2)                # Espera 2 segundos
        cyberpi.led.set_bri(100)     # Sube el brillo al 100%
        return True
    else:
        cyberpi.led.set_bri(0)       # Apaga los ojos si no hay rojo
        return False

while True:
    detectar_color()
    time.sleep(0.1)