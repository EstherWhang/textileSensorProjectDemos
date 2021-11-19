import pyaudio
import numpy as np
import serial
import numpy as np
import time
import pyaudio
from scipy import signal

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

def generate_sine(volume = 1, fs = 44100 , duration = 0.01):
    f = 440.0 *(change_music() +1) #(np.log(change_music() +1) + 1)
    print(change_music())
    # generate samples, note conversion to float32 array
    #samples = np.array((0.1*signal.sawtooth(2*np.pi*np.arange(fs*duration)*f/fs)+(np.sin(2*np.pi*np.arange(fs*duration)*f/fs))).astype(np.float32))
    samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)
    return samples

def fading(chunks):
    chunk = chunks * 0.25

    fade = int(np.ceil(len(chunks)*0.25))

    fade_in = np.arange(0., 1., 1/fade)
    fade_out = np.arange(1., 0., -1/fade)

    chunk[:fade] =np.multiply(chunk[:fade], fade_in)
    chunk[-fade:] = np.multiply(chunk[-fade:], fade_out)
    #print("check chunk")
    #print(len(chunk))
    return chunk.astype(np.float32)


arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.3)
min_value, max_value = 210.0, 370.0 #data_initialization()
p = pyaudio.PyAudio()

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                output=True)

# play. May repeat with different volume values (if done interactively) 
for i in range(100):
    samples = generate_sine(volume = 0.5, fs = 44100 , duration = 0.3)
    stream.write(fading(samples).tobytes())
    

stream.stop_stream()
stream.close()
p.terminate()