import requests
import json

BASE = "http://127.0.0.1:5000"

"""Запросите адрес / и напечатайте три вещи: код ответа, тип значения r.text и тип значения r.json().
Затем напечатайте из ответа название сервиса.
В отчёте объясните одной строкой, почему типы разные.
"""


r = requests.get("http://127.0.0.1:5000/")

def some_request():
    print("Адрес:", r.url)
    print("Тип значения:", r.text)
    print("Тип значения:", r.json())

"""Заберите все анкеты и напечатайте, сколько их пришло и ФИО первой.
Подсказка: r.json() вернёт список словарей, работайте с ним как с обычным списком.
"""

request = requests.get("http://127.0.0.1:5000/anketi")

def show_all_anketi():
    count = 0;
    for surname in request.json():
        count+=1    
    print("Всего анкет:", count)
    print("Фамилия первого типа:", request.json()[0]["fio"])

"""Задача H3. Анкеты нет
Запросите анкету с номером 99 — такой на сервере нет.
Напечатайте код ответа и значение r.ok. Убедитесь, что программа при этом не упала и исключения не было.
Затем напечатайте текст ошибки, который прислал сервер.
В отчёте ответьте: почему requests не считает код 404 поводом для исключения?
"""

def request_number_99():
    
    req_99 = requests.get("http://127.0.0.1:5000/anketi/99")

    print("Код:", req_99.status_code)
    print("Статус:", req_99.ok)
    print("Ошибка:", req_99.json())
    

"""Заберите анкеты преподавателей, передав параметр через именованный аргумент params. 
Склеивать адрес вручную нельзя.
Напечатайте получившийся адрес запроса (r.url), а затем ФИО и кафедру каждого преподавателя.
"""

def get_teachers():    
    req = requests.get("http://127.0.0.1:5000/anketi", params= {"tip": "t"})
    print("Адрес запроса:", req.url)
    teacher_index = 0
    for teacher in req.json():
        print("Преподаватель: ", req.json()[teacher_index]["fio"])
        print("Кафедра: ", req.json()[teacher_index]["kafedra"])
        teacher_index+=1


"""Отправьте методом POST на адрес /proverka две почты по очереди: 
ivanov@mail.ru и kuznetsov.mail.ru.
r = requests.post(BASE + "/proverka", json={"mail": mail})
Для каждой напечатайте саму почту, код ответа и то, что ответил сервер в поле prinyato.
В отчёте объясните, почему коды ответа у двух запросов разные.
"""

def post_mail():
    
    mails = { "ivanov@mail.ru", "kuznetsov.mail.ru"}
    
    for mail in mails:
        r = requests.post(BASE + "/proverka", json={"mail": mail})
        print("Почта:", mail)
        print("Код ответа:", r.status_code)
        print("Prinyato:", r.json()["prinyato"])

    