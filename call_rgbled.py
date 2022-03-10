#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from rgbled import led, flash
from open_rele import greenled, openrele
import asyncio
from logger import multiprocessing, listener_process, listener_configurer, worker_configurer, log_process, logging


def rgb_demo(): 
    log_process(logging.INFO, "----------------------RGB DEMO!")
    asyncio.run(ready())
    asyncio.run(valid())
    asyncio.run(error())
    asyncio.run(deny())
    asyncio.run(color(0xcc00cc, 1))
    asyncio.run(color(0x00cccc, 1))
    asyncio.run(color(0xcccc00, 1))
    asyncio.run(color(0x00ff00, 1))
    log_process(logging.INFO, "----------------------RGB DEMO Completed!")

async def color(color, times):
    task3 = asyncio.create_task(flash(color, times))
    await task3
    log_process(logging.INFO, "COLOR completed")


async def ready():
    l = 0xff0000
    task3 = asyncio.create_task(flash(l, 2))
    await task3
    log_process(logging.INFO, "completed & READY")


async def deny():
    l = 0xff0000
    task3 = asyncio.create_task(led(l))
    outF = open("access.txt", "w")
    outF.write('DENYACCESS')
    outF.close()
    await task3
    log_process(logging.CRITICAL, "DENY completed")


async def error():
    l = 0xff0000
    task3 = asyncio.create_task(flash(l, 3))
    await task3
    log_process(logging.ERROR, "ERROR completed")


async def valid():
    l = 0x00ff00
    task4 = asyncio.create_task(openrele())
    task3 = asyncio.create_task(led(l))
    # task5 = asyncio.create_task(greenled())
    outF = open("access.txt", "w")
    outF.write('OK')
    outF.close()
    await task4
    await task3
    # await task5
    log_process(logging.INFO, "VALID completed & free")

if __name__ == '__main__':
    queue = multiprocessing.Queue(-1)
    listener = multiprocessing.Process(
        target=listener_process,
        args=(queue, listener_configurer))
    listener.start()
    # worker_configurer(queue)


    log_process(logging.INFO, 'START call_rgbled.py')

    # asyncio.run(testcode('google-oauth2|108786239037208379949', 'barcode'))
    # asyncio.run(ready())
    # asyncio.run(valid())
    # asyncio.run(error())
    # asyncio.run(deny())
    # asyncio.run(color(0xcc00cc, 1)) # red
    # asyncio.run(color(0x00cccc, 1)) # green
    # asyncio.run(color(0xcccc00, 1)) # yellow
    # asyncio.run(color(0xffff00, 1)) # yellow
    asyncio.run(color(0x4040ff, 1)) # yellow light <-------
    asyncio.run(color(0xCCFFFF, 1)) # lightgreen
    asyncio.run(color(0xFFFF00, 1))

