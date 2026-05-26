from eggogoproveryalka9000 import inputCheck, OUTLINE, USER_INPUT
from eto_baza import Database
from eggogi import Error_ValueUnacceptable, Error_FieldNotFound


def yesno(a):

    if a == 1:
        b = 'Да'
    else:
        b = 'Нет'
    return b


def print_record(record: dict):
    print(f"{record['id']}: {record['name']}\n"
          f"Редкость: {int(record['rarity']) * '*'}\n"
          f"Предпочитаемая дистанция: {record['dist_apt']}\n"
          f"Предпочитаемая стратегия: {record['strat']}\n"
          f"Может бежать в грязи? {yesno(int(record['dirt']))}\n")


def add_uma(db: Database):
    print('\n--- Добавление умамусуме ---')
    data = {}
    prompts = {
        'name': 'Имя: ',
        'rarity': 'Редкость (1-3): ',
        'dist_apt': 'Предпочитаемая дистанция: ',
        'strat': 'Предпочитаемая стратегия: ',
        'dirt': 'Может бегать в грязи? (0/1): '
    }
    for field in USER_INPUT:
        data[field] = input(prompts[field].strip())
    try:
        no_errors = inputCheck(data)
        record = db.add_uma(no_errors)
        print('Умамусуме добавлена успешно!')
        print_record(record)
    except Error_ValueUnacceptable as e:
        print(f'Ошибка: недопустимое значение {e}')


def show_all(db: Database):
    records = db.find_uma()
    if not records:
        print('Тут ничего нет!')
        return
    print('\n--- Все умамусуме ---')
    for rec in records:
        print_record(rec)


def search_umas(db: Database):
    print('\n--- Поиск умамусуме ---')
    print('Введите фильтры в виде "поле=значение" через запятую, например: rarity=2, strat=end')
    filtr = input('Фильтры: ').strip()
    if not filtr:
        print('Фильтры не выбраны')
        return

    filters = {}
    try:
        parts = [p.strip() for p in filtr.split(',') if p.strip()]
        for part in parts:
            if '=' not in part:
                raise ValueError(f"Некорректный формат фильтра {part}")
            field, value = part.split('=', 1)
            if field in OUTLINE:
                exp_type = OUTLINE[field]
                if exp_type == int:
                    value = int(value)
            filters[field] = value

        res = db.find_uma(filters)
        if not res:
            print('Соответствий фильтрам не найдено')
        else:
            print(f'Найдено соответствий: {len(res)}')
            for r in res:
                print_record(r)
    except ValueError or Error_FieldNotFound as e:
        print(f'Ошибка: {e}')


def run():
    db = Database()
    menu = """
1. Добавить умамусуме
2. Показать всех умамусуме
3. Найти умамусуме (фильтрация)
0. Выход
"""
    while True:
        print(menu)
        action = input("Выберите действие: ").strip()
        if action == '1':
            add_uma(db)
        elif action == '2':
            show_all(db)
        elif action == '3':
            search_umas(db)
        elif action == '0':
            print("Пока-пока!")
            break
        else:
            print("Некорректный ввод")
