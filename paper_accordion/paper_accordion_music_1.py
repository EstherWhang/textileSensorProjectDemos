import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import time
import pyaudio
import struct
import math

#music code modified from from https://stackoverflow.com/questions/26761055/synthesizing-an-audio-pitch-in-python

SHRT_MAX=32767 # short uses 16 bits in complement 2
wave_delta_arcsin = 0.0

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



def change_music():
    global min_value #globals so I can access in animate
    global max_value

    arduino.flushInput()
    arduino.flushOutput()
   #get data from arduino
    arduino_value = get_valid_arduino_values()
    input = 0
    print("value")
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

    return input

def my_sin(t,frequency):
    global wave_delta_arcsin
    radians = t * frequency * 2.0 * math.pi
    pulse = math.sin(radians+wave_delta_arcsin)
    return pulse

#pulse_function creates numbers in [-1,1] interval
def generate(duration = 0.2,pulse_function = (lambda t: my_sin(t,1000))):
    global wave_delta_arcsin
    sample_width=2  
    sample_rate = 44100
    sample_duration = 1.0/sample_rate
    total_samples = int(sample_rate * duration)
    print("total samples: "+str(total_samples))
    p = pyaudio.PyAudio()
    pformat = p.get_format_from_width(sample_width)
    stream = p.open(format=pformat,channels=1,rate=sample_rate,output=True)
    for n in range(total_samples):
        t = n*sample_duration
        pulse_func = pulse_function(t)
        pulse = int(SHRT_MAX*pulse_func)
       # print("n: "+str(n))
        wave_delta_arcsin = np.arcsin(pulse_func)
       # if n == total_samples:
        #    wave_delta_arcsin = np.arcsin(pulse_func)
        data=struct.pack("h",pulse)
        
        stream.write(data)

#example of a function I took from wikipedia.
major_chord = f = lambda t: (my_sin(t,440)+my_sin(t,550)+my_sin(t,660))/3

#choose any frequency you want
#choose amplitude from 0 to 1
def create_pulse_function(frequency=1000,amplitude=1):
    return lambda t: amplitude * my_sin(t,frequency)
    

arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)
min_value, max_value = 190.0, 350.0 #data_initialization()

if __name__=="__main__":
    # play fundamental sound at 1000Hz for 1 seconds at half intensity
    for i in range(1000):
        input = change_music()
        f = create_pulse_function(261.63*(np.log(input+1)+1),1)#261.63
        generate(pulse_function=f)


