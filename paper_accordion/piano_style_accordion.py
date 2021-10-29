import pyaudio
import struct
import math

#code modified from from https://stackoverflow.com/questions/26761055/synthesizing-an-audio-pitch-in-python

SHRT_MAX=32767 # short uses 16 bits in complement 2

def my_sin(t,frequency):
    radians = t * frequency * 2.0 * math.pi
    pulse = math.sin(radians)
    return pulse

#pulse_function creates numbers in [-1,1] interval
def generate(duration = 5,pulse_function = (lambda t: my_sin(t,1000))):
    sample_width=2  
    sample_rate = 44100
    sample_duration = 1.0/sample_rate
    total_samples = int(sample_rate * duration)
    p = pyaudio.PyAudio()
    pformat = p.get_format_from_width(sample_width)
    stream = p.open(format=pformat,channels=1,rate=sample_rate,output=True)
    for n in range(total_samples):
        t = n*sample_duration
        pulse = int(SHRT_MAX*pulse_function(t))
        data=struct.pack("h",pulse)
        stream.write(data)

#example of a function I took from wikipedia.
major_chord = f = lambda t: (my_sin(t,440)+my_sin(t,550)+my_sin(t,660))/3

#choose any frequency you want
#choose amplitude from 0 to 1
def create_pulse_function(frequency=1000,amplitude=1):
    return lambda t: amplitude * my_sin(t,frequency)
    

if __name__=="__main__":
    # play fundamental sound at 1000Hz for 5 seconds at maximum intensity
    f = create_pulse_function(1000,1)
    generate(pulse_function=f)
    # play fundamental sound at 500Hz for 5 seconds at maximum intensity
    f = create_pulse_function(500,1)
    generate(pulse_function=f)
    # play fundamental sound at 500Hz for 5 seconds at 50% intensity
    f = create_pulse_function(500,0.5)
    generate(pulse_function=f)