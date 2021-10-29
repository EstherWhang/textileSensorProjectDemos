
import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import time

#https://create.arduino.cc/projecthub/ansh2919/serial-communication-between-python-and-arduino-e7cce0

#future setup: make this all into a class so I can make multiple bendy things
# I would need to parse serial input to corresponding object
#also would need to initialize head/tail for arrows

def get_valid_arduino_values():

    while True:
        arduino_read = arduino.readline()
        print(arduino_read)
        if arduino_read != b'' and arduino_read != b'\n' and arduino_read != b'\r\n' and arduino_read != b'0\r\n': #check I don't get null value
            arduino_value = float(arduino_read.strip())
            #print("checking: arduino value" + str(arduino_value))
            return arduino_value
        elif str(arduino_read)[1:5] == "'a='":
            print(str(arduino_read)[1:5])
            continue
        else:
            print("wait a bit")

def check_reasonable(min_array, max_array):
    min_array.sort() #least to greatest
    max_array.sort()

    min_test = 0
    max_test = 0
    
    for i in range(1,49):
        
        mean_with_extremes = np.mean(min_array)
        print("slice for min_array")
        print(min_array[i:])
        mean_without_min = np.mean(min_array[i:])

        #just to get outliers
        if abs(mean_with_extremes - mean_without_min) < 1:  #turn this into percentage? so withoutmin/withmin?
            min_test = min_array[i]

        mean_with_extremes = np.mean(max_array)
        mean_without_max = np.mean(max_array[:-i])
        print("slice for max_array")
        print(max_array[:-i])

        #just to get outliers
        if abs(mean_with_extremes - mean_without_max) < 1:
            max_test = max_array[-i]
        
        if min_test !=0 and max_test !=0:
            print(min_test, max_test)
            return min_test, max_test
                

def data_initialization(): #determines the range of the sensor of folded vs straight arm
    global min_value #globals so I can access in animate
    global max_value
    min_value = 0
    max_value = 0

    straight_arm = []
    folded_arm = []

    while True:
        setting = input("Which Calibration? (0, 180, done)")
        if setting == "0": 
            print("intializing: hold pose for at least 10 seconds")
            straight_arm = [] #reset
            arduino.flushInput()
            arduino.flushOutput()
            for i in range(50):
                arduino_value = get_valid_arduino_values()
                #print(arduino_value)
                straight_arm.append(arduino_value)
                time.sleep(0.1)
            #max_value = np.max(straight_arm)
            
        elif setting == "180":
            folded_arm = [] #reset 
            arduino.flushInput()
            arduino.flushOutput()
            print("intializing: hold pose for at least 10 seconds")
            for i in range(50): #serial flush
                arduino_value = get_valid_arduino_values()
                #print(arduino_value)
                folded_arm.append(arduino_value)
                time.sleep(0.1)
            #min_value = check_reasonable(folded_arm, "min")
            #min_value = np.min(folded_arm)
               
        elif setting == "done":
            
            min_value, max_value = check_reasonable(folded_arm, straight_arm)
            print(min_value, max_value)
            return min_value, max_value
        else:
            print("Please calibrate")

def calculate_angle(min_value, max_value):
    i = 0
    input = 0

    arduino.flushInput()
    arduino.flushOutput()

    while True:
        arduino_value = get_valid_arduino_values()
        i+=1
        if arduino_value < 1.1*max_value and arduino_value > 0.9*min_value:
            #this after checking that arduino value isnt ridiculous or recalibrating
            #treating higer values as freak occurances
            #issue with current calibration is that it pushes min_values and max_values further up
            if arduino_value > max_value: 
                input = 0
            elif arduino_value < min_value:
                input = 1
            else:
                input = ((max_value-arduino_value) / ((max_value)-(min_value))) 
                break
        if i > 100:
            print("need to recalibrate")
            min_value, max_value = data_initialization()

    angle = (input)*(np.pi) #convert to radians
    print(arduino_value, input, angle)
    return angle

def main_code():
    global min_value #globals so I can access in animate
    global max_value

   #get data from arduino
    input = 0
    #print("before update")
    print(min_value, max_value)
        
    #convert data to angle
    angle = calculate_angle(min_value, max_value)
    
    degrees = angle* (180/np.pi)
    #write to arduino
    message_to_arduino = 'a' + str(degrees) +'\n'
    print(message_to_arduino.encode())
    arduino.write(message_to_arduino.encode())

    #way to break
i = 0
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)
min_value, max_value = data_initialization()
#min_value, max_value = 20.0, 120.0

while True:
    i +=1
    main_code()
    if i > 1000:
        False

#frequency!!!
#sewing it to make this neater
#smoothing

