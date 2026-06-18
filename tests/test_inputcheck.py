import unittest
from eggogoproveryalka9000 import InputCheck
from eggogi import ValueUnacceptableError


class TestInputCheck(unittest.TestCase):
    def test_valid_data(self):
        data = {
            'name': 'Skibidi Rizz',
            'rarity': '3',
            'distance': 'mile',
            'strat': 'front',
            'dirt': '1'
        }
        result = InputCheck.validate(data)
        expected = {'name': 'Skibidi Rizz', 'rarity': 3, 'distance': 'mile', 'strat': 'front', 'dirt': 1}
        self.assertEqual(result, expected)

    def test_missing_field(self):
        data = {'name': 'Skibidi Rizz', 'rarity': '3', 'distance': 'mile', 'strat': 'pace'}
        with self.assertRaises(ValueUnacceptableError) as cm:
            InputCheck.validate(data)
        self.assertIn('Отсутствует обязательное значение dirt', str(cm.exception))

    def test_invalid_name_not_string(self):
        data = {'name': 41224141, 'rarity': 3, 'distance': 'mile', 'strat': 'front', 'dirt': 1}
        with self.assertRaises(ValueUnacceptableError) as cm:
            InputCheck.validate(data)
        self.assertIn('Имя должно быть непустой строкой', str(cm.exception))

    def test_invalid_name_empty(self):
        data = {'name': ' ', 'rarity': 3, 'distance': 'mile', 'strat': 'front', 'dirt': 1}
        with self.assertRaises(ValueUnacceptableError) as cm:
            InputCheck.validate(data)
        self.assertIn('Имя должно быть непустой строкой', str(cm.exception))

    def test_invalid_name_symbols(self):
        data = {'name': '5k!b!d! R!zz', 'rarity': 3, 'distance': 'mile', 'strat': 'front', 'dirt': 1}
        with self.assertRaises(ValueUnacceptableError) as cm:
            InputCheck.validate(data)
        self.assertIn('Имя может содержать только латинские буквы, пробелы и точки', str(cm.exception))

    def test_invalid_rarity_not_int(self):
        data = {'name': 'Skibidi Rizz', 'rarity': 'sgfdfgsgfsd', 'distance': 'mile', 'strat': 'front', 'dirt': 1}
        with self.assertRaises(ValueUnacceptableError) as cm:
            InputCheck.validate(data)
        self.assertIn('Редкость умамусуме соответствует кол-ву звезд при получении и является целым числом от 1 до 3', str(cm.exception))

    def test_invalid_rarity_out_of_range(self):
        data = {'name': 'Skibidi Rizz', 'rarity': 228, 'distance': 'mile', 'strat': 'front', 'dirt': 1}
        with self.assertRaises(ValueUnacceptableError) as cm:
            InputCheck.validate(data)
        self.assertIn('Редкость умамусуме соответствует кол-ву звезд при получении и является целым числом от 1 до 3', str(cm.exception))

    def test_invalid_distance(self):
        data = {'name': 'Skibidi Rizz', 'rarity': 3, 'distance': 'very daleko', 'strat': 'front', 'dirt': 1}
        with self.assertRaises(ValueUnacceptableError) as cm:
            InputCheck.validate(data)
        self.assertIn('Дистанция должна быть sprint, mile, med или long', str(cm.exception))

    def test_invalid_strat(self):
        data = {'name': 'Skibidi Rizz', 'rarity': 3, 'distance': 'mile', 'strat': 'rush b', 'dirt': 1}
        with self.assertRaises(ValueUnacceptableError) as cm:
            InputCheck.validate(data)
        self.assertIn('Стратегия должна быть front, pace, late или end', str(cm.exception))

    def test_invalid_dirt_not_int(self):
        data = {'name': 'Skibidi Rizz', 'rarity': 3, 'distance': 'mile', 'strat': 'front', 'dirt': 'skibidi dop dop dop yes yes'}
        with self.assertRaises(ValueUnacceptableError) as cm:
            InputCheck.validate(data)
        self.assertIn('Если умамусуме способна эффективно бежать через грязь, введите 1. Если нет, то 0', str(cm.exception))

    def test_invalid_dirt_out_of_range(self):
        data = {'name': 'Skibidi Rizz', 'rarity': 3, 'distance': 'mile', 'strat': 'front', 'dirt': 9000}
        with self.assertRaises(ValueUnacceptableError) as cm:
            InputCheck.validate(data)
        self.assertIn('Если умамусуме способна эффективно бежать через грязь, введите 1. Если нет, то 0', str(cm.exception))


if __name__ == '__main__':
    unittest.main()
