import RPi.GPIO as GPIO
from flask import Flask, request,render_template
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.OUT)

app = Flask(__name__)

@app.route('/led_on')
def led_on():
    GPIO.output(23,GPIO.HIGH)
    print("ONNN")
    return 'LED ON'


@app.route('/')
def mainPath():
    return render_template("client.html")


@app.route('/led_off')
def led_off():    
    GPIO.output(23,GPIO.LOW)
    print("OFF")
    return 'LED OFF'

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port='5000')
