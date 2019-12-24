from evdev import InputDevice, categorize, ecodes

device = InputDevice("/dev/ais") # dAISy for tresting - Make HP33A
for event in device.read_loop():
    if event.type == ecodes.EV_KEY:
        print(categorize(event))
