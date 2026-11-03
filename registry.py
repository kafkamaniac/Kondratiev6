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

    def add(self, person):
        self.accepted.append(person)

    def load(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        parts = line.split(",")
                        if len(parts) != 4:
                            raise AnketaError("Некорректное количество полей.")

                        fio, email, phone, extra = parts[0], parts[1], parts[2], parts[3]
                        if "Student" in extra:
                            if extra.startswith("Student:"):
                                group = extra.split(":", 1)[1].strip()
                                student = Student(fio, email, phone, group)
                                self.add(student)
                            elif extra.startswith("Teacher:"):
                                department = extra.split(":", 1)[1].strip()
                                teacher = Teacher(fio, email, phone, department)
                                self.add(teacher)
                            else:
                                raise AnketaError("Неизвестная роль.")
                            
                        elif "Teacher" in extra:
                            department = extra.split(":")[1].strip()
                            teacher = Teacher(fio, email, phone, department)
                            self.add(teacher)
                        else:
                            raise AnketaError("Неизвестная роль.")
                        
                    except AnketaError as e:
                        self.errors.append(f"{line} | Error: {str(e)}")
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
            if isinstance(person, Student):
                group = person.group
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