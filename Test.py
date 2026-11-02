class Student:
    def __init__(self, fio, group):
        self.fio = fio
        self.group = group

    def short(self):
        parts = self.fio.split()

        surname = parts[0]
        initials = ""

        for word in parts[1:]:
            initials += word[0] + "."

        initials = initials.strip()

        return surname + " " + initials

def show_students():
    student1 = Student("Иванов Иван Петрович", "09с33")
    student2 = Student("Петрова Анна", "09с34")


    print(student1.short(), "|", student1.group)
    print()

    print(student2.short(), "|", student2.group)


"""Написать класс-счётчик с именем и значением.
— __init__ принимает имя, значение изначально равно нулю.
— Метод add(n) увеличивает значение на n; по умолчанию на единицу.
— Метод reset() обнуляет значение.
— __str__ возвращает строку вида «принято: 7».
— Создать два счётчика и показать, что они не мешают друг другу."""


class Counter:
    def __init__(self, name):
        self.name = name
        self.value = 0

    def add(self, n=1):
        self.value += n

    def reset(self):
        self.value = 0

    def __str__(self):
        return f"{self.name}: {self.value}"

def show_counters():
    counter1 = Counter("принято")
    counter2 = Counter("отклонено")

    counter1.add(7)
    counter2.add()

    print(counter1)
    print(counter2)

    counter1.reset()
    print("после сброса:", counter1)

    """_summary_
    Написать класс для температуры с хранением в градусах Цельсия.
— __init__ принимает температуру в Цельсиях.
— Свойство fahrenheit считает значение в Фаренгейтах по формуле C × 9 / 5 + 32. Это именно @property, а не метод: обращение без скобок.
— __str__ выводит обе величины с одним знаком после точки.
— __lt__ сравнивает объекты по Цельсиям.
— Создать список из трёх температур, отсортировать его через sorted и найти максимум через max.
    """
    
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @property
    def fahrenheit(self):
        return self.celsius * 9 / 5 + 32

    def __str__(self):
        return f"{self.celsius:.1f} C = {self.fahrenheit:.1f} F"

    def __lt__(self, other):
        return self.celsius < other.celsius
    
def show_temperatures():
    temp1 = Temperature(21.5)
    temp2 = Temperature(-3.0)
    temp3 = Temperature(20)

    temperatures = [temp1, temp2, temp3]

    sorted_temps = sorted(temperatures)
    max_temp = max(temperatures)

    print("Отсортированные температуры:")
    for temp in sorted_temps:
        print(temp)

    print("Максимальная температура:")
    print(max_temp)
    
"""Написать базовый класс Figure и двух наследников.
— У Figure есть поле name и метод area(), возвращающий ноль.
— __str__ выводит название и площадь с двумя знаками после точки.
— Rect принимает ширину и высоту, Circle — радиус; оба вызывают super().__init__ и переопределяют area().
— Создать список из разных фигур, напечатать каждую и посчитать общую площадь одним циклом.
— В цикле не должно быть проверок типа фигуры."""

class Figure:
    def __init__(self, name):
        self.name = name
    def area(self):
        return 0
    def __str__(self):
        return f"{self.name}: {self.area():.2f}"

class Rect(Figure):
    def __init__(self, width, height):
        super().__init__("Прямоугольник")
        self.width = width
        self.height = height
    def area(self):
        return self.width * self.height

class Circle(Figure):
    def __init__(self, radius):
        super().__init__("Круг")
        self.radius = radius
    def area(self):
        return 3.14159 * self.radius ** 2


def show_figures():
    rect = Rect(4, 3)
    circle = Circle(2)
    rect2 = Rect(5, 3)
    figures = [rect, circle, rect2]
    total_area = 0
    
    for figure in figures:
        print(figure)
        total_area += figure.area()

    print(f"Общая площадь: {total_area:.2f}")
    
"""Написать своё исключение AgeError и класс Person, который его бросает.
— AgeError наследуется от Exception.
— __init__ класса Person проверяет возраст: допустимо от 0 до 120.
— При недопустимом возрасте бросается AgeError с понятным текстом; объект при этом не создаётся.
— В основной части программы задан список из трёх-четырёх человек, среди них есть неправильные.
— Правильные собираются в список, про неправильных печатается причина, программа не падает."""

class Person:
    def __init__(self, name, age):
        if age < 0 or age > 120:
            raise AgeError(f"Возраст {age} вне границ (0-120)")
        self.name = name
        self.age = age
        
class AgeError(Exception):
    pass

def create_people():
    people_data = [
        ("Иванов Иван", 19),
        ("Пупкина Мария", -5),
        ("Сидоров Пётр", 200),
        ("Петрова Анна", 30)
    ]

    valid_people = []

    for name, age in people_data:
        try:
            person = Person(name, age)
            valid_people.append(person)
        except AgeError as e:
            print(f"Не принято: {name} - {e}")

    print("Принято: {valid_people_count}".format(valid_people_count=len(valid_people)))
    for person in valid_people:
        print(f"{person.name}, возраст: {person.age}")
