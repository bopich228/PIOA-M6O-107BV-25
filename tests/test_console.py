import unittest
from unittest.mock import patch, MagicMock
from konsos import Console
from eto_baza import Database
from eggogi import ValueUnacceptableError


class TestConsole(unittest.TestCase):
    def setUp(self):
        self.ui = Console()
        self.ui.db = MagicMock(spec=Database)

    def test_yes_no(self):
        self.assertEqual(Console._yes_no(1), 'Да')
        self.assertEqual(Console._yes_no(0), 'Нет')

    @patch('builtins.input', side_effect=['Test', '2', 'mile', 'pace', '1'])
    @patch('builtins.print')
    def test_add_uma_success(self, mock_print):
        self.ui.db.add_uma.return_value = {
            'id': 1, 'name': 'Test', 'rarity': 2, 'distance': 'mile', 'strat': 'pace', 'dirt': 1
        }
        self.ui.add_uma()
        self.ui.db.add_uma.assert_called_once()
        mock_print.assert_any_call('Умамусуме добавлена успешно!')

    @patch('builtins.input', side_effect=['Test', '2', 'mile', 'pace', '1'])
    @patch('builtins.print')
    def test_add_uma_failure(self, mock_print):
        self.ui.db.add_uma.side_effect = ValueUnacceptableError('ошибка')
        self.ui.add_uma()
        mock_print.assert_any_call('Ошибка: недопустимое значение ошибка')

    @patch('builtins.input', side_effect=['n'])
    @patch('builtins.print')
    def test_show_all_no_records(self, mock_print):
        self.ui.db.find_uma.return_value = []
        self.ui.show_all()
        self.ui.db.find_uma.assert_called_with(sort_by=None, sort_order='asc')
        mock_print.assert_any_call('Тут ничего нет!')

    @patch('builtins.input', side_effect=['n'])
    @patch('builtins.print')
    def test_show_all_with_records(self, mock_print):
        records = [{'id': 1, 'name': 'A', 'rarity': 1, 'distance': 'sprint', 'strat': 'front', 'dirt': 0}]
        self.ui.db.find_uma.return_value = records
        self.ui.show_all()
        self.ui.db.find_uma.assert_called_with(sort_by=None, sort_order='asc')
        mock_print.assert_any_call('\n--- Все умамусуме ---')

    @patch('builtins.input', side_effect=['y', 'name', 'desc'])
    @patch('builtins.print')
    def test_show_all_with_sort(self, mock_print):
        records = [{'id': 1, 'name': 'B', 'rarity': 1, 'distance': 'sprint', 'strat': 'front', 'dirt': 0},
                   {'id': 2, 'name': 'A', 'rarity': 2, 'distance': 'mile', 'strat': 'pace', 'dirt': 1}]
        self.ui.db.find_uma.return_value = records
        self.ui.show_all()
        self.ui.db.find_uma.assert_called_with(sort_by='name', sort_order='desc')
        mock_print.assert_any_call('\n--- Все умамусуме ---')

    @patch('builtins.input', side_effect=['y', 'invalid', 'asc'])
    @patch('builtins.print')
    def test_show_all_invalid_sort_field(self, mock_print):
        self.ui.db.find_uma.return_value = []
        self.ui.show_all()
        self.ui.db.find_uma.assert_called_with(sort_by=None, sort_order='asc')
        mock_print.assert_any_call('Поле invalid не найдено, сортировка отменена')

    @patch('builtins.input', side_effect=['rarity=2', 'n'])
    @patch('builtins.print')
    def test_search_umas_success(self, mock_print):
        records = [{'id': 1, 'name': 'B', 'rarity': 2, 'distance': 'mile', 'strat': 'pace', 'dirt': 1}]
        self.ui.db.find_uma.return_value = records
        self.ui.search_umas()
        self.ui.db.find_uma.assert_called_with({'rarity': 2}, None, 'asc')
        mock_print.assert_any_call('Найдено соответствий: 1')

    @patch('builtins.input', side_effect=['', 'n'])
    @patch('builtins.print')
    def test_search_umas_empty_filters(self, mock_print):
        self.ui.search_umas()
        mock_print.assert_any_call('Фильтры не выбраны')
        self.ui.db.find_uma.assert_not_called()

    @patch('builtins.input', side_effect=['invalid_format', 'n'])
    @patch('builtins.print')
    def test_search_umas_invalid_filter_format(self, mock_print):
        self.ui.search_umas()
        mock_print.assert_any_call('Ошибка: Некорректный формат фильтра invalid_format')

    @patch('builtins.input', side_effect=['rarity=abc', 'n'])
    @patch('builtins.print')
    def test_search_umas_invalid_value_type(self, mock_print):
        self.ui.db.find_uma.side_effect = ValueError("invalid literal for int() with base 10: 'abc'")
        self.ui.search_umas()
        mock_print.assert_any_call('Ошибка: invalid literal for int() with base 10: \'abc\'')

    @patch('builtins.input', side_effect=['n'])
    def test_ask_sort_no(self):
        sort_by, order = self.ui._ask_sort()
        self.assertIsNone(sort_by)
        self.assertEqual(order, 'asc')

    @patch('builtins.input', side_effect=['y', 'name', 'desc'])
    def test_ask_sort_yes(self):
        sort_by, order = self.ui._ask_sort()
        self.assertEqual(sort_by, 'name')
        self.assertEqual(order, 'desc')

    @patch('builtins.input', side_effect=['y', 'invalid', 'asc'])
    @patch('builtins.print')
    def test_ask_sort_invalid_field(self, mock_print):
        sort_by, order = self.ui._ask_sort()
        self.assertIsNone(sort_by)
        self.assertEqual(order, 'asc')
        mock_print.assert_any_call('Поле invalid не найдено, сортировка отменена')


if __name__ == '__main__':
    unittest.main()
