import pytest
import people
from people import Person

"""ФИО приводится к одному виду"""
"""parametrize, не меньше четырёх наборов: разный регистр, лишние пробелы"""

@pytest.mark.parametrize("input_fio, expected_fio", [
    ("иванов иван иванович", "Иванов И.И."),
    ("ИВАНОВ ИВАН ИВАНОВИЧ", "Иванов И.И."),
    ("  иванов   иван   иванович  ", "Иванов И.И."),
    ("Петров ПЁТР Сергеевич", "Петров П.С."),
])
def test_short_fio(input_fio, expected_fio):
    person = Person(input_fio, "test@example.com", "71234567890")
    assert person.short_fio() == expected_fio
    
"""ФИО из одного слова отклоняется"""

@pytest.mark.parametrize("input_fio", [
    "Иванов",
    "Петров",
    "Сидоров",
])
def test_one_word(input_fio):
    with pytest.raises(people.AnketaError):
        person = Person(input_fio, "test@example.com", "71234567890")
        
"""Почта приводится к нижнему регистру
parametrize, не меньше двух наборов"""

@pytest.mark.parametrize("input_email, expected_email", [
    ("TEST@EXAMPLE.COM", "test@example.com"),
    ("Test@Example.com", "test@example.com"),
])
def test_email_lower(input_email, expected_email):
    person = Person("Иванов Иван Иванович", input_email, "71234567890")
    assert person.email == expected_email
    
"""Плохая почта отклоняется
parametrize + pytest.raises, не меньше четырёх видов брака"""

@pytest.mark.parametrize("input_email", [
    "testexample.com",
    "test@.com",
    "test@example",
    "@example.com", 
])

def test_bad_email(input_email):
    with pytest.raises(people.AnketaError):
        person = Person("Иванов Иван Иванович", input_email, "71234567890")
        
"""Телефон приводится к одному виду
parametrize: все четыре записи дают один результат"""

@pytest.mark.parametrize("input_phone, expected_phone", [
    ("8 (123) 456-78-90", "+7 (123) ***-**-90"),
    ("+7 123 456 78 90", "+7 (123) ***-**-90"),
    ("71234567890", "+7 (123) ***-**-90"),
    ("7-123-456-78-90", "+7 (123) ***-**-90"),
])

def test_phone_numbers(input_phone, expected_phone):
    person = Person("Иванов Иван Иванович", "lololo@mail.ru", input_phone)
    assert person.masked_phone() == expected_phone
    
    
"""Плохой телефон отклоняется
parametrize + pytest.raises"""

@pytest.mark.parametrize("input_phone", [
    "7123890",
    "8 (123) 456-78-9",
    "+7 123 456 78 901",
    "79123456789",
])
def test_bad_phone(input_phone):
    with pytest.raises(people.AnketaError):
        person = Person("Иванов Иван Иванович", "test@example.com", input_phone)

"""Студент и преподаватель отвечают по-разному"""

@pytest.mark.parametrize("fio, email, expected_role, extra_value", [
    ("Иванов Иван Иванович", "test@example.com", "Student", "Группа 101"),
    ("Петров Петр Петрович", "test@example.com", "Teacher", "Кафедра Математики"),
])

def test_student_teacher_roles(fio, email, expected_role, extra_value):
    if expected_role == "Student":
        person = people.Student(fio, email, "71234567890", group=extra_value)
    elif expected_role == "Teacher":
        person = people.Teacher(fio, email, "71234567890", department=extra_value)
    assert person.role() == expected_role
    assert person.extra() == extra_value
    
"""Студент без группы отклоняется
pytest.raises"""

def test_student_without_group():
    with pytest.raises(people.AnketaError):
        student = people.Student("Иванов Иван Иванович", "test@example.com", "71234567890", "")
        
"""Строка файла разбирается верно
два теста: студент и преподаватель, с проверкой типа"""

def test_student_parsing():
    line = "s;Иванов Иван Иванович;test@example.com;71234567890;Группа 101"
    person = people.parse_person(line)
    assert isinstance(person, people.Student)
    assert person.group == "Группа 101"

def test_teacher_parsing():
    line = "t;Петров Петр Петрович;test@example.com;71234567890;Кафедра Математики"
    person = people.parse_person(line)
    assert isinstance(person, people.Teacher)
    assert person.department == "Кафедра Математики"
    
"""Плохая строка отклоняется
parametrize: неизвестный тип, мало полей, пустая строка"""

@pytest.mark.parametrize("line", [
    "x;Иванов Иван Иванович;test@example.com;71234567890;Группа 101",
    "s;Иванов Иван Иванович;test@example.com;71234567890",
    "",
])
def test_bad_line(line):
    with pytest.raises(people.AnketaError):
        person = people.parse_person(line)