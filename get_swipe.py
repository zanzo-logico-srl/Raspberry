#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import evdev
import asyncio
from evdev import InputDevice, categorize
from numpy import empty  # import * is evil :)
from call_rgbled import valid, deny, error, color
from call_rest import access, verify
from logger import multiprocessing, listener_process, listener_configurer, worker_configurer, log_process, logging


dev = InputDevice('/dev/input/event0')


# Provided as an example taken from my own keyboard attached to a Centos 6 box:
scancodes = {
    # Scancode: ASCIICode
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
}
rv = ''
start = False

# Funzione che esegue la ricerca di una stringa all'interno di una lista
def Search(lista, chiave):
    j = 0
    for i in lista:
        if i == chiave:
            return j
            break
        j += 1
    return False

# Funzione che legge dalla porta seriale
def sync_loop_swipe():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(loop_swipe())
    loop.close()

async def loop_swipe():
    log_process(logging.INFO, 'Device:{0}'.format(dev))
    counterror = 0
    data = None
    key_lookup = None
    rv = None
    start = False
    for event in dev.read_loop():
        try:
            if event.type == evdev.ecodes.EV_KEY:
                data = evdev.categorize(event)  # Save the event temporarily to introspect it
                if data.keystate == 1:  # Down events only
                    key_lookup = scancodes.get(data.scancode) or 'UNKNOWN:{0}'.format(data.scancode)  # Lookup or return UNKNOWN:XX
                    log_process(logging.DEBUG, 'You Pressed the {0} key!'.format(key_lookup))  # Print it all out!
                    #return ';0000000000?' #ERROR!

                    if (key_lookup == ';'): 
                        start = True
                        rv = ''
                    elif (start == True and key_lookup == 'LSHFT'):
                        start = False
                        # logger.info('You Pressed the {0} key!'.format(rv)) 
                    elif (start == True):
                        rv += key_lookup

                if (start == False and rv != ''):
                    log_process(logging.INFO, 'Full key are {0} !'.format(rv))  # Print it all out!
                    # await color(0x4040ff, 1)
                    tmprv = rv
                    rv = ''
                    flag, accessId = verify(str(tmprv), 'card')
                    log_process(logging.INFO, 'Verify Response flag:{0} id:{1} !'.format(flag, accessId))  # Print it all out!
                    if flag == True:
                        await valid()
                        log_process(logging.INFO, 'VALID!')  # Print it all out!
                        access(accessId)
                    else:
                        log_process(logging.INFO, 'DENY!')  # Print it all out!
                        await deny()
                # elif rv != '':
                #     log_process(logging.INFO, 'Elif key : {0}'.format(rv))  # Print it all out!
        except Exception as ex:
            counterror += 1
            log_process(logging.ERROR, "loop except {0} : error.n.{1}".format(sys.exc_info()[0], counterror))
            if (counterror == 5):
                # os.system('kill %d' % os.getpid())
                return
            # await deny()
            await error()
            pass


    #port = None
    #counterror = 0
    #while True:
    #    try:
    #        if port is None:
    #            for device in locations:
    #                logger.debug("loop port is none. Device %s", device)
    #                port = serial.Serial(device, 9600, timeout=3.0, rtscts=1)
    #                port.flushInput()
    #                port.flushOutput()
    #                logger.debug("loop portstr %s", port.portstr)
    #                break
    #        elif port.isOpen() is False:
    #            for device in locations:
    #                logger.debug("loop port is CLOSE. device %s", device)
    #                port = serial.Serial(device, 9600, timeout=3.0)
    #                port.flushInput()
    #                port.flushOutput()
    #                logger.debug("loop portstr %s", port.portstr)
    #                break
    #        else:
    #            time.sleep(.1)
    #            rcv = readlineCR(port)
    #            port.flushInput()
    #            port.flushOutput()
    #            if rcv is not None and rcv != '':
    #                logger.debug("loop else rcv %s", rcv)
    #                await color(0x0099ff, 1)
    #                flag = verify(str(rcv), 'card')
    #                if flag:
    #                    await valid()
    #                    access()
    #                else:
    #                    await deny()
    #            rcv = ''
    #    except:
    #        counterror = counterror + 1
    #        logger.error("loop except %s : %s : error.n.%d",
    #                     device, sys.exc_info()[0], counterror)
    #        if (counterror == 10):
    #            os.system('kill %d' % os.getpid())
    #        await deny()
    #        await error()
    #        pass



if __name__ == "__main__":
    try:
        queue = multiprocessing.Queue(-1)
        listener = multiprocessing.Process(
            target=listener_process,
            args=(queue, listener_configurer))
        listener.start()
        # worker_configurer(queue)

        log_process(logging.INFO, 'START get_swipe.py')
        asyncio.run(loop_swipe())

    except KeyboardInterrupt:
        pass
