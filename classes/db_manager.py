import psycopg2
from config import config
from typing import Any

class DBManager:
    """Класс для работы с базой данных, инициализируется названием базы данных и данными из конфигурационного файла"""
    def __init__(self, dbname: str):
        self.dbname = dbname
        self.params = config()


    def create_database(self):
        """Создает базу данных и таблицы"""
        # Подключаемся к postgres, чтобы создать БД
        conn = psycopg2.connect(dbname='postgres', **self.params)
        conn.autocommit = True
        cur = conn.cursor()


        cur.execute(f"DROP DATABASE IF EXISTS {self.dbname}")
        cur.execute(f"CREATE DATABASE {self.dbname}")

        cur.close()
        conn.close()

        # Подключаемся к созданной БД и создаем таблицы
        conn = psycopg2.connect(dbname=self.dbname, **self.params)

        with conn.cursor() as cur:
            cur.execute('''CREATE TABLE employers (employer_id INT PRIMARY KEY, employer_name varchar NOT NULL )''')

        conn.commit()

        with conn.cursor() as cur:
            cur.execute(
                '''CREATE TABLE vacancies (
                vacancies_id SERIAL PRIMARY KEY, 
                title varchar(100) NOT NULL ,
                salary_min REAL,
                salary_max REAL,
                employer_id INT REFERENCES employers(employer_id) NOT NULL,
                vacancy_url TEXT                
                )'''
            )

        conn.commit()

        conn.close()

    def insert(self, data) -> None:
        """Добавление данных в базу данных в таблицы"""
        conn = psycopg2.connect(dbname=self.dbname, **self.params)

        with conn.cursor() as cur:

            # Заполняем данными таблицу компаний-работадателей

            for emp in data:
                employer_id = emp['items'][0]['employer']['id']
                employer_name = emp['items'][0]['employer']['name']

                cur.execute(
                    """
                    INSERT INTO employers (employer_id, employer_name)
                    VALUES (%s, %s)
                    RETURNING employer_id
                    """,
                    (employer_id, employer_name)
                )
            #Заполняем данными таблицу вакансий

            for vacancy in emp['items']:
                vacancy_name = vacancy['name']

                if vacancy['salary'] is None:
                    salary_from = None
                    salary_to = None

                elif not vacancy['salary']['from']:
                    salary_from = None
                    salary_to = vacancy['salary']['to']

                elif not vacancy['salary']['to']:
                    salary_from = vacancy['salary']['from']
                    salary_to = salary_from

                else:
                    salary_from = vacancy['salary']['from']
                    salary_to = vacancy['salary']['to']

                vacancy_url = vacancy['alternate_url']

                cur.execute(
                    '''
                    INSERT INTO vacancies (title, salary_min, salary_max, employer_id, vacancy_url)
                    VALUES (%s, %s, %s, %s, %s)
                    ''',
                    (vacancy_name, salary_from, salary_to, employer_id, vacancy_url)
                )

        conn.commit()
        conn.close()
