from gpiozero import DistanceSensor, Servo
from time import sleep

# Set up the DistanceSensor
# Trigger pin (Trig) is connected to GPIO 18
# Echo pin (Echo) is connected to GPIO 24
sensor = DistanceSensor(echo=15, trigger=14)

# Set up the LED on GPIO pin 17
servo = Servo(18)

# Define the threshold distance in meters
threshold_distance = 0.3  # 20 centimeters

try:
    while True:
        # Measure the distance
        distance = sensor.distance
        
        # Print the distance
        print(f"Distance: {distance * 100:.1f} cm")
        
        # Turn on the LED if an object is within the threshold distance
        if distance < threshold_distance:
            servo.max()
        else:
            servo.value = None
        
        # Wait for a short time before the next measurement
        sleep(1)

except KeyboardInterrupt:
    print("Program stopped by user")
    servo.mid()  # Ensure the LED is turned off
