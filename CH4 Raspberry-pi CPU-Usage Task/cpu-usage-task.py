# from gpiozero import LED
import psutil
from time import sleep
from datetime import datetime

# led_green = LED(20)
# led_yellow = LED(21)
# led_red = LED(22)

with open("cpu-usage-script.txt", "w") as file:
    while True:
        cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
        cpu_usage_mean = round(sum(cpu_usage) / len(cpu_usage), 3)
        print(f"CPU Usage: {cpu_usage_mean}%")

        if cpu_usage_mean <= 50:
            print("OK - Green LED")
            # led_green.on()
            # led_yellow.off()
            # led_red.off()
        elif cpu_usage_mean < 80:
            print("OK - Yellow LED")
            # led_green.off()
            # led_yellow.on()
            # led_red.off()   
        else:
            print("OK - Red LED")
            # led_green.off()
            # led_yellow.off()
            # led_red.on()   

        data = f"{datetime.now().strftime('%Y/%m/%d %H:%M:%S')} "\
               f"CPU Usage: {cpu_usage_mean}%\n"
        file.write(data)
        file.flush() 
        sleep(5)
