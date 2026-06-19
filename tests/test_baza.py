import unittest
from eto_baza import Database
from eggogi import FieldNotFoundError, ValueUnacceptableError


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database()

    def test_add_uma_success(self):
        data = {'name': 'Skibidi Rizz', 'rarity': 3, 'distance': 'mile', 'strat': 'front', 'dirt': 1}
        record = self.db.add_uma(data)
        self.assertEqual(record['id'], 1)
        self.assertEqual(record['name'], 'Skibidi Rizz')
        self.assertEqual(record['rarity'], 3)
        self.assertEqual(record['distance'], 'mile')
        self.assertEqual(record['strat'], 'front')
        self.assertEqual(record['dirt'], 1)

    def test_add_uma_failure_validation(self):
        data = {'name': 'Skibidi Rizz', 'rarity': 3, 'distance': 'mile', 'strat': 'front'}
        with self.assertRaises(ValueUnacceptableError):
            self.db.add_uma(data)

    def test_find_all_empty(self):
        self.assertEqual(self.db.find_uma(), [])

    def test_find_all_after_add(self):
        self.db.add_uma({'name': 'Skibidi Rizz', 'rarity': 3, 'distance': 'mile', 'strat': 'front', 'dirt': 1})
        self.db.add_uma({'name': 'Fortnite Dance', 'rarity': 2, 'distance': 'sprint', 'strat': 'pace', 'dirt': 0})
        records = self.db.find_uma()
        self.assertEqual(len(records), 2)

    def test_find_with_filter(self):
        self.db.add_uma({'name': 'A', 'rarity': 1, 'distance': 'sprint', 'strat': 'front', 'dirt': 0})
        self.db.add_uma({'name': 'B', 'rarity': 2, 'distance': 'mile', 'strat': 'pace', 'dirt': 1})
        records = self.db.find_uma({'rarity': 2})
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['name'], 'B')

    def test_find_filter_field_not_found(self):
        with self.assertRaises(FieldNotFoundError) as cm:
            self.db.find_uma({'is_golshi': 1})
        self.assertIn('Поле is_golshi не найдено', str(cm.exception))

    def test_find_sort_by_id_asc(self):
        self.db.add_uma({'name': 'B', 'rarity': 1, 'distance': 'sprint', 'strat': 'front', 'dirt': 0})
        self.db.add_uma({'name': 'A', 'rarity': 2, 'distance': 'mile', 'strat': 'pace', 'dirt': 1})
        records = self.db.find_uma(sort_by='id', sort_order='asc')
        self.assertEqual([r['id'] for r in records], [1, 2])

    def test_find_sort_by_id_desc(self):
        self.db.add_uma({'name': 'B', 'rarity': 1, 'distance': 'sprint', 'strat': 'front', 'dirt': 0})
        self.db.add_uma({'name': 'A', 'rarity': 2, 'distance': 'mile', 'strat': 'pace', 'dirt': 1})
        records = self.db.find_uma(sort_by='id', sort_order='desc')
        self.assertEqual([r['id'] for r in records], [2, 1])

    def test_find_sort_by_name(self):
        self.db.add_uma({'name': 'B', 'rarity': 1, 'distance': 'sprint', 'strat': 'front', 'dirt': 0})
        self.db.add_uma({'name': 'A', 'rarity': 2, 'distance': 'mile', 'strat': 'pace', 'dirt': 1})
        records = self.db.find_uma(sort_by='name', sort_order='asc')
        self.assertEqual([r['name'] for r in records], ['A', 'B'])

    def test_find_sort_by_distance(self):
        self.db.add_uma({'name': 'A', 'rarity': 1, 'distance': 'long', 'strat': 'front', 'dirt': 0})
        self.db.add_uma({'name': 'B', 'rarity': 2, 'distance': 'mile', 'strat': 'pace', 'dirt': 1})
        self.db.add_uma({'name': 'C', 'rarity': 3, 'distance': 'sprint', 'strat': 'end', 'dirt': 0})
        records = self.db.find_uma(sort_by='distance', sort_order='asc')
        self.assertEqual([r['distance'] for r in records], ['sprint', 'mile', 'long'])

    def test_find_sort_by_strat(self):
        self.db.add_uma({'name': 'A', 'rarity': 1, 'distance': 'sprint', 'strat': 'front', 'dirt': 0})
        self.db.add_uma({'name': 'B', 'rarity': 2, 'distance': 'mile', 'strat': 'pace', 'dirt': 1})
        self.db.add_uma({'name': 'C', 'rarity': 3, 'distance': 'long', 'strat': 'end', 'dirt': 0})
        records = self.db.find_uma(sort_by='strat', sort_order='asc')
        self.assertEqual([r['strat'] for r in records], ['front', 'pace', 'end'])

    def test_find_sort_by_invalid_field(self):
        with self.assertRaises(FieldNotFoundError) as cm:
            self.db.find_uma({'is_golshi': 1})
        self.assertIn('Поле is_golshi не найдено', str(cm.exception))

    def test_find_with_filter_and_sort(self):
        self.db.add_uma({'name': 'A', 'rarity': 1, 'distance': 'sprint', 'strat': 'front', 'dirt': 0})
        self.db.add_uma({'name': 'B', 'rarity': 2, 'distance': 'mile', 'strat': 'pace', 'dirt': 1})
        self.db.add_uma({'name': 'C', 'rarity': 1, 'distance': 'long', 'strat': 'end', 'dirt': 0})
        records = self.db.find_uma({'rarity': 1}, sort_by='name', sort_order='asc')
        self.assertEqual([r['name'] for r in records], ['A', 'C'])


if __name__ == '__main__':
    unittest.main()
