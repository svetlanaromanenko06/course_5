from config import config
from db_manager import DBManager
from HH import HH

def main():
   my_db = DBManager('vacancies')
   print('Сoздаем базу данных и таблицы')
   print()
   my_db.create_database()
   print('База данных создана.')
   print()
   data_hh= HH()
   employers = data_hh.get_data_vacancies()
   my_db.insert(employers)


if __name__ == '__main__':
   main()