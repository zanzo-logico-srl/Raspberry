
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# https://docs.python.org/3/howto/logging-cookbook.html#logging-to-a-single-file-from-multiple-processes

import datetime
import sys
import logging
import logging.handlers
import multiprocessing


# The size of the rotated files is made small so you can see the results easily.
def listener_configurer():
    try:
        root = logging.getLogger()
        now = datetime.datetime.now()
        h = logging.handlers.RotatingFileHandler('/home/pi/AreaFerrero/log/raspberry.log', maxBytes=100*1024, backupCount=10)
        # h = logging.handlers.RotatingFileHandler('log/scripts.log', when='D', interval=1, backupCount=10)
        # %(processName)-10s
        f = logging.Formatter('%(asctime)s %(name)s %(levelname)-8s %(message)s')
        h.setFormatter(f)
        root.addHandler(h)
    except Exception:
        import sys, traceback
        print('Whoops! listener_configurer Problem:', file=open("/home/pi/AreaFerrero/log/errlog.txt","a"))
        traceback.print_exc(file=open("/home/pi/AreaFerrero/log/errlog.txt","a"))

# This is the listener process top-level loop: wait for logging events
# (LogRecords)on the queue and handle them, quit when you get a None for a
# LogRecord.
def listener_process(queue, configurer):
    configurer()
    while True:
        try:
            record = queue.get()
            if record is None:  # We send this as a sentinel to tell the listener to quit.
                break
            logger = logging.getLogger(record.name)
            logger.handle(record)  # No level or filter logic applied - just do it!
        except Exception:
            import sys, traceback
            print('Whoops! listener_process Problem:', file=open("/home/pi/AreaFerrero/log/errlog.txt","a"))
            traceback.print_exc(file=open("/home/pi/AreaFerrero/log/errlog.txt","a"))

def worker_configurer(queue):
    try:
        h = logging.handlers.QueueHandler(queue)  # Just the one handler needed
        root = logging.getLogger()
        root.addHandler(h)
        # send all messages, for demo; no other level or filter logic applied.
        root.setLevel(logging.DEBUG)
    except Exception:
        import sys, traceback
        print('Whoops! worker_configurer Problem:', file=open("/home/pi/AreaFerrero/log/errlog.txt","a"))
        traceback.print_exc(file=open("/home/pi/AreaFerrero/log/errlog.txt","a"))

# This is the worker process top-level loop, which just logs ten events with
# random intervening delays before terminating.
# The print messages are just so you know it's doing something!
def worker_process(queue, configurer):
    try:
        configurer(queue)
        name = multiprocessing.current_process().name
        print('Worker started: %s' % name)
        # for i in range(10):
        # time.sleep(random())
        logger = logging.getLogger(name)
        # level = choice(LEVELS)
        # message = choice(MESSAGES)
        logger.debug("message")
        print('Worker finished: %s' % name)
    except Exception:
        import sys, traceback
        print('Whoops! worker_process Problem:', file=open("/home/pi/AreaFerrero/log/errlog.txt","a"))
        traceback.print_exc(file=open("/home/pi/AreaFerrero/log/errlog.txt","a"))

def log_process(level, message):
    try:
        # worker_configurer(queue)
        name = multiprocessing.current_process().name
        # print('Log Process: %s' % name)
        logger = logging.getLogger(name)
        # .{self.__class__.__name__}
        # logger = logging.getLogger(f"{__name__}")
        logger.log(level, message)
        # print('Worker finished: %s' % name)
    except Exception:
        import sys, traceback
        print('Whoops! log_process Problem:', file=open("/home/pi/AreaFerrero/log/errlog.txt","a"))
        traceback.print_exc(file=open("/home/pi/AreaFerrero/log/errlog.txt","a"))

def main():
    try:
        worker_process(queue, worker_configurer)
        # logger = logging.getLogger()
        # logger.info('Hello')
        # logger.debug('Goodbye')
        queue.put_nowait(None)
        listener.join()
    except Exception:
        import sys, traceback
        print('Whoops! log_process Problem:', file=open("/home/pi/AreaFerrero/log/errlog.txt","a"))
        traceback.print_exc(file=open("/home/pi/AreaFerrero/log/errlog.txt","a"))

if __name__ == '__main__':
    queue = multiprocessing.Queue(-1)
    listener = multiprocessing.Process(target=listener_process,
                                       args=(queue, listener_configurer))
    listener.start()
    sys.exit(main())