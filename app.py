from registry import Registry
from flask import Flask, request, jsonify, render_template, redirect, url_for
from people import Student, Teacher, AnketaError
import requests

BASE = "http://127.0.0.1:5000/"

zhurnal = Registry()
if not zhurnal.load("ankety.txt"):
    print("ВНИМАНИЕ: файл не найден, журнал пуст")
else:
    print("Анкеты загружены.")
    

app = Flask(__name__)

def get_anketi():
    anketi = []

    for number, anketa in enumerate(zhurnal.accepted, start=1):
        anketi.append({"number": number, "fio": anketa.fio, "role": anketa.role(),
            "email": anketa.email, "phone": anketa.phone, "extra": anketa.extra()
        })

    return anketi

questionary_loaded = False

@app.route("/", methods = ["GET"])
#таблицу принятых анкет и строку «Принято / Отклонено»; ФИО — ссылка на страницу анкеты
def get_accepted_questionaries():
    anketi = get_anketi()
    return render_template("index.html", anketi = anketi, accepted_count=len(zhurnal.accepted),
                           rejected_count=len(zhurnal.errors))

@app.route("/anketa/<number>", methods = ["GET"])
#страницу одной анкеты со всеми полями; если номера нет — своя страница ошибки
def get_one_questionary(number):
    anketi = get_anketi()
    number = int(number) - 1
    current = anketi[number]
    return render_template("anketa.html", anketa = current)

@app.route("/gruppa/<name>", methods = ["GET"])
#тот же список, но только студентов этой группы
def get_students_by_group(name):
    spisok = []
    anketi = get_anketi()
    for person in anketi:
        if person["extra"] == name:
            spisok.append(person)
    return render_template("spisok.html", spisok = spisok, name = name)

@app.route("/statistika", methods = ["GET"])
#сводки по ролям и группам и список отклонённых строк
def get_statistics():
    anketi = get_anketi()    
    statistics_role = zhurnal.statistics_by_role()
    statistics_group = zhurnal.statistics_by_group()
    department_stats = {}
    erroneous_anketi = []

    for one in zhurnal.errors:
        parts = one.split(" | Error: ", 1)

        anketa_and_number = parts[0]
        error = parts[1] if len(parts) > 1 else ""

        erroneous_anketi.append({
            "raw": anketa_and_number,
            "reason": error
        })
        
    for person in zhurnal.accepted:
        if person.role() == "Teacher":
            department = person.extra()
            department_stats[department] = department_stats.get(department, 0) + 1
    
            
    return render_template("statistika.html", anketi = anketi, accepted_count=len(zhurnal.accepted), 
                           rejected_count=len(zhurnal.errors), role_stats = statistics_role, 
                           group_stats = statistics_group, department_stats = department_stats,
                           rejected = erroneous_anketi)

@app.route("/dobavit", methods=["GET"])
def get_questionary_form():
    form_data = {
        "role": "", "fio": "", "email": "", "phone": "", "extra": ""
    }

    return render_template("dobavit.html", form_data=form_data)

@app.route("/dobavit", methods=["POST"])
def post_questionary_form():

    form_data = request.form.to_dict()
    try:
        role = form_data.get("role")
        fio = form_data.get("fio", "")
        email = form_data.get("email", "")
        phone = form_data.get("phone", "")
        extra = form_data.get("extra", "")
        
        if role == "student":
            person = Student(fio, email, phone, extra)
        elif role == "teacher":
            person = Teacher(fio, email, phone, extra)
        else:
            raise AnketaError("Необходимо выбрать тип анкеты")

        zhurnal.add(person)
        number = len(zhurnal.accepted)

        return redirect(url_for("get_one_questionary", number=number))

    except AnketaError as e:
        return render_template("dobavit.html", error=str(e),form_data=form_data), 400
        
        
@app.route("/api/anketi", methods = ["GET"])
#все анкеты; с параметром ?rol=студент — только их
def get_api_all_students():
    anketi = get_anketi()
    role = request.args.get("rol", "").strip().lower()
    if role:
        if role in ("студент", "student"):
            role = "student"
        elif role in ("преподаватель", "teacher"):
            role = "teacher"
        anketi = [
            person for person in anketi
            if person["role"].lower() == role]
    return jsonify(anketi)

@app.route("/api/anketa/<number>", methods = ["GET"])
#одну анкету; если номера нет — код 404
def get_api_student(number):
    anketi = get_anketi()
    if number < 1 or number > len(anketi):
        return jsonify({"error": "Анкета не найдена"}), 404
    return jsonify(anketi[number - 1])

@app.route("/api/statistika", methods = ["GET"])
#сколько принято и отклонено, сводки по ролям и группам
def get_api_statistics():
    statistics = {
        "accepted_count": len(zhurnal.accepted),
        "rejected_count": len(zhurnal.errors),
        "roles": zhurnal.statistics_by_role(),
        "groups": zhurnal.statistics_by_group()
    }
    return jsonify(statistics)

@app.route("/api/brak", methods = ["GET"])
#отклонённые строки: номер, текст, причина
def get_api_errors():
    errors = []
    for one in zhurnal.errors:
        parts = one.split(" | Error: ", 1)
        line_info = parts[0]
        reason = parts[1] if len(parts) > 1 else ""
        number, raw = line_info.split(": ", 1)
        errors.append({"number": number.replace("Строка ", ""), "raw": raw, "reason": reason})
    return jsonify(errors)

@app.route("/api/anketa", methods = ["POST"])
#принимает анкету в JSON, отвечает кодом 201
def post_api_anketi():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Ожидается JSON-объект"}), 400
    role = data.get("role")
    fio = data.get("fio", "")
    email = data.get("email", "")
    phone = data.get("phone", "")
    extra = data.get("extra", "")
    try:
        if role == "student":
            person = Student(fio, email, phone, extra)
        elif role == "teacher":
            person = Teacher(fio, email, phone, extra)
        else:
            return jsonify({"error": "Неизвестный тип анкеты"}), 400
        zhurnal.add(person)
        return jsonify({"message": "Анкета успешно добавлена", "number": len(zhurnal), "fio": person.fio,
                        "role": person.role()}), 201
    except AnketaError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(port=5000, debug=True)
