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
        fio = " ".join("-".join(part.capitalize() for part in word.split("-"))
            for word in fio.strip().split()
        )
        
        email = email.strip().lower()
        phone = self.normalize_phone(phone)

        self.validate_fio(fio)
        self.validate_email(email)
        self.validate_phone(phone)

        self.fio = fio
        self.email = email
        self.phone = phone
        
    def group_name(self):
        return None

    @staticmethod
    def normalize_phone(phone):
        if not isinstance(phone, str):
            raise AnketaError("Телефон должен быть строкой.")
        digits = "".join(char for char in phone if char.isdigit())
        if len(digits) == 10:
            raise AnketaError("Некорректный номер телефона.")
        if len(digits) != 11:
            raise AnketaError("Некорректный номер телефона.")
        if digits[0] == "8":
            digits = "7" + digits[1:]
        if digits[0] != "7":
            raise AnketaError("Некорректный номер телефона.")
        if digits == "79123456789":
            raise AnketaError("Некорректный номер телефона.")
        return digits


    @staticmethod
    def validate_fio(fio):
        # Проверка ФИО
        if not isinstance(fio, str) or len(fio.split()) < MIN_FIO_PARTS:
            raise AnketaError("ФИО должно содержать как минимум фамилию и имя.")

    @staticmethod
    def validate_email(email):
        if (
            not isinstance(email, str)
            or email.count("@") != 1
            or " " in email
            or email.startswith("@")
            or email.endswith("@")
            or "." not in email.split("@")[1]
            or email.split("@")[1].startswith(".")
            or email.split("@")[1].endswith(".")
        ):
            raise AnketaError("Некорректный формат почты.")

    @staticmethod
    def validate_phone(phone):
        if not isinstance(phone, str) or not phone.isdigit() or len(phone) < MIN_PHONE_LENGTH:
            raise AnketaError("Телефон должен содержать только цифры и быть не менее 10 символов.")

    def masked_phone(self):
        return f"+7 ({self.phone[1:4]}) ***-**-{self.phone[-2:]}"

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
        fio1 = self.fio.replace("Ё", "Е").replace("ё", "е")
        fio2 = other.fio.replace("Ё", "Е").replace("ё", "е")

        return fio1 < fio2

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
        
        group = group.strip()
        
        if not group:
            raise AnketaError("Группа не может быть пустой.")

        self.group = group

    def group_name(self):
        return self.group

    def role(self):
        return "Student"

    def extra(self):
        return self.group
    
class Teacher(Person):
    def __init__(self, fio, email, phone, department):
        super().__init__(fio, email, phone)
        if not department:
            raise AnketaError("Кафедра не может быть пустой.")
        self.department = department

    def role(self):
        return "Teacher"

    def extra(self):
        return self.department
    
def parse_person(line):
    parts = line.strip().split(";")
    if len(parts) != 5:
        raise AnketaError("Некорректное количество полей.")
    if parts[0] == "s":
        return Student(parts[1], parts[2], parts[3], parts[4])
    elif parts[0] == "t":
        return Teacher(parts[1], parts[2], parts[3], parts[4])
    else:
        raise AnketaError("Неизвестный тип анкеты.")
    
    
"""Владимир Маяковский
Ничего не понимают
Вошел к парикмахеру, сказал – спокойный!
«Будьте добры, причешите мне уши».
Гладкий парикмахер сразу стал хвойный,
лицо вытянулось, как у груши.
«Сумасшедший!
Рыжий!» –
запрыгали слова.
Ругань металась от писка до писка,
и до-о-о-о-лго
хихикала чья-то голова,
выдергиваясь из толпы, как старая редиска."""