#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2017 Adafruit Industries
# Author: Tony DiCola & James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!

import time
import subprocess
import busio
import adafruit_ssd1306
import asyncio
from os import path, remove, popen
from datetime import date
from board import SCL, SDA
from PIL import Image, ImageDraw, ImageFont
from logger import multiprocessing, listener_process, listener_configurer, worker_configurer, log_process, logging



# Return % of CPU used by user as a character string
def getCPUuse():
    return(str(popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip()))

# Return CPU temperature as a character string


def getCPUtemperature():
    res = popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=", "").replace("'C\n", ""))

# Return RAM information (unit=kb) in a list
# Index 0: total RAM
# Index 1: used RAM
# Index 2: free RAM


def getRAMinfo():
    p = popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i == 2:
            return(line.split()[1:4])

def logSystemData():
    # CPU informatiom
    log_process(logging.INFO, "CPU Temp:" + getCPUtemperature() + "°" + " CPU Usage:" + getCPUuse() + "%")

    # RAM information
    # Output is in kb, here I convert it in Mb for readability
    RAM_stats = getRAMinfo()
    RAM_total = round(int(RAM_stats[0]) / 1000, 1)
    RAM_used = round(int(RAM_stats[1]) / 1000, 1)
    RAM_free = round(int(RAM_stats[2]) / 1000, 1)
    log_process(logging.INFO, "RAM Total:" + str(RAM_total) + " Used:" + str(RAM_used) + " Free:" + str(RAM_free))


def loop_oled():
    # Create the I2C interface.
    i2c = busio.I2C(SCL, SDA)

    # Create the SSD1306 OLED class.
    # The first two parameters are the pixel width and pixel height.  Change these
    # to the right size for your display!
    disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

    # Clear display.
    disp.fill(0)
    disp.show()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new("1", (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    # draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    # padding = -2
    # top = padding
    # bottom = height - padding

    # Move left to right keeping track of the current x position for drawing shapes.
    left = 1
    top = -2

    # Load default font.
    # font = ImageFont.load_default()

    # Alternatively load a TTF font.  Make sure the .ttf font file is in the
    # same directory as the python script!
    # Some other nice fonts to try: http://www.dafont.com/bitmap.php
    # font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
    font = ImageFont.truetype(
        '/usr/share/fonts/truetype/quicksand/Quicksand-Regular.ttf', 12)
    font16 = ImageFont.truetype(
        '/usr/share/fonts/truetype/quicksand/Quicksand-Regular.ttf', 16)
    fontMedium = ImageFont.truetype(
        '/usr/share/fonts/truetype/quicksand/Quicksand-Regular.ttf', 22)
    fontBig = ImageFont.truetype(
        '/usr/share/fonts/truetype/quicksand/Quicksand-Regular.ttf', 28)

    days = ['Domenica', 'Lunedì', 'Martedì',
            'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato']

    looper = 0
    switch = 0
    data = ''
    filename = 'access.txt'

    t = time.time()

    log_process(logging.INFO, "LOOP OLED TIME {0}".format(t))

    while True:

        if time.time() - t > 5*60: # 5minutes
            logSystemData()
            t = time.time()

        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        # Shell scripts for system monitoring from here:
        # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
        cmd = "hostname -I | cut -d' ' -f1"
        IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
        # cmd = "top -bn1 | grep load | awk '{printf \"CPU : %s %% \", $(NF-2)*100}'"
        # CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
        # cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
        cmd = "free -m | awk 'NR==2{printf \"Mem : %.2f%% \", $3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
        # cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
        # Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
        Ora = time.strftime("%H:%M:%S")
        Data = time.strftime("%d-%m-%Y")
        # Giorno = time.strftime("%A")
        dayNumber = date.today().weekday()
        Giorno = days[dayNumber]

        # Write  lines of text.
        if path.isfile(filename) == True:
            log_process(logging.DEBUG, "File {0} exist".format(filename))
            switch = 4

        if switch == 0 or switch == 1:
            draw.text((left, top + 0), "IP: " + IP, font=font, fill=255)
            draw.text((left, top + 11), getCPUuse(), font=font, fill=255)
            draw.text((left, top + 22), MemUsage, font=font, fill=255)

        if switch == 2:
            draw.text((left, top + 2), Ora, font=fontMedium, fill=255)

        if switch == 3:
            draw.text((left, top), Giorno, font=font16, fill=255)
            draw.text((left, top + 18), Data, font=font16, fill=255)

        if switch == 4:
            switch = 0 # imposto il case successivo
            if path.isfile(filename) == True:
                with open(filename, 'r') as file:
                    data = file.read().replace('\n', '')
                    log_process(logging.INFO, "READ DATA FROM FILE IS >" + data + "<")
                remove(filename)
                if data == "OK":
                    draw.text((left, top + 2), "OK", font=fontBig, fill=255)
                    # log_process(logging.INFO, ">" + data + "<")
                else:
                    draw.text((left, top + 2), "NO ACCESS", font=fontMedium, fill=255)
                    log_process(logging.INFO, "EXECUTED BRANCH --> NO ACCESS") 
                data = ''
                time.sleep(0.8)

        # if(looper >= 20):
        #     if path.isfile(filename):
        #         remove(filename)
        #     looper = 0
        #     if switch >= 3:
        #         switch = 0
        # if (looper == 0):
        #     switch += 1

        # Display image.
        disp.image(image)
        disp.show()
        time.sleep(0.2)
        # looper += 1
        if switch >= 3:
            switch = 0



if __name__ == "__main__":
    try:
        queue = multiprocessing.Queue(-1)
        listener = multiprocessing.Process(
            target=listener_process,
            args=(queue, listener_configurer))
        listener.start()
        # worker_configurer(queue)

        log_process(logging.INFO, 'START i2c_display_oled.py')
        asyncio.run(loop_oled())

    except KeyboardInterrupt:
        pass
