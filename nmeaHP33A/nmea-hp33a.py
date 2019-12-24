from evdev import InputDevice, categorize, ecodes

device = InputDevice("/dev/ais") # dAISy for tresting - Make HP33A
for event in device.read_loop():
    if event.type == ecodes.EV_KEY:
        print(categorize(event))

 -----------------------------------------------------------------------------------       
>> import asyncio
>>> from evdev import InputDevice, categorize, ecodes

>>> dev = InputDevice('/dev/ais')

>>> async def helper(dev):
...     async for ev in dev.async_read_loop():
...         print(repr(ev))

import asyncio, evdev
-----------------------------------------------------------------------------------
import asyncio, evdev

mouse = evdev.InputDevice('/dev/input/event4')
keybd = evdev.InputDevice('/dev/input/event5')

async def print_events(device):
    async for event in device.async_read_loop():
        print(device.path, evdev.categorize(event), sep=': ')

for device in mouse, keybd:
    asyncio.ensure_future(print_events(device))

loop = asyncio.get_event_loop()
loop.run_forever()
