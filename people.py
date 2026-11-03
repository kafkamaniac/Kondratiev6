MIN_FIO_PARTS = 2
MIN_PHONE_LENGTH = 10


"""Класс Person
— Поля: ФИО, почта, телефон.
— __init__ принимает их в сыром виде, приводит в порядок и проверяет.
— При плохих данных бросает AnketaError с понятной причиной. Объект при этом не создаётся.
— Проверки оформлены как @staticmethod: им не нужен объект.
— Методы masked_phone() и short_fio() — как в прошлой работе, только теперь берут данные у себя.
— Методы role() и extra() в базовом классе возвращают заглушку — их переопределят наследники.
— __str__ и __lt__: сортировка по ФИО."""

class Person:
    def __init__(self, fio, email, phone):
        self.fio = fio
        self.email = email
        self.phone = phone

    @staticmethod
    def validate_fio(fio):
        # Проверка ФИО
        if not isinstance(fio, str) or len(fio.split()) < MIN_FIO_PARTS:
            raise AnketaError("ФИО должно содержать как минимум фамилию и имя.")

    @staticmethod
    def validate_email(email):
        # Проверка почты
        if "@" not in email:
            raise AnketaError("Некорректный формат почты.")

    @staticmethod
    def validate_phone(phone):
        if not isinstance(phone, str) or not phone.isdigit() or len(phone) < MIN_PHONE_LENGTH:
            raise AnketaError("Телефон должен содержать только цифры и быть не менее 10 символов.")

    def masked_phone(self):
        return f"{self.phone[:3]}****{self.phone[-2:]}"

    def short_fio(self):
        parts = self.fio.split()
        surname = parts[0]
        initials = "".join([word[0] + "." for word in parts[1:]])
        return f"{surname} {initials}"

    def role(self):
        return "Person"

    def extra(self):
        return ""

    def __str__(self):
        return f"{self.fio}, {self.email}, {self.masked_phone()}, {self.extra()}"

    def __lt__(self, other):
        return self.fio < other.fio

class AnketaError(Exception):
    pass
    
"""Классы Student и Teacher
— Оба наследуются от Person.
— __init__ вызывает super().__init__ для общей части, затем добавляет своё поле.
— Student добавляет группу, Teacher — кафедру. Пустое значение — AnketaError.
— Оба переопределяют role() и extra().
— Проверки почты и телефона в них не повторяются."""

class Student(Person):
    def __init__(self, fio, email, phone, group):
        super().__init__(fio, email, phone)

        if not group:
            raise AnketaError("Группа не может быть пустой.")

        self.group = group


    def role(self):
        return "Student"

    def extra(self):
        return f"Group: {self.group}"
    
class Teacher(Person):
    def __init__(self, fio, email, phone, department):
        super().__init__(fio, email, phone)
        if not department:
            raise AnketaError("Кафедра не может быть пустой.")
        self.department = department

    def role(self):
        return "Teacher"

    def extra(self):
        return f"Department: {self.department}"