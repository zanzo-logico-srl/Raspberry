#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
from os import path
import time
import json
import subprocess
# from jinja2 import Undefined
from call_rgbled import color, valid
from bottle import route, run, response, request, json_dumps, hook
from logger import multiprocessing, listener_process, listener_configurer, worker_configurer, log_process, logging
from open_rele import greenled


@hook('after_request')
def enable_cors():
    '''Add headers to enable CORS'''
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@route('/rpi', methods=['GET'])
def rpi():
    response.content_type = 'text/html; charset=utf-8'
    response.status = 200
    with open("index.html", "r") as myfile:
        return myfile.readlines()


@route('/log/<message>', methods=['GET'])
def log(message):
    # request.fullpath
    log_process(logging.INFO, request.fullpath)
    log_process(logging.INFO, request.json)
    return {"status": "OK", "message": "logged"}


@route('/log', methods=['POST'])
def log():
    log_process(logging.INFO, request.fullpath)
    log_process(logging.INFO, request.json)
    return {"status": "OK", "message": "logged"}


@route('/reboot', method=['OPTIONS', 'POST'])
def index():
    log_process(logging.INFO, request.fullpath)
    response.content_type = 'application/json; charset=utf-8'
    response.status = 200
    subprocess.Popen(['sudo', 'shutdown', '-r', 'now'])
    return json_dumps({"status": "OK", "message": "reboot started"})


@route('/openvpn', method=['OPTIONS', 'POST'])
def openvpn():
    log_process(logging.INFO, request.fullpath)
    response.content_type = 'application/json; charset=utf-8'
    response.status = 200
    subprocess.Popen(['sudo', 'openvpn', 'raspberryareaferrero.ovpn'], cwd="/home/pi/AreaFerrero/vpn")
    return json_dumps({"status": "OK", "message": "vpn opened"})
    #
    # Esporta in un file pem temporaneo
    # openssl pkcs12 -in protected.p12 -nodes -out temp.pem
    # #  -> Enter password
    # Converti pem in p12
    # openssl pkcs12 -export -in temp.pem  -out unprotected.p12
    # # -> Just press [return] twice for no password
    # Rimuovi certificato temporaneo
    # rm temp.pem

    # ------------------------------------------------------------
    # Può essere raggiunto con varie opensslchiamate.

    # PASSWORD è la tua password attuale
    # YourPKCSFile è il file che vuoi convertire
    # NewPKCSWithoutPassphraseFile è il file di destinazione per PKCS12 senza passphrase
    # Innanzitutto, estrai il certificato:

    # $ openssl pkcs12 -clcerts -nokeys -in "YourPKCSFile" \
    #       -out certificate.crt -password pass:PASSWORD -passin pass:PASSWORD
    # In secondo luogo, la chiave CA:

    # $ openssl pkcs12 -cacerts -nokeys -in "YourPKCSFile" \
    #       -out ca-cert.ca -password pass:PASSWORD -passin pass:PASSWORD
    # Ora, la chiave privata:

    # $ openssl pkcs12 -nocerts -in "YourPKCSFile" \
    #       -out private.key -password pass:PASSWORD -passin pass:PASSWORD \
    #       -passout pass:TemporaryPassword
    # Ora rimuovi la passphrase:

    # $ openssl rsa -in private.key -out "NewKeyFile.key" \
    #       -passin pass:TemporaryPassword
    # Metti insieme le cose per il nuovo file PKCS:

    # $ cat "NewKeyFile.key"  \
    #       "certificate.crt" \
    #       "ca-cert.ca" > PEM.pem
    # E crea il nuovo file:

    # $ openssl pkcs12 -export -nodes -CAfile ca-cert.ca \
    #       -in PEM.pem -out "NewPKCSWithoutPassphraseFile"
    # Ora hai un nuovo file di chiavi PKCS12 senza passphrase nella parte della chiave privata.


@route('/open', method=['OPTIONS', 'POST'])
def index():
    log_process(logging.INFO, request.fullpath)
    log_process(logging.INFO, request.json)
    asyncio.run(color(0x4040ff, 1))
    asyncio.run(valid())
    response.content_type = 'application/json; charset=utf-8'
    response.status = 200
    return json_dumps({"status": "OK", "message": "open gate"})


@route('/changeapi', method=['OPTIONS', 'GET', 'POST'])
def changeapi():
    log_process(logging.INFO, request.fullpath)
    log_process(logging.INFO, request.json)
    if request.method == 'GET':
        log_process(logging.INFO, "GET NOT ALLOWED")
        response.status = 405
        return {}
    if request.method == 'OPTIONS':
        return {}
    if request.method == 'POST':
        req = request.json
        with open("config.json") as json_data_file:
            data = json.load(json_data_file)
        log_process(logging.INFO, data)
        data['api'] = req['api']
        with open("config.json", "w") as outfile:
            json.dump(data, outfile)

    response.content_type = 'application/json; charset=utf-8'
    response.status = 200
    return json_dumps({"status": "OK", "message": "config saved"})


@route('/test', method=['OPTIONS', 'GET', 'POST'])
def test():
    log_process(logging.INFO, request.fullpath)
    log_process(logging.INFO, request.method)
    response.content_type = 'application/json; charset=utf-8'
    _ = asyncio.run(greenled())
    response.status = 200
    return json_dumps({"status": "OK", "message": "Raspberry varco UP!"})


@route('/access', method=['OPTIONS', 'GET', 'POST'])
def access():
    log_process(logging.INFO, request.fullpath)
    client_ip = request.environ.get('REMOTE_ADDR')
    log_process(logging.INFO, "Call api /access from ip {0}".format(client_ip))
    sub = ''
    # ip = ''
    # roomid = ''
    if request.method == 'GET':
        log_process(logging.INFO, "GET NOT ALLOWED")
        response.status = 405
        return {}
    if request.method == 'OPTIONS':
        return {}
    if request.method == 'POST':
        data = request.json
        log_process(logging.INFO, data)
        sub = data['sub']
        # ip = data['ip']
        # roomid = data['roomid']
    response.content_type = 'application/json; charset=utf-8'
    response.status = 200
    asyncio.run(valid())
    xday = time.strftime("%a %d-%m-%Y")
    xtime = time.strftime("%H:%M")
    return json_dumps({"status": "OK", "message": "il giorno {1} alle {2} è stato autorizzato accesso di {0}".format(sub, xday, xtime)})


if __name__ == "__main__":
    try:
        queue = multiprocessing.Queue(-1)
        listener = multiprocessing.Process(
            target=listener_process,
            args=(queue, listener_configurer))
        listener.start()
        worker_configurer(queue)

        port = 4443

        # HTTP
        run(host='0.0.0.0', port=port)

        # HTTPS
        # os.system(
        #     "openssl req -nodes -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -subj '/CN=raspberrypi'")
        # httpd = HTTPServer(('0.0.0.0', port), ZSimpleHTTPRequestHandler)
        # httpd.socket = ssl.wrap_socket(
        #     httpd.socket, keyfile='private.key', certfile="certificate.crt", server_side=True)
        # print(f"Server running on https://0.0.0.0:{port}")
        # httpd.serve_forever()

    except KeyboardInterrupt:
        pass
