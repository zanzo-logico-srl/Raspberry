#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import threading
import asyncio
import socket
import subprocess
from logger import multiprocessing, listener_process, listener_configurer, worker_configurer, log_process, logging
from i2c_display_oled import loop_oled
from call_rgbled import rgb_demo
from get_swipe import sync_loop_swipe
from get_barcode import sync_loop_barcode
from open_rele import sync_read


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

async def main():
    queue = multiprocessing.Queue(-1)
    listener = multiprocessing.Process(
        target=listener_process,
        args=(queue, listener_configurer))
    listener.start()
    worker_configurer(queue)

    while True:
        time.sleep(0.5)
        ip = get_ip()
        log_process(logging.INFO, 'waiting for ip {0}'.format(ip))
        if ip != '127.0.0.1':
            break


    log_process(logging.INFO, 'START! i2c_display_oled.py')
    f = threading.Thread(name='displayoled', target=loop_oled)
    f.start()

    log_process(logging.INFO, 'START! get_swipe.py')
    s = threading.Thread(name='swipe', target=sync_loop_swipe)
    s.start()

    # log_process(logging.INFO, 'START! call_rgbled.py')
    # b = threading.Thread(name='background', target=rgb_demo)
    # b.start()

    # log_process(logging.INFO, 'START! open_rele.py')
    # r = threading.Thread(name='background', target=sync_read)
    # r.start()

    log_process(logging.INFO, 'START! get_barcode.py')
    p = threading.Thread(name='barcode', target=sync_loop_barcode)
    p.start()

    log_process(logging.INFO, 'START! rest_server.py')
    subprocess.run("python3 rest_server.py", shell=True)

    # log_process(logging.INFO, 'START! open_rele.py')
    # subprocess.run("python3 open_rele.py", shell=True)

    while True:
        time.sleep(30)
        # log_process(logging.INFO, 'loop 30sec timeout')

    # asyncio.run(testcode('google-oauth2|108786239037208379949', 'barcode'))
    # queue.put_nowait(None)
    # listener.join()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
