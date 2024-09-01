import RPi.GPIO as GPIO
import time
import mysql.connector

# Ultrasonic Sensor GPIO Pins
TRIG = 23
ECHO = 24

# Database connection setup
try:
    conn = mysql.connector.connect(
        user="new",        # Replace with your MariaDB username
        password="1234",    # Replace with your MariaDB password
        host="localhost",            # Since MariaDB is on the same Pi
        database="UltrasonicDB"
    )
    cursor = conn.cursor()
except mysql.connector.Error as e:
    print(f"Error connecting to MariaDB: {e}")
    exit(1)

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def measure_distance():
    # Send a 10us pulse to trigger the sensor
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Measure the time of the echo
    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(ECHO) == 0:
        start_time = time.time()

    while GPIO.input(ECHO) == 1:
        stop_time = time.time()

    # Calculate the time difference and convert it to distance
    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2  # Speed of sound is 34300 cm/s

    return distance

try:
    while True:
        distance = measure_distance()
        print(f"Distance: {distance:.2f} cm")

        # Insert reading into the MariaDB database
        try:
            cursor.execute("INSERT INTO Readings (distance) VALUES (%s)", (distance,))
            conn.commit()
            print("Distance saved to database.")
        except mysql.connector.Error as e:
            print(f"Error inserting data: {e}")

        time.sleep(1)  # Adjust delay between measurements as needed

except KeyboardInterrupt:
    print("Measurement stopped by User")

finally:
    # Cleanup GPIO and close database connection
    GPIO.cleanup()
    conn.close()