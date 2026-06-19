from eggogi import ValueUnacceptableError
from config import ACCEPTABLE_SYMBOLS, dist_var, strat_var, USER_INPUT


class InputCheck:
    @staticmethod
    def validate(data: dict) -> dict:

        errors = []
        not_errors = {}

        for param in USER_INPUT:
            if param not in data:
                errors.append(f'Отсутствует обязательное значение {param}')

        if errors:
            raise ValueUnacceptableError("; ".join(errors))

        name = data['name']
        if not isinstance(name, str) or not name.strip():
            errors.append('\nИмя должно быть непустой строкой')
        else:
            for s in name:
                if s not in ACCEPTABLE_SYMBOLS:
                    errors.append('\nИмя может содержать только латинские буквы, пробелы и точки')
                    break
            else:
                not_errors['name'] = name.strip()

        try:
            rarity = int(data['rarity'])
            if not 1 <= rarity <= 3:
                raise ValueError
            not_errors['rarity'] = rarity
        except (ValueError, TypeError):
            errors.append('\nРедкость умамусуме соответствует кол-ву звезд при получении и является целым числом от 1 до 3')

        distance = data['distance'].strip().lower()
        if distance not in dist_var:
            errors.append('\nДистанция должна быть sprint, mile, med или long')
        else:
            not_errors['distance'] = distance

        strat = data['strat'].strip().lower()
        if strat not in strat_var:
            errors.append('\nСтратегия должна быть front, pace, late или end')
        else:
            not_errors['strat'] = strat

        try:
            dirt = int(data['dirt'])
            if not 0 <= dirt <= 1:
                raise ValueError
            not_errors['dirt'] = dirt
        except (ValueError, TypeError):
            errors.append('\nЕсли умамусуме способна эффективно бежать через грязь, введите 1. Если нет, то 0')

        if errors:
            raise ValueUnacceptableError('; '.join(errors))

        return not_errors
