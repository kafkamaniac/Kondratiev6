"""— Хранит список принятых анкет и список бракованных строк.
— Метод add(person) добавляет анкету.
— Метод load(filename) читает файл. Возвращает False, если файла нет.
— Пустые строки пропускает молча.
— Методы статистики: по ролям и по группам.
— Методы сохранения в ok.txt и errors.txt.
— __len__ возвращает число принятых анкет."""

from people import AnketaError, Student, Teacher


class Registry:
    def __init__(self):
        self.accepted = []
        self.errors = []

    def __iter__(self):
        return iter(self.accepted)
    
    def add(self, person):
        self.accepted.append(person)

    def load(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line_number, line in enumerate(file, start=1):
                    original_line = line.rstrip("\r\n")

                    if not original_line.strip():
                        continue

                    try:
                        parts = [part.strip() for part in original_line.split(";")]

                        if len(parts) != 5:
                            raise AnketaError("Некорректное количество полей.")

                        person_type, fio, email, phone, extra = parts

                        if person_type == "s":
                            person = Student(fio, email, phone, extra)
                        elif person_type == "t":
                            person = Teacher(fio, email, phone, extra)
                        else:
                            raise AnketaError("Неизвестный тип анкеты.")

                        self.add(person)

                    except AnketaError as e:
                        self.errors.append(
                            f"Строка {line_number}: {original_line} | Error: {e}"
                        )

            return True

        except FileNotFoundError:
            return False

    def statistics_by_role(self):
        stats = {}
        for person in self.accepted:
            role = person.role()
            stats[role] = stats.get(role, 0) + 1
        return stats

    def statistics_by_group(self):
        stats = {}
        for person in self.accepted:
            group = person.group_name()
            if group:
                stats[group] = stats.get(group, 0) + 1
        return stats

    def save_ok(self):
        with open("ok.txt", "w", encoding="utf-8") as file:
            for person in self.accepted:
                file.write(str(person) + "\n")

    def save_errors(self):
        with open("errors.txt", "w", encoding="utf-8") as file:
            for error in self.errors:
                file.write(error + "\n")

    def __len__(self):
        return len(self.accepted)
    
    
"""Владимир Маяковский
Гимн взятке
Пришли и славословим покорненько
тебя, дорогая взятка,
все здесь, от младшего дворника
до того, кто в золото заткан.

Всех, кто за нашей десницей
посмеет с укором глаза весть,
мы так, как им и не снится,
накажем мерзавцев за зависть.

Чтоб больше не смела вздыматься хула,
наденем мундиры и медали
и, выдвинув вперед убедительный кулак,
спросим: «А это видали?»

Если сверху смотреть –- разинешь рот.
И взыграет от радости каждая мышца.
Россия – сверху – прямо огород,
вся наливается, цветет и пышится.

А разве видано где-нибудь, чтоб стояла коза
и лезть в огород козе лень?..
Было бы время, я б доказал,
которые – коза и зелень.

И нечего доказывать – идите и берите.
Умолкнет газетная нечисть ведь.
Как баранов, надо стричь и брить их.
Чего стесняться в своем отечестве?
"""