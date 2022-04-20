from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import time
import random
import datetime
import csv

GPIO.setmode(GPIO.BCM)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
pins = (17,27,22) # R = 11, G = 12, B = 13
patient_name = input("What is the patient's name?  ")
app = Flask(__name__)
user_emotion = ""
collected_data=[]
user_name=""
user_emotion=""

def setup():
    global pwmR, pwmG, pwmB
    for i in pins:  # iterate on the RGB pins, initialize each and set to HIGH to turn it off (COMMON ANODE)
        GPIO.setup(i, GPIO.OUT)
    pwmR = GPIO.PWM(pins[0], 2000)  # set each PWM pin to 2 KHz
    pwmG = GPIO.PWM(pins[1], 2000)
    pwmB = GPIO.PWM(pins[2], 2000)
    pwmR.start(0)   # initially set to 0 duty cycle
    pwmG.start(0)
    pwmB.start(0)
     
def setColor(r, g, b):  # 0 ~ 100 values since 0 ~ 100 only for duty cycle
    pwmR.ChangeDutyCycle(r)
    pwmG.ChangeDutyCycle(g)
    pwmB.ChangeDutyCycle(b)

    

setup()

@app.route("/", methods=["GET", "POST"])
def home():
    user_emotion = request.form.get("emote")
    current_time = datetime.datetime.now() 
    time=current_time.strftime("%H:%M:%S")
    day=current_time.strftime("%m/%d/%Y")
    input_emotion=""
    user_name=patient_name
    if(int(current_time.strftime("%H")) >11):
        time_of_day="Afternoon"
    else:
        time_of_day="Morning"
    
    
    if user_emotion == "Happy":
    	setColor(0, 100, 0) # green
    if user_emotion == "Sad":
    	setColor(0, 0, 100) # blue
    if user_emotion == "Angry":
    	setColor(100, 0, 0) #   red 
    if user_emotion == "Hungry":
    	setColor(100, 100, 0) # yellow
    if user_emotion == "Thirsty":
    	setColor(0, 100, 100) # cyan
    if user_emotion != "Open this select menu":
        if user_emotion == "Nurse":
            user_emotion = "N/A"
            user_name = "Nurse"
        collected_data.append({"user": user_name, "time": time, "day": day, "emotion": user_emotion})
        for elem in collected_data:
            print(elem)
        
        keys = collected_data[0].keys()

        with open('data.csv', 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(collected_data)    

    return render_template("index.html", messages={'name': patient_name, 'time': time_of_day})
    
    
if __name__ == '__main__':
    app.run(host='10.224.18.28', port=5000, debug=True, threaded=False)
    
