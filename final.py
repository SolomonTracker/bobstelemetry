from ina219 import INA219
from gpiozero import InputDevice, AngularServo
from time import sleep
import signal
import sys
from numpy import random

# Current sensor setup
SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 0.2

# InfraRed sensor setup
sensor = InputDevice(17)

# Servo motor setup
#servo = AngularServo(18, min_pulse_width=0.0006, max_pulse_width=0.0023)
servo = AngularServo(18)
#servo.speed(20)

# Function to handle interrupt and stop servo safely
def signal_handler(sig, frame):
    print("Interruption received, stopping the servo.")
    servo.angle = 0  # Put the servo in neutral position
    sys.exit(0)

# Register the signal handler
#signal.signal(signal.SIGINT, signal_handler)

# Energy consumption (Wh)
def energy(w):
    return ((0.9*(w*0.02-1.5))/1.5 + 1 + 50*10**(-3)+5 + random.rand())

last_detected = False
cont = 0
# Main loop
try:
    while True:
        # Read current sensor
        #read_current()
        #print(f"Power Consumption: {energy(20)} Wh")
        # Check infrared sensor state
        if sensor.is_active:
            #print("No obstacle detected")  # Prints when no obstacle is detected
            if last_detected:
                cont += 1
                print(f"Box count: {cont}")
            last_detected = False
        else:
            #print("Obstacle detected")
            last_detected = True

     # Prints when an obstacle is detected

        sleep(0.25)  # Delay for a second before repeating
        energy1 = energy(20)
        print(f"Energy consumption [Wh]: {energy1}")

except KeyboardInterrupt:
    print("Program terminated.")
    sensor.close()
    servo.close()  # Stop the servo when the program is interrupted
    sys.exit(0)
    
