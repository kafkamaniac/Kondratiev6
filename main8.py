import json
import requests
import client
import server
import people
from pathlib import Path

url = "http://127.0.0.1:5000"
file_path = Path("ankety.txt")
source = None
all_questionaries = []
lines = []

try:
    all_questionaries = client.get_all_questionaries("http://127.0.0.1:5000/anketi")
    source = "server"
    print("Данные получены с сервера.")
    
except client.ServerNedostupen as error:
    print(f"Сервер недоступен. Причина: {error}")
    print("Пробуем использовать резервный файл anketa.txt...")

    if file_path.is_file():
        lines = file_path.read_text(encoding="utf-8").splitlines()

        if lines and any(line.strip() for line in lines):
            source = "file"
            print("Данные получены из файла anketa.txt.")
            
if source is None:
    print("Нет доступных источников данных. Программа завершена.")
    raise SystemExit

every_student_and_teacher = []
list_of_errors = []

if source == "server":
    for questionary in all_questionaries:
        try:
            if questionary["tip"] == "s":
                new_student = people.Student(fio = questionary["fio"], email = questionary["mail"], 
                                            phone = questionary["phone"], group = questionary["gruppa"])
                every_student_and_teacher.append(new_student)
        
            elif questionary["tip"] == "t":
                new_teacher = people.Teacher(fio = questionary["fio"], email = questionary["mail"], 
                                            phone = questionary["phone"], department = questionary["kafedra"])
                every_student_and_teacher.append(new_teacher)
            else:
                print("Неизвестный тип анкеты:", questionary)
        except people.AnketaError as error:
            list_of_errors.append((questionary, error))
            
elif source == "file":
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            person = people.parse_person(line)
            every_student_and_teacher.append(person)
        except people.AnketaError as error:
            list_of_errors.append((number, error))        
        
print("Принято:", len(every_student_and_teacher), 
      "| Отклонено:", len(list_of_errors))

print("\nПринятые анкеты:")
for every_item in every_student_and_teacher:
    print(every_item)

print("\nБраки:")
for questionary, error in list_of_errors:
    if source == "server":
        print(f"Анкета №{questionary['nomer']}: {error}")
    else:
        print(f"Строка №{questionary}: {error}")
    
print("\nСводка по ролям:")
student_count = 0
teacher_count = 0
for person in every_student_and_teacher:
    if person.role() == "Student":
        student_count += 1
    elif person.role() == "Teacher":
        teacher_count += 1
        
print("Учителя:", teacher_count, 
      "| Студенты:", student_count)

stats = None
mail_results = []

if source == "server":
    print("\nСтатистика у сервера:")
    try:
        stats = client.get_statistics(url)
        print(stats)
    except client.ServerNedostupen as error:
        print(f"Не удалось получить статистику: {error}")

    print("\nОтчёт по почтам:")
    for person in every_student_and_teacher:
        try:
            result = client.send_mail_to_proverka(url, person.email)
            mail_results.append({
                "email": person.email,
                "result": result
            })
            print(result)
        except client.ServerNedostupen as error:
            print(f"Сервер стал недоступен: {error}")
            break

else:
    print("\nСтатистика сервера недоступна.")
    print("Проверка почты пропущена: используется резервный файл.")
    
"""JSON"""

report = {
    "accepted_count": len(every_student_and_teacher),
    "rejected_count": len(list_of_errors),

    "accepted": [
        {
            "fio": person.fio,
            "email": person.email,
            "phone": person.phone,
            "role": person.role(),
            "extra": person.extra()
        }
        for person in every_student_and_teacher
    ],

    "rejected": [
        {
            "questionary": questionary,
            "error": str(error)
        }
        for questionary, error in list_of_errors
    ],

    "roles": {
        "students": student_count,
        "teachers": teacher_count
    },

    "data_source": source,
    "server_statistics": stats,
    "mail_results": mail_results
}

with open("otchet.json", "w", encoding="utf-8") as file:
    json.dump(report, file, ensure_ascii=False, indent=4)

print("\nОтчёт сохранён в otchet.json")