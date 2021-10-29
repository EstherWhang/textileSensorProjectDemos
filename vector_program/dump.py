#change it so its the opposite number
arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)

def data_initialization():
    straight_arm = []
    folded_arm = []
    min_value = 0
    max_value = 0
    while True:
        setting = input("Which Calibration? (0, 180, done)")
        arduino_value = arduino.readline()
        if setting == "0": 
            for i in range(10):
                straight_arm.append(arduino_value)
                time.sleep(0.1)
            min_value = min(straight_arm)
        elif setting == "180":
            for i in range(10):
                folded_arm.append(arduino_value)
                time.sleep(0.1)
            max_value = max(folded_arm)
        elif setting == "done":
            return min_value, max_value
        else:
            print("Please calibrate")
            break

