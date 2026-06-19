from konsos import Console
from eto_baza import Database
from file_db import FileDatabase


def choose_database():
    print("=== Выбор режима хранения данных ===")
    print("1. in-memory")
    print("2. JSON")
    choice = input("Ваш выбор (1 или 2): ").strip()
    while choice not in ('1', '2'):
        print("Некорректный ввод. Введите 1 или 2.")
        choice = input("Ваш выбор (1 или 2): ").strip()
    return Database() if choice == '1' else FileDatabase()


if __name__ == "__main__":
    db = choose_database()
    console = Console(db)
    console.run()
