#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import importlib.util

try:
    # Check and import real RPi.GPIO library
    importlib.util.find_spec('RPi.GPIO')
    import RPi.GPIO as GPIO
except ImportError:
    # If real RPi.GPIO library fails, load the fake one
    """
    import FakeRPi.GPIO as GPIO
    OR
    import FakeRPi.RPiO as RPiO
    """
    import FakeRPi.GPIO as GPIO


GPIO.setwarnings(False)
colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFF]

# R_GPIO = 17
# B_GPIO = 27
# G_GPIO = 22

# R_PIN = 11
# B_PIN = 13
# G_PIN = 15


def setup():
    global pins
    global p_R, p_G, p_B

    gpioMode = GPIO.getmode()
    # print("gpioMode : {0}".format(gpioMode))
    if gpioMode is None:
        GPIO.setmode(GPIO.BCM)
        gpioMode = GPIO.BCM
    else:
        GPIO.setmode(gpioMode)

    pins = {'pin_R', 'pin_G', 'pin_B'}
    if gpioMode == 11:  # GPIO
        pins = {'pin_R': 17, 'pin_G': 22, 'pin_B': 27}
        # pins['pin_R'] = 17
        # pins['pin_G'] = 22
        # pins['pin_B'] = 27
    if gpioMode == 10:  # PIN
        pins = {'pin_R': 11, 'pin_G': 13, 'pin_B': 15}
        # pins['pin_R'] = 11
        # pins['pin_G'] = 13
        # pins['pin_B'] = 15

    for i in pins:
        GPIO.setup(pins[i], GPIO.OUT)   # Set pins' mode is output
        # GPIO.output(pins[i], GPIO.HIGH)  # Set pins to high(+3.3V) to off led

    p_R = GPIO.PWM(pins['pin_R'], 2000)  # set Frequece to 2KHz
    p_G = GPIO.PWM(pins['pin_G'], 2000)
    p_B = GPIO.PWM(pins['pin_B'], 2000)

    p_R.start(100)      # Initial duty Cycle = 0(leds off)
    p_G.start(100)
    p_B.start(100)


def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def off():
    for i in pins:
        GPIO.output(pins[i], GPIO.HIGH)    # Turn off all leds


def setColor(col):   # For example : col = 0x112233
    R_val = (col & 0xff0000) >> 16
    G_val = (col & 0x00ff00) >> 8
    B_val = (col & 0x0000ff) >> 0

    R_val = map(R_val, 0, 255, 0, 100)
    G_val = map(G_val, 0, 255, 0, 100)
    B_val = map(B_val, 0, 255, 0, 100)

    p_R.ChangeDutyCycle(100-R_val)     # Change duty cycle
    p_G.ChangeDutyCycle(100-G_val)
    p_B.ChangeDutyCycle(100-B_val)


def loop():
    while True:
        for col in colors:
            setColor(col)
            time.sleep(1)


async def led(color):
    setup()
    setColor(color)
    time.sleep(1.2)
    destroy()


async def flash(color, times=1):
    for i in range(0, times):
        setup()
        # print("value of loop {0}".format(i))
        setColor(color)
        time.sleep(0.5)
        destroy()
        time.sleep(0.5)


def destroy():
    p_R.stop()
    p_G.stop()
    p_B.stop()
    off()
    GPIO.cleanup()


if __name__ == "__main__":
    # try:
    setup()
    # loop()
    color = 0xbfd2db
    setColor(color)
    time.sleep(1)
    destroy()
    # except KeyboardInterrupt:
