import requests

class HH():
    '''
    Класс для работы с ресурсом HeadHunter.ru
    '''

    def __init__(self):
        self.api_url = 'https://api.hh.ru/vacancies'
        self.keyword = None
        self.per_page = 50

    def get_vacancies(self):
        """Метод для получения вакансий с помощью ApiHH"""

        vacancies = []
        params = {
            "text": self.keyword,
            "per_page": self.per_page, # количество вакансий на страницу
            'area': 113 #Россия
        }

        hh_response = requests.get(self.api_url, params)
        if hh_response.status_code == 200:
            data = hh_response.json()

            for item in data['items']:
                name = item['name']

                # проверка на наличие указания зарплаты
                if item['salary'] is None:
                    salary_from = 0
                    salary_to = 0

                elif not item['salary']['from']:
                    salary_from = 0
                    salary_to = item['salary']['to']

                elif not item['salary']['to']:
                    salary_from = item['salary']['from']
                    salary_to = salary_from

                else:
                    salary_from = item['salary']['from']
                    salary_to = item['salary']['to']

                experience = item['experience']['name']
                area = item['area']['name']
                vacancy_url = item['alternate_url']



                # Добавляем вакансию в список
                vacancies.append(name,)

            return vacancies

        else:
            print(f'Ошибка подключения к серверу - {hh_response.status_code}')

