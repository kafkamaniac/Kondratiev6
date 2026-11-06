from flask import Flask, jsonify, request
import requests
import json

BASE = "http://127.0.0.1:5000"

class ServerNedostupen(Exception):    
    """Сервер недоступен."""
    pass

def process_request(url, method="GET", **kwargs):
    try:
        req = requests.request(method, url, timeout=5, **kwargs)
        status_code = req.status_code
        if (status_code >= 500):
            raise ServerNedostupen("Сервер недоступен!")
        return req
    except requests.exceptions.ConnectionError:
        raise ServerNedostupen("Не удалось подключиться к серверу")
    except requests.exceptions.Timeout:
         raise ServerNedostupen("Время истекло")

def get_all_questionaries(url):
    req = process_request(url)
    py_object = req.json()
    return py_object
        
def get_one_questionary(url, number):
    req = process_request(url)
    py_object = req.json()
    for item in py_object:
        if item["nomer"] == number:
            return item
    return None
    
def send_mail_to_proverka(url, mail):
    req = process_request(url + "/proverka", method="POST", json={"mail": mail})
    return req.json()

def get_statistics(url):
    req = process_request(url + "/statistika")
    return req.json()

