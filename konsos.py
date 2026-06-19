from typing import Any
from config import USER_INPUT, OUTLINE
from eggogi import ValueUnacceptableError, FieldNotFoundError


class Console:
    def __init__(self, db: Any):
        self.db = db

    @staticmethod
    def _yes_no(value: int) -> str:
        return 'Да' if value == 1 else 'Нет'

    def _print_record(self, record: dict):
        print(f"{record['id']}: {record['name']}\n"
              f"Редкость: {int(record['rarity']) * '*'}\n"
              f"Предпочитаемая дистанция: {record['distance']}\n"
              f"Предпочитаемая стратегия: {record['strat']}\n"
              f"Может бежать в грязи? {self._yes_no(int(record['dirt']))}\n")

    def add_uma(self):
        print('\n--- Добавление умамусуме ---')
        data = {}
        prompts = {
            'name': 'Имя: ',
            'rarity': 'Редкость (1-3): ',
            'distance': 'Предпочитаемая дистанция: ',
            'strat': 'Предпочитаемая стратегия: ',
            'dirt': 'Может бегать в грязи? (0/1): '
        }
        for field in USER_INPUT:
            data[field] = input(prompts[field].strip())
        try:
            record = self.db.add_uma(data)
            print('Умамусуме добавлена успешно!')
            self._print_record(record)
        except ValueUnacceptableError as e:
            print(f'Ошибка: недопустимое значение {e}')

    def show_all(self):
        sort_by, sort_order = self._ask_sort()
        try:
            records = self.db.find_uma(sort_by=sort_by, sort_order=sort_order)
        except FieldNotFoundError as e:
            print(f'Ошибка: {e}')
            return
        if not records:
            print('Тут ничего нет!')
            return
        print('\n--- Все умамусуме ---')
        for rec in records:
            self._print_record(rec)

    def search_umas(self):
        print('\n--- Поиск умамусуме ---')
        print('Введите фильтры в виде "поле=значение" через запятую, например: rarity=2, strat=end')
        filtr = input('Фильтры: ').strip().lower()
        if not filtr:
            print('Фильтры не выбраны')
            return

        filters = {}
        try:
            parts = [p.strip().lower() for p in filtr.split(',') if p.strip().lower()]
            for part in parts:
                if '=' not in part:
                    raise ValueError(f"Некорректный формат фильтра {part}")
                field, value = part.split('=', 1)
                if field in OUTLINE:
                    exp_type = OUTLINE[field]
                    if exp_type == int:
                        value = int(value)
                filters[field] = value

            sort_by, sort_order = self._ask_sort()
            res = self.db.find_uma(filters, sort_by, sort_order)
            if not res:
                print('Соответствий фильтрам не найдено')
            else:
                print(f'Найдено соответствий: {len(res)}')
                for r in res:
                    self._print_record(r)
        except (ValueError, FieldNotFoundError) as e:
            print(f'Ошибка: {e}')

    @staticmethod
    def _ask_sort():
        sort_choice = input('Сортировать результат? (y/n, по умолчанию n): ').strip().lower()
        if sort_choice != 'y':
            return None, 'asc'
        sort_by = input('Введите поле для сортировки (id, name, rarity, distance, strat, dirt): ').strip().lower()
        if sort_by not in OUTLINE:
            print(f'Поле {sort_by} не найдено, сортировка отменена')
            return None, 'asc'
        order = input('Порядок: asc (по возрастанию) или desc (по убыванию), по умолчанию asc: ').strip().lower()
        if order not in ('asc', 'desc'):
            order = 'asc'
        return sort_by, order

    def run(self):
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
                self.add_uma()
            elif action == '2':
                self.show_all()
            elif action == '3':
                self.search_umas()
            elif action == '0':
                print("Пока-пока!")
                break
            else:
                print("Некорректный ввод")
