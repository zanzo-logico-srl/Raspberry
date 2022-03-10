#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import pyzbar.pyzbar as pyzbar
from logger import multiprocessing, listener_process, listener_configurer, worker_configurer, log_process, logging


# Main


def decodeDisplay(image):
    barcodes = pyzbar.decode(image)
    for barcode in barcodes:
        # Extract the position of the bounding box of the barcode
        # Draw the bounding box of the barcode in the image
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # barcode data is a byte object, so if we want to be on the output image
        # , you need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        # Draw the data and barcode type of the barcode on the image
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    .5, (0, 0, 125), 2)

        # Print barcode data and barcode type to the terminal
        log_process(logging.INFO, "decode display type {} ".format(barcodeType))
        log_process(logging.INFO, "decode display code {}".format(barcodeData))
        return barcodeData
    return None


def detect():
    camera = cv2.VideoCapture(0)
    while True:
        # Read current frame
        ret, frame = camera.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        im = decodeDisplay(gray)

        cv2.waitKey(5)
        if im is not None:
            log_process(logging.INFO, 'qrcode detected')
            return im
        # cv2.imshow("camera", im)
    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':

    queue = multiprocessing.Queue(-1)
    listener = multiprocessing.Process(
        target=listener_process,
        args=(queue, listener_configurer))
    listener.start()
    # worker_configurer(queue)

    detect()
