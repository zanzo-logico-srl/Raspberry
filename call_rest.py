#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import urllib.parse
import json
from logger import multiprocessing, listener_process, listener_configurer, worker_configurer, log_process, logging


with open("config.json") as json_data_file:
    data = json.load(json_data_file)

url = data['api'] + '/api/Access'

headers = {"Content-Type": "application/json"}


def verify(userid, typo):
    # operation = "/%s/verify".format(code)
    operation = "/%s/verify" % urllib.parse.quote(userid)
    if typo == 'card':
        operation = "/%s/verifycard" % urllib.parse.quote(userid)

    try:
        # response = requests.get(url,timeout=3)
        log_process(logging.INFO, "request : " + url + operation)
        response = requests.request(
            'GET', url+operation, headers=headers, timeout=2)
        response.raise_for_status()  # Raise error in case of failure
    except requests.exceptions.HTTPError as httpErr:
        log_process(logging.ERROR, "Http Error:", exc_info=True)
    except requests.exceptions.ConnectionError as connErr:
        log_process(logging.ERROR, "Error Connecting:", exc_info=True)
    except requests.exceptions.Timeout as timeOutErr:
        log_process(logging.ERROR, "Timeout Error:", exc_info=True)
    except requests.exceptions.RequestException as reqErr:
        log_process(logging.ERROR, "Something Else:", exc_info=True)
    except requests.exceptions.ConnectionError as reqErr:
        log_process(logging.ERROR, "Connection Error:", exc_info=True)
    except Exception as e:
        log_process(logging.ERROR, "Oops!", exc_info=True)

    log_process(logging.INFO, "Status Code : " + str(response.status_code))  
    if response.status_code != 200:
        # return (False, "Errore Accesso", "", "0")
        return (False, '')

    # Update headers with clientid and token
    json_data = json.loads(response.text)
    # headers.update({"clientid":clientid})
    # headers.update({"token":token})
    json_formatted_str = json.dumps(json_data, indent=2)
    log_process(logging.INFO, json_formatted_str)
    # json_data["message1"], json_data["message2"])
    return (json_data["access"], json_data["accessId"])


def access(accessId):
    # Create a tag to store a boolean
    operation = "/%s/access" % urllib.parse.quote(accessId)
    # data = '''
    # {
    #     "path":"PiBit",
    #     "parameters": {
    #          "Value": {
    #              "DataType":"Discrete",
    #              "ParameterSource":"Value",
    #              "Value":"False"
    #          }
    #     }
    # }
    # '''
    # response = requests.request('POST', url+operation, data=data, headers=headers)

    try:
        # response = requests.get(url,timeout=3)
        log_process(logging.INFO, "request : " + url+operation)
        response = requests.request(
            'PUT', url+operation, headers=headers, timeout=2)
        response.raise_for_status()  # Raise error in case of failure
    except requests.exceptions.HTTPError as httpErr:
        log_process(logging.ERROR, "Http Error:", exc_info=True)
    except requests.exceptions.ConnectionError as connErr:
        log_process(logging.ERROR, "Error Connecting:", exc_info=True)
    except requests.exceptions.Timeout as timeOutErr:
        log_process(logging.ERROR, "Timeout Error:", exc_info=True)
    except requests.exceptions.RequestException as reqErr:
        log_process(logging.ERROR, "Something Else:", exc_info=True)
    except requests.exceptions.ConnectionError as reqErr:
        log_process(logging.ERROR, "Connection Error:", exc_info=True)
    except Exception as e:
        log_process(logging.ERROR, "Oops!", exc_info=True)

    if response.status_code != 200:
        # return (False, "Errore Accesso", "", "0")
        return False

    json_data = json.loads(response.text)
    json_formatted_str = json.dumps(json_data, indent=2)
    log_process(logging.INFO, "response-----------------------")
    log_process(logging.INFO, json_formatted_str)
    return True

# Define a function to toggle the state of PiBit
# (You will likely prefer to inject all dependencies in production code)
# def toggleBit(state):
#     data = '''{"path":"PiBit",
#                "parameters":{
#                    "Value":{
#                        "Value":"'''+str(not state)+'''"
#     }}}'''
#     requests.request('PUT', url+operation, data=data, headers=headers)
#     return not state

# read state of Boolean Tag
# def readBooleanTag(tagName):
#     querystring = {'path':tagName}
#     response = requests.request('GET', url+operation, params=querystring, headers=headers)
#     json_response = json.loads(response.text)
#     test = json_response[0]["value"]
#     return test == "True"

# Write a callback function to execute on event detection
# def callback(input_pin):
#     print("Input on pin",input_pin)
#     current_state = GPIO.input(40)
#     toggleBit(current_state)
#     GPIO.output(40, not current_state)

# if __name__ == '__main__':
#     valid, message1, message2, accessId = verify('google-oauth2|108786239037208379949', 'barcode')
#     if valid:
#         access(accessId)


if __name__ == "__main__":
    try:
        queue = multiprocessing.Queue(-1)
        listener = multiprocessing.Process(
            target=listener_process,
            args=(queue, listener_configurer))
        listener.start()
        # worker_configurer(queue)

    except KeyboardInterrupt:
        pass
