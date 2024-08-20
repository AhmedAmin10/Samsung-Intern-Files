from matplotlib import pyplot as plt
from matplotlib import animation
from gpiozero import LED
import numpy as np
import Adafruit_DHT
import time
sensor = Adafruit_DHT.DHTII
pin = 20
led_blue = LED(20)
led_red = LED (21)

fig = plt.figure()
ax= plt.axes(xlim=(0, 30), ylim=(15, 45))
line,= ax.plot(np.arange(30), np.ones(30, dtype=float)* np.nan, Iw=l, c='blue',marker= 'd',ms=2)
h,t = Adafruit_DHT.read_retry(sensor,pin)
def init():
    return line
def animate (i):
    h,t = Adafruit_DHT.read_retry(sensor,pin)
    if t <=25:
        led_blue.on()
        led_red.off()
    else:
        led_blue.off()
        led_red.on()
    print(f"Frame #{i} - Temprature = {t}")
    y=t
    old_y= line.get_ydata()
    new_y = np.r_[old_y[1:] , y]
    line.set_ydata(new_y)
    return line ,
anim = animation.FuncAnimation(fig,animate, init_func=init, frames=30, interval =100,blit =False)
anim.save(f"/home_{int(time.time())}.gif",writer='pillow')
led_blue.off()
led_red.off()
