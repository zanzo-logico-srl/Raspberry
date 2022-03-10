#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import importlib.util
from rgbled import setup, destroy

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


if __name__ == "__main__":
    try:
        print("clear all __main__")
        setup()
        destroy()
        GPIO.cleanup()
    except:
        pass
