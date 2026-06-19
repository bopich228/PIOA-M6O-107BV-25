import json
import os
from typing import List, Dict, Any, Optional

from config import OUTLINE, DIST_ORDER, STRAT_ORDER
from eggogi import FieldNotFoundError
from eggogoproveryalka9000 import InputCheck


class FileDatabase:
    def __init__(self, filename: str = "database.json"):
        self._filename = filename
        self._records: List[Dict[str, Any]] = []
        self._next_id = 1
        self._load()

    def _load(self):
        if not os.path.exists(self._filename):
            return

        try:
            with open(self._filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if not isinstance(data, dict) or 'next_id' not in data or 'records' not in data:
                return
            self._next_id = data['next_id']
            self._records = data['records']
        except (json.JSONDecodeError, IOError):
            return

    def _save(self):
        data = {
            'next_id': self._next_id,
            'records': self._records
        }
        with open(self._filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add_uma(self, real_data: dict) -> dict:
        verified_data = InputCheck.validate(real_data)
        uma = {'id': self._next_id, **verified_data}
        self._records.append(uma)
        self._next_id += 1
        self._save()
        return uma

    def find_uma(self,
                 filters: Optional[Dict[str, Any]] = None,
                 sort_by: Optional[str] = None,
                 sort_order: str = 'asc') -> List[Dict[str, Any]]:
        if filters is None:
            filters = {}

        for field in filters:
            if field not in OUTLINE:
                raise FieldNotFoundError(f'Поле {field} не найдено')

        result = []
        for record in self._records:
            if all(record.get(field) == value for field, value in filters.items()):
                result.append(record)

        if sort_by is not None:
            if sort_by not in OUTLINE:
                raise FieldNotFoundError(f'Поле {sort_by} не найдено')
            result = self._sort_records(result, sort_by, sort_order)

        return result

    @staticmethod
    def _sort_records(records: List[Dict[str, Any]], sort_by: str, sort_order: str) -> List[Dict[str, Any]]:
        def key_func(record):
            value = record.get(sort_by)
            if sort_by == 'distance':
                return DIST_ORDER[value]
            elif sort_by == 'strat':
                return STRAT_ORDER[value]
            elif isinstance(value, str):
                return value.lower() if value else ''
            else:
                return value

        reverse = (sort_order.lower() == 'desc')
        return sorted(records, key=key_func, reverse=reverse)
