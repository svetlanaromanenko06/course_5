from employers import employers_list
import requests
import json
import time

class HHApi:
    """Класс для подключения к API hh.ru и работы с ним"""

    def __init__(self, per_page=100):
        self.api_url = 'https://api.hh.ru/vacancies'
        self.per_page = per_page


    def get_hh_data(self):
        """Подключается к API hh.ru и получает данные о компаниях и их вакансиях"""

        employer_data = []

        for employer_id in employers_list:


            params = {
                    'employer_id': employer_id,
                    'area': 113,
                    'per_page': self.per_page
                }
            response = requests.get(self.api_url, params)
            if response.status_code ==200:
                data = response.json()
                employer_data.append(data)
                time.sleep(0.20)  # Задержка запроса

            else:
                print(f'Ошибка подключения к серверу - {response.status_code}')

        return employer_data



hh = HHApi()
print(hh.get_hh_data())