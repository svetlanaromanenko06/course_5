#SQL-запросы для портала

--Содание таблицы vacancies
CREATE TABLE vacancies (
                vacancies_id SERIAL PRIMARY KEY,
                title varchar(100) NOT NULL ,
                salary_min REAL,
                salary_max REAL,
                employer_id INT REFERENCES employers(employer_id) NOT NULL,
                vacancy_url TEXT);

--Содание таблицы employers
CREATE TABLE employers (employer_id INT PRIMARY KEY, employer_name varchar NOT NULL);


--Получает список всех компаний и количество вакансий у каждой компании
SELECT employer, COUNT(*) AS vacancies_count
FROM vacancies
GROUP BY employer

или
SELECT COUNT(*) FROM vacancy
INNER JOIN company USING(company_id)


--Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
SELECT company_name, vacancy_name, salary_from, salary_to, vacancy_url FROM company
INNER JOIN vacancy ON vacancy.company_id=company.company_id




SELECT * FROM vacancyes
WHERE vacancy_name LIKE '%Python%' OR vacancy_name LIKE '%python%'

