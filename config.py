# вынес сюда константы из eggogoproveryalka9000
# (и здесь же сделать сортировку текстовых полей для второго доп пункта)

import string
ACCEPTABLE_SYMBOLS = string.ascii_letters + '. '
dist_var = ['sprint', 'mile', 'med', 'long']
strat_var = ['front', 'pace', 'late', 'end']

OUTLINE = {
    'id': int,
    'name': str,
    'rarity': int,
    'distance': str,
    'strat': str,
    'dirt': int
}

USER_INPUT = ['name', 'rarity', 'distance', 'strat', 'dirt']
DIST_ORDER = {'long': 3, 'med': 2, 'mile': 1, 'sprint': 0}
STRAT_ORDER = {'end': 3, 'late': 2, 'pace': 1, 'front': 0}
