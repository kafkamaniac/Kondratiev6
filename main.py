from registry import Registry

def main():
    filename = "ankety.txt"
    registry = Registry()

    if not registry.load(filename):
        print(f"Файл {filename} не найден.")
        return

    registry.accepted.sort()

    print(f"{'№':<4} {'ФИО':<30} {'Почта':<30} {'Роль':<18} {'Группа/кафедра':<20} {'Телефон'}")
    print("-" * 130)

    role_names = {
        "Student": "студент",
        "Teacher": "преподаватель"
    }

    for number, person in enumerate(registry.accepted, start=1):
        print(
            f"{number:<4} "
            f"{person.fio:<30} "
            f"{person.email:<30} "
            f"{role_names.get(person.role(), person.role()):<18} "
            f"{person.extra():<20} "
            f"{person.masked_phone()}"
        )

    print("-" * 130)

    print(f"\nОтклонено строк: {len(registry.errors)}")
    
    for error in registry.errors:
        print(error)

    print(f"\nПринято: {len(registry)} | Отклонено: {len(registry.errors)}")
    print("\nПо ролям:")
    for role, count in registry.statistics_by_role().items():
        print(f"  {role_names.get(role, role):<18} {count}")

    print("\nПо группам:")
    for group, count in registry.statistics_by_group().items():
        print(f"  {group:<18} {count}")

    registry.save_ok()
    registry.save_errors()

    print("\nРезультаты сохранены в ok.txt и errors.txt.")

if __name__ == "__main__":
    main()
    
"""Канителят стариков бригады
канитель одну и ту ж.
Товарищи!
На баррикады!–
баррикады сердец и душ.
Только тот коммунист истый,
кто мосты к отступлению сжег.
Довольно шагать, футуристы,
в будущее прыжок!
Паровоз построить мало –
накрутил колес и утек.
Если песнь не громит вокзала,
то к чему переменный ток?
Громоздите за звуком звук вы
и вперед,
поя и свища.
Есть еще хорошие буквы:
Эр,
Ша,
Ща.
Это мало – построить парами,
распушить по штанине канты.
Все совдепы не сдвинут армий,
если марш не дадут музыканты.
На улицу тащите рояли,
барабан из окна багром!
Барабан,
рояль раскроя ли,
но чтоб грохот был,
чтоб гром.
Это что – корпеть на заводах,
перемазать рожу в копоть
и на роскошь чужую
в отдых
осовелыми глазками хлопать.
Довольно грошовых истин.
Из сердца старое вытри.
Улицы – наши кисти.
Площади – наши палитры.
Книгой времени
тысячелистой
революции дни не воспеты.
На улицы, футуристы,
барабанщики и поэты!
"""