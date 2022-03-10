#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
from sys import exc_info
from qrcode import detect
from call_rgbled import valid, deny, error, color
from call_rest import verify, access
from logger import multiprocessing, listener_process, listener_configurer, worker_configurer, log_process, logging


def sync_loop_barcode():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(loop_barcode())
    loop.close()


async def loop_barcode():
    while True:
        try:
            # lettura qrcode
            barcode = detect()
            log_process(logging.INFO, "detect barcode {}".format(barcode))
            if barcode is not None and barcode != '':
                await color(0x4040ff, 0.5)
                flag, accessId = verify(str(barcode), 'barcode')
                log_process(logging.INFO, 'Verify Response flag:{0} id:{1} !'.format(
                    flag, accessId))  # Print it all out!
                if flag == True:
                    await valid()
                    log_process(logging.INFO, 'VALID!')  # Print it all out!
                    access(accessId)
                else:
                    log_process(logging.INFO, 'DENY!')  # Print it all out!
                    await deny()
                # asyncio.coroutine(testcode(barcode, 'barcode'))
                # prepare_for_foo()
                # await testcode(barcode, 'barcode')
                # task = loop.create_task(testcode(barcode, 'barcode'))
                # remaining_work_not_depends_on_foo()
        except Exception as e:  # work on python 2.x
            log_process(logging.ERROR, "get barcode error", exc_info=True)
            # log_process(logging.ERROR, 'exception message: ' +
            #             str(e), exc_info=True)
            # await deny()
            await error()
            pass

        # dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # show("AreaFerrero", dt_string, 0.5)

if __name__ == "__main__":
    try:
        queue = multiprocessing.Queue(-1)
        listener = multiprocessing.Process(
            target=listener_process,
            args=(queue, listener_configurer))
        listener.start()
        # worker_configurer(queue)

        asyncio.run(loop_barcode())

    except KeyboardInterrupt:
        pass
