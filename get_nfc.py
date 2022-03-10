#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import importlib.util
import mfrc522
from call_rgbled import valid, deny, error, color, ready
from call_rest import verify, access
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



continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
# def end_read(signal,frame):
#     global continue_reading
#     print("Ctrl+C captured, ending read.")
#     continue_reading = False
#     GPIO.cleanup()

# Hook the SIGINT
# signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = mfrc522.MFRC522()

# Welcome message
# print("Welcome to the MFRC522 data read example")
# print("Press Ctrl-C to stop.")



async def loop_nfc():
    while True:
        try:
            # lettura qrcode
            # barcode = detect()
            # logger.info("Hold a tag near the reader")
            # id, text = reader.read()
            # This loop keeps checking for chips. If one is near it will get the UID and authenticate
            while continue_reading:

                # Scan for cards
                (status, TagType) = MIFAREReader.MFRC522_Request(
                    MIFAREReader.PICC_REQIDL)

                # If a card is found
                if status == MIFAREReader.MI_OK:
                    log_process(logging.INFO, "Card detected")
                    log_process(logging.INFO, "Card type {0}".format(TagType))

                # Get the UID of the card

                (status, uid) = MIFAREReader.MFRC522_Anticoll()

                # If we have the UID, continue
                if status == MIFAREReader.MI_OK:

                    # Print UID
                    log_process(logging.INFO, "UID: " + str(uid))
                    # print("Card read UID: %s %s %s %s" % (uid[0], uid[1], uid[2], uid[3]))
                    # logger.info("Card read UID: {0} {1} {2} {3}".format(*uid))

                    # This is the default key for authentication
                    key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

                    # Select the scanned tag
                    zz = MIFAREReader.MFRC522_SelectTag(uid)
                    log_process(logging.INFO, "TAG: " + str(zz))

                    MIFAREReader.Read_MFRC522

                    # Authenticate
                    status = MIFAREReader.MFRC522_Auth(
                        MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

                    # Check if authenticated
                    if status == MIFAREReader.MI_OK:
                        data = MIFAREReader.MFRC522_Read(8)
                        MIFAREReader.MFRC522_StopCrypto1()
                        # print(data)
                    else:
                        log_process(logging.ERROR, "authentication error")

                    # retect code -----------------------------------
                    # logger.info("detect nfc {}".format(uid))
                    id = "".join(map(lambda b: format(b, "02x"), uid))
                    log_process(logging.INFO, "token {0}".format(id))

                    if len(id) > 0:
                        await color(0x0099ff, 1)
                        flag, accessId = verify(str(id), 'card')
                        log_process(logging.INFO, "verify response {}".format(flag))
                        if flag:
                            await valid()
                            log_process(logging.INFO, "verify accessId {}".format(accessId))
                            access(accessId)
                        else:
                            await deny()
                    # print("-----------------------")
                    # logger.info(id)
                    # logger.info(text)

        except:
            log_process(logging.ERROR, "get nfc error")
            await deny()
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

        asyncio.run(loop_nfc())
    except KeyboardInterrupt:
        pass
