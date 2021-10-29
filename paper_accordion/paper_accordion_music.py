import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import time

def get_valid_arduino_values():
    
    while True:
        arduino_read = arduino.readline()
        #print(arduino_read)
        if arduino_read != b'' and arduino_read != b'\n' and arduino_read != b'\r\n' and arduino_read != b'0\r\n': #check I don't get null value
            arduino_value = float(arduino_read.strip())
            #print("checking: arduino value" + str(arduino_value))
            return arduino_value
            
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

    max_value_array = []
    min_value_array = []

    while True:
        setting = input("Which Calibration? (straight, squished, done)")
        if setting == "straight": 
            print("intializing: hold for at least 10 seconds")
            max_value_array = [] #reset
            arduino.flushInput()
            arduino.flushOutput()
            for i in range(50):
                arduino_value = get_valid_arduino_values()
                #print(arduino_value)
                max_value_array.append(arduino_value)
                time.sleep(0.1)
            #max_value = np.max(straight_arm)
            
        elif setting == "squished":
            min_value_array = [] #reset 
            arduino.flushInput()
            arduino.flushOutput()
            print("intializing: hold for at least 10 seconds")
            for i in range(50): #serial flush
                arduino_value = get_valid_arduino_values()
                #print(arduino_value)
                min_value_array.append(arduino_value)
                time.sleep(0.1)
            #min_value = check_reasonable(folded_arm, "min")
            #min_value = np.min(folded_arm)
               
        elif setting == "done":
            
            min_value, max_value = check_reasonable(min_value_array, max_value_array)
            print(min_value, max_value)
            return min_value, max_value
        else:
            print("Please calibrate")



def change_music(i):
    global min_value #globals so I can access in animate
    global max_value

    arduino.flushInput()
    arduino.flushOutput()
   #get data from arduino
    arduino_value = 0
    input = 0
    print("before update")
    print(min_value, max_value)


    #this after checking that arduino value isnt ridiculous or recalibrating
    #treating higer values as freak occurances
    #issue with current calibration is that it pushes min_values and max_values further up

    if arduino_value > max_value: 
        input = 0
    elif arduino_value < min_value:
        input = 1
    else:
        input = ((max_value-arduino_value) / ((max_value)-(min_value)))


arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)
min_value, max_value = data_initialization()
print(min_value, max_value)
