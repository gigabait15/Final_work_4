import json
import os
import requests
from work_class.Abstract_basic import Abstract_basic



class SuperJob(Abstract_basic):
    all_job = []
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://api.superjob.ru/2.0/vacancies/"


    def dump_json(self, filename):
        """Функция открывает файл вакансий, создает словарь из ключевых значений и записывает их в список класса"""
        api_key: str = os.getenv('API_S')
        headers = {"X-Api-App-Id": api_key}
        params = {"POST": "/2.0/favorites/ HTTP/1.1",
                  "Host": "api.superhob.ru",
                  "Authorization": "Bearer r.000000010000001.example.access_token",
                  "Content - Type": "application/x-www-form-urlencoded"
                  }
        count = 0

        # Открываем файл для записи
        with open(f'json_dir/{filename}.json', 'a', encoding="utf-8") as f:
            all_job = []
            while True:
                response = requests.get(f"{self.url}?t=4&page={count}", headers=headers, params=params).json()
                items = response.get("objects",
                                       [])  # Получаем элементы "objects" из текущего ответа или пустой список, если ключ отсутствует

                if not items:
                    break  # Прерываем цикл, если список "items" пуст
                all_job.extend(items)
                count += 1
                # Записываем элементы в файл
            json.dump({"objects": all_job}, f, ensure_ascii=False, indent=2)


    def loads_json(self, filename):
        """Функция открывает файл вакансий,
        создает словарь из ключевых значений и записывает их в список класса"""
        with open(f'../json_dir/{filename}.json', 'r', encoding="utf-8") as file:
            data = json.load(file)
            for index, value in enumerate(data["objects"]):
                self.__name = value["profession"]  # название вакансии
                self.__link = value["link"]  # ссылка на вакансию
                s_from = value["payment_from"]
                s_to = value["payment_to"]
                self.__salary_from = ((s_from + s_to) // 2) if s_from and s_from >0 else s_from + s_to  # зарплата
                self.__currency = value["currency"] if isinstance(self.__salary_from, int) else ""  # валюта заработной платы
                self.__responsibility = value["firm_activity"] \
                    if value["firm_activity"] is not None else "Уточнить у работодателя"  # обязанности
                self.__city = value["town"]["title"]  # город в котором находиться вакансия
                self.__street = value["address"] \
                    if value["address"] != None \
                    else "Уточнить у работодателя"  # улица на которой находиться вакансия
                self.__metro = value["metro"][0]["title"] \
                    if value["metro"] != [] \
                    else "Уточнить у работодателя"  # станция метро на которой находиться вакансия
                self.__experience = value["experience"]["title"] \
                    if value["experience"]["title"] \
                       is not None else "Уточнить у работодателя"  # требуемый опыт работы для данной вакансии
                self.__employment = value["type_of_work"]["title"] \
                    if value["type_of_work"]["title"] \
                       is not None else "Уточнить у работодателя"  # тип занятости
                self.__employer = value["firm_name"]  # название компании
                all_info = {"название вакансии": self.__name, "ссылка на вакансию": self.__link,
                            "зарплата": self.__salary_from, "валюта": self.__currency,
                            "обязанности": " ".join(self.__responsibility.split("\n")),
                            "город": self.__city, "улица": self.__street,
                            "метро": self.__metro, "опыт": self.__experience, "тип занятости": self.__employment,
                            "название компании": self.__employer}
                SuperJob.all_job.append(all_info)





