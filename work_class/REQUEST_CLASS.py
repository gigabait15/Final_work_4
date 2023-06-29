import os
import requests
import time

from work_class.ABSTRACT_CLASS import Abstract_basic


class HH(Abstract_basic):

    def __init__(self):
        super().__init__()
        self.url = "https://api.hh.ru/vacancies"  # url сайта

    def requests_json(self, page=0):
        while True:
            """Получаем данные с сайта и сохраняем их в список для дальнейшей работы """
            response = requests.get(f"{self.url}?page={page}")
            data = response.json()
            items = data.get("items", [])

            if not items:
                break  # Прерываем цикл, если список "items" пуст

            self.all_job.extend(items)
            time.sleep(0.02)
            page += 1
        return self.all_job


class SuperJob(Abstract_basic):

    def __init__(self):
        super().__init__()
        self.url = "https://api.superjob.ru/2.0/vacancies/"  # url сайта
        self.__api_key: str = os.getenv('API_S')  # секретный ключ для сайта
        self.__headers = {"X-Api-App-Id": self.__api_key}  # Передача ключа для входа
        self.__params = {"POST": "/2.0/favorites/ HTTP/1.1",
                         "Host": "api.superhob.ru",
                         "Authorization": "Bearer r.000000010000001.example.access_token",
                         "Content - Type": "application/x-www-form-urlencoded"
                         }  # Данные для корректного подключения

    def requests_json(self, page=0):
        while True:
            """Получаем данные с сайта и сохраняем их в список для дальнейшей работы """
            response = requests.get(f"{self.url}?t=4&page={page}",
                                    headers=self.__headers, params=self.__params)
            data = response.json()
            items = data.get("objects", [])

            if not items:
                break  # Прерываем цикл, если список "items" пуст

            self.all_job.extend(items)
            page += 1
        return self.all_job


