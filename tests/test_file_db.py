import unittest
import json
import os
import tempfile
from file_db import FileDatabase
from eggogi import FieldNotFoundError, ValueUnacceptableError


class TestFileDatabase(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.filename = self.temp_file.name
        self.db = FileDatabase(self.filename)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_add_uma_success(self):
        data = {'name': 'Skibidi Rizz', 'rarity': 3, 'distance': 'mile', 'strat': 'front', 'dirt': 1}
        record = self.db.add_uma(data)
        self.assertEqual(record['id'], 1)
        self.assertEqual(record['name'], 'Skibidi Rizz')
        with open(self.filename, 'r') as f:
            saved = json.load(f)
        self.assertEqual(len(saved['records']), 1)
        self.assertEqual(saved['next_id'], 2)

    def test_add_uma_failure_validation(self):
        data = {'name': 'Skibidi Rizz', 'rarity': 3, 'distance': 'mile', 'strat': 'front'}
        with self.assertRaises(ValueUnacceptableError):
            self.db.add_uma(data)

    def test_find_all_empty(self):
        self.assertEqual(self.db.find_uma(), [])

    def test_find_all_after_add(self):
        self.db.add_uma({'name': 'A', 'rarity': 1, 'distance': 'sprint', 'strat': 'front', 'dirt': 0})
        self.db.add_uma({'name': 'B', 'rarity': 2, 'distance': 'mile', 'strat': 'pace', 'dirt': 1})
        records = self.db.find_uma()
        self.assertEqual(len(records), 2)

    def test_find_with_filter(self):
        self.db.add_uma({'name': 'A', 'rarity': 1, 'distance': 'sprint', 'strat': 'front', 'dirt': 0})
        self.db.add_uma({'name': 'B', 'rarity': 2, 'distance': 'mile', 'strat': 'pace', 'dirt': 1})
        records = self.db.find_uma({'rarity': 2})
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['name'], 'B')

    def test_find_filter_field_not_found(self):
        with self.assertRaises(FieldNotFoundError):
            self.db.find_uma({'is_golshi': 1})

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

    def test_persistence_between_instances(self):
        self.db.add_uma({'name': 'Skibidi Rizz', 'rarity': 3, 'distance': 'mile', 'strat': 'front', 'dirt': 1})
        new_db = FileDatabase(self.filename)
        records = new_db.find_uma()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['name'], 'Skibidi Rizz')
        self.assertEqual(records[0]['id'], 1)

    def test_load_corrupted_file(self):
        with open(self.filename, 'w') as f:
            f.write('{not json}')
        db = FileDatabase(self.filename)
        self.assertEqual(db.find_uma(), [])
        db.add_uma({'name': 'New', 'rarity': 1, 'distance': 'sprint', 'strat': 'front', 'dirt': 0})
        self.assertEqual(len(db.find_uma()), 1)

    def test_load_missing_file(self):
        os.remove(self.filename)
        db = FileDatabase(self.filename)
        self.assertEqual(db.find_uma(), [])
        db.add_uma({'name': 'New', 'rarity': 1, 'distance': 'sprint', 'strat': 'front', 'dirt': 0})
        self.assertTrue(os.path.exists(self.filename))


if __name__ == '__main__':
    unittest.main()
