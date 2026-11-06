from flask import Flask, jsonify, request, render_template
import requests

app = Flask(__name__)

some_list = ["Kartoshkov", "Pureshkov", "Makaroshkov"]


@app.route("/")
def spravka():
    return "LOL"

@app.route("/privet/<imya>")
def say_hello(imya):
    return f"Здравствуйте, {imya}!"

@app.route("/kvadrat/<int:chislo>")
def square(chislo):
    result = chislo * chislo
    return f"{chislo} в квадрате будет = {result}"

@app.route("/spisok")
def get_the_list():
    return jsonify(some_list)

@app.route("/spisok/dlina")
def get_list_length():
    list_lenth = len(some_list)
    return str(list_lenth)

@app.route("/spisok/<int:nomer>")
def get_specific_list_data(nomer):    
    list_lenth = len(some_list)
    if nomer - 1 <= list_lenth and nomer - 1 > 0 and nomer - 1 != 0:
        return some_list[nomer - 1]
    else:
        return jsonify({"oshibka": "нет такого номера"}), 404
    
@app.route("/dobavit", methods=["POST"])
def add_new_surname():
    try:
        data = request.get_json()
        surname = data.get("surname")
        
        if not surname:            
            return jsonify({"oshibka": "Фамилия не указана"}), 400
        some_list.append(surname)
        return jsonify({"добавлено": surname}), 201
    
    except Exception:
        return jsonify({"oshibka": "JSON пустой"}), 400

"""def some_request():
    r = requests.post(
        "http://127.0.0.1:5000/dobavit",
        json={"surname": "Иванов"}
    )
    print(r.status_code)
    print(r.json())
    
some_request()"""

@app.route("/stranica")
def show_list():
    return render_template("spisok.html", spisok=some_list)

print(app.url_map)
if __name__ == "__main__":
    app.run(port=5000)
