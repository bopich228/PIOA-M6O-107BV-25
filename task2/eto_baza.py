from typing import List, Dict, Any
from eggogi import Error_FieldNotFound
from eggogoproveryalka9000 import OUTLINE

class Database:
    def __init__(self):
        self._umas: List[Dict[str, Any]] = []
        self._next_id = 1

    def add_uma(self, real_data: dict) -> dict:
        uma = {'id': self._next_id, **real_data}
        self._umas.append(uma)
        self._next_id += 1
        return uma

    def find_uma(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        if not filters:
            return list(self._umas)

        for field in filters:
            if field not in OUTLINE:
                raise Error_FieldNotFound(f'Поле {field} не найдено')

        res = []
        for record in self._umas:
            if all(record.get(field) == value for field, value in filters.items()):
                res.append(record)
        return res

