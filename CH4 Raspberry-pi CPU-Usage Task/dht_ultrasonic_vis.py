import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import matplotlib.pyplot as plt

# Set up GPIO
GPIO.setmode(GPIO.BCM)
TRIG = 23
ECHO = 24
DHT_PIN = 17
DHT_SENSOR = Adafruit_DHT.DHT11  # Change to DHT11 if using that sensor

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def read_ultrasonic():
    GPIO.output(TRIG, False)
    time.sleep(2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance

def read_dht():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    return humidity, temperature

def main():
    distances = []
    temperatures = []
    humidities = []
    timestamps = []

    try:
        while True:
            distance = read_ultrasonic()
            humidity, temperature = read_dht()

            if humidity is not None and temperature is not None:
                print(f"Distance: {distance} cm, Temperature: {temperature:.1f}C, Humidity: {humidity:.1f}%")
            else:
                print("Failed to retrieve data from DHT sensor")

            distances.append(distance)
            temperatures.append(temperature)
            humidities.append(humidity)
            timestamps.append(time.time())

            # Update plots
            plt.clf()
            plt.subplot(3, 1, 1)
            plt.plot(timestamps, distances, label='Distance (cm)')
            plt.xlabel('Time')
            plt.ylabel('Distance (cm)')
            plt.legend()

            plt.subplot(3, 1, 2)
            plt.plot(timestamps, temperatures, label='Temperature (C)', color='r')
            plt.xlabel('Time')
            plt.ylabel('Temperature (C)')
            plt.legend()

            plt.subplot(3, 1, 3)
            plt.plot(timestamps, humidities, label='Humidity (%)', color='g')
            plt.xlabel('Time')
            plt.ylabel('Humidity (%)')
            plt.legend()

            plt.pause(1)  # Pause to update the plot every second

    except KeyboardInterrupt:
        print("Measurement stopped by user")
        GPIO.cleanup()

if __name__ == "__main__":
    main()
