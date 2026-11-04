"""Для тестов журнала понадобится файл с анкетами — его готовит фикстура, а не вы руками.
Фикстура должна: создать временный файл, положить в него три верные строки и три бракованные, 
создать журнал, загрузить файл и вернуть журнал."""

import pytest
from registry import Registry 
import people

@pytest.fixture
def fayl_s_anketami(tmp_path):
    file_path = tmp_path / "ankets1.txt"

    file_path.write_text(
        "s;Петров Иван Иванович;ivanov@mail.ru;71234567890;Группа 101\n"
        "t;Иванов Петр Петрович;petrov@mail.ru;71234567891;Кафедра Математики\n"
        "s;Сидоров Сидор Сидорович;sidorov@mail.ru;71234567892;Группа 102\n"
        "s;Иванов;badmail;123;Группа 103\n"
        "t;Петров Петр;badmail;123;Кафедра Физики\n"
        "s;Сидоров Сидор Сидорович;sidorov@mail.ru;123;Группа 104\n",
        encoding="utf-8"
    )

    registry = Registry()
    registry.load(file_path)

    return registry

def test_empty_registry():
    registry = Registry()
    assert len(registry) == 0

def test_three_lines(fayl_s_anketami):
    assert len(fayl_s_anketami) == 3
    
def test_three_errors(fayl_s_anketami):
    assert len(fayl_s_anketami.errors) == 3
    
    """У брака правильные номера строк"""
    
def test_right_line_numbers(fayl_s_anketami):
    assert fayl_s_anketami.errors[0].startswith("Строка 4:")
    assert fayl_s_anketami.errors[1].startswith("Строка 5:")
    assert fayl_s_anketami.errors[2].startswith("Строка 6:")
    
def test_file_doesnt_exist(fayl_s_anketami):
    registry = Registry()
    result = registry.load("nonexistent_file.txt")

    assert result is False
    
def test_statistics_by_role(fayl_s_anketami):
    stats = fayl_s_anketami.statistics_by_role()
    assert stats == {"Student": 2, "Teacher": 1}
    
"""Тест 7. счётчик групп считает только студентов;"""
    
def test_count_only_students(fayl_s_anketami):
    stats = fayl_s_anketami.statistics_by_group()
    assert stats == {"Группа 101": 1, "Группа 102": 1}

"""Тест 8. журнал перебирается циклом for;"""

def test_registry_for(fayl_s_anketami):
    count = 0
    for person in fayl_s_anketami:
        count += 1
    assert count == 3
    
    
""""""

def test_sort_by_alphabet(fayl_s_anketami):
    sorted_people = sorted(fayl_s_anketami.accepted)
    surnames = [person.fio.split()[0] for person in sorted_people]
    assert surnames == ["Иванов", "Петров", "Сидоров"]
    
"""Тест 10. save_ok пишет по строке на человека;"""

def test_save_ok(fayl_s_anketami):
    fayl_s_anketami.save_ok()

    with open("ok.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    assert len(lines) == 3
    
""". save_errors пишет причину отказа."""

def test_save_errors(fayl_s_anketami):
    fayl_s_anketami.save_errors()
    with open("errors.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        
    assert len(lines) == 3
    
    
""""""""""""""

def test_double_surname():
    person = people.Person(
        "петров-водкин кузьма",
        "test@example.com",
        "71234567890"
    )
    assert person.fio == "Петров-Водкин Кузьма"
    
def test_backspace_inside():
    test_email = "iv anov@mail.ru"
    test_email = test_email.replace(" ", "")
    person = people.Person("Иван Иванов Анович", test_email, "71234567890")

    person.validate_email(test_email)
    
def test_sort_with_yo():
    registry = Registry()

    registry.add(people.Person("Яковлев Иван", "yakovlev@mail.ru", "71234567890"))
    registry.add(people.Person("Ёлкин Петр", "elkin@mail.ru", "71234567891"))
    registry.add(people.Person("Абрамов Сергей", "abramov@mail.ru", "71234567892"))

    sorted_people = sorted(registry)
    surnames = [person.fio.split()[0] for person in sorted_people]

    assert surnames == ["Абрамов", "Ёлкин", "Яковлев"]  
    