#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import importlib.util
import asyncio
from logger import multiprocessing, listener_process, listener_configurer, worker_configurer, log_process, logging

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



# LED = 21
# PUSH = 20
# RELE = 16
pins = {'pin_LED', 'pin_PUSH', 'pin_RELE'}

def sync_read():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(read())
    loop.close()
    

def setup():
    global pins

    GPIO.setwarnings(False)
    gpioMode = GPIO.getmode()
    log_process(logging.INFO, "gpioMode : {0}".format(gpioMode))
    if gpioMode is None:
        GPIO.setmode(GPIO.BCM)
        gpioMode = GPIO.BCM
    else:
        GPIO.setmode(gpioMode)

    if gpioMode == 11:  # GPIO
        pins = {'pin_LED': 21, 'pin_PUSH': 20, 'pin_RELE': 16}
    if gpioMode == 10:  # PIN
        pins = {'pin_LED': 40, 'pin_PUSH': 38, 'pin_RELE': 36}

    # GPIO.setmode(GPIO.BCM)
    # set the initial output of pin to be LOW
    GPIO.setup(pins['pin_PUSH'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(pins['pin_LED'], GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(pins['pin_RELE'], GPIO.OUT, initial=GPIO.LOW)


# async def read():
#     setup()
#     while True:
#         if GPIO.input(pins['pin_PUSH']) == GPIO.HIGH:
#             await greenled()
#             await openrele()
#         time.sleep(0.5)


async def greenled():
    setup()
    log_process(logging.INFO, "Green LED on")
    GPIO.output(pins['pin_LED'], GPIO.HIGH)
    time.sleep(0.5)
    log_process(logging.INFO, "Green LED off")
    GPIO.output(pins['pin_LED'], GPIO.LOW)


async def openrele():
    setup()
    log_process(logging.WARNING, "OPEN Relè on")
    GPIO.output(pins['pin_RELE'], GPIO.HIGH)
    time.sleep(1)
    log_process(logging.WARNING, "OPEN Relè off")
    GPIO.output(pins['pin_RELE'], GPIO.LOW)


if __name__ == '__main__':
    try:
        queue = multiprocessing.Queue(-1)
        listener = multiprocessing.Process(
            target=listener_process,
            args=(queue, listener_configurer))
        listener.start()
        # worker_configurer(queue)

        # asyncio.run(read())
    except KeyboardInterrupt:
        pass