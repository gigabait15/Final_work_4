import json
import time
import requests
from work_class.Abstract_basic import Abstract_basic
import os


class HH(Abstract_basic):
    all_job = []
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://api.hh.ru/vacancies"

    def __repr__(self):
        return f"Info(name='{self.__name}')"

    def dump_json(self, filename):
        """Сохраняем полученные данные в JSON-формате"""
        count = 0
        # Открываем файл для записи
        with open(f'json_dir/{filename}.json', 'a', encoding="utf-8") as f:
            all_job = []
            while True:
                response = requests.get(f"{self.url}?page={count}")
                data = response.json()
                items = data.get("items",
                                 [])  # Получаем элементы "items" из текущего ответа или пустой список, если ключ отсутствует

                if not items:
                    break  # Прерываем цикл, если список "items" пуст
                all_job.extend(items)
                # Записываем элементы в файл
                count += 1
                time.sleep(0.02)
            json.dump({"items": all_job}, f, ensure_ascii=False, indent=2)


    def loads_json(self, filename):
        """Функция открывает файл вакансий,
        создает словарь из ключевых значений и записывает их в список класса"""
        with open(f'../json_dir/{filename}.json', 'r', encoding="utf-8") as file:
            data = json.load(file)
            for index, value in enumerate(data["items"]):
                self.__name = value["name"]  # название вакансии
                self.__link = value["alternate_url"]  # ссылка на вакансию
                salary = value["salary"] if isinstance(value["salary"], dict) else "Уточнить у работодателя"  # Данные по заработное плате
                self.__currency = salary["currency"] if isinstance(salary, dict) else salary  # валюта заработной платы
                s_from = salary["from"] if isinstance(salary, dict) and salary["from"] is not None else 0  #начальный порог заработной платы
                s_to = salary["to"] if isinstance(salary, dict) and salary["to"] is not None else 0  #итоговый порог заработной платы
                s_cor = ((s_from + s_to) // 2) if s_from and s_to > 0 else s_from + s_to
                self.__salary_from = s_cor
                # Здесь начинается расчет и конвертация зарабатной платы
                if self.__currency == "Уточнить у работодателя":
                    self.__salary_from = 0
                if self.__currency == "KZT":
                    self.__salary_from = int(s_cor * 0.19)
                    self.__currency = "RUR"
                if self.__currency == "BYR":
                    self.__salary_from = int(s_cor * 33.07)
                    self.__currency = "RUR"
                if self.__currency == "KGS":
                    self.__salary_from = int(s_cor * 0.96)
                    self.__currency = "RUR"
                if self.__currency == "UZS":
                    self.__salary_from = int(s_cor * 0.0073)
                    self.__currency = "RUR"
                if self.__currency == "USD":
                    self.__salary_from = int(s_cor * 84.55)
                    self.__currency = "RUR"
                if self.__currency == "EUR":
                    self.__salary_from = int(s_cor * 91.05)
                    self.__currency = "RUR"
                self.__requirement = value["snippet"]["requirement"]  # требования
                self.__responsibility = value["snippet"]["responsibility"] \
                    if value["snippet"]["responsibility"] is not None else "Уточнить у работодателя"  # обязанности
                self.__city = value["area"]["name"]  # город в котором находиться вакансия
                self.__street = value["address"]["raw"] \
                    if value["address"] is not None else "Уточнить у работодателя"  # улица на которой находиться вакансия
                address = value["address"]["metro"] if value["address"]\
                    and value["address"]["metro"] is not None else "Уточнить у работодателя"
                self.__metro = address["station_name"] if isinstance(address, dict) else address # станция метро на которой находиться вакансия
                self.__experience = value["experience"]["name"]\
                    if value["experience"]["name"] is not None else "Уточнить у работодателя"  # требуемый опыт работы для данной вакансии
                self.__employment = value["employment"]["name"]\
                    if value["employment"]["name"] is not None else "Уточнить у работодателя"  # тип занятости
                self.__employer = value["employer"]["name"]\
                    if value["employer"]["name"] is not None else "Уточнить у работодателя"  # название компании
                all_info = {"название вакансии": self.__name, "ссылка на вакансию": self.__link, "зарплата": self.__salary_from, "валюта": self.__currency,
                            "требования": self.__requirement, "обязанности": self.__responsibility, "город": self.__city, "улица": self.__street,
                            "метро": self.__metro, "опыт": self.__experience, "тип занятости": self.__employment, "название компании": self.__employer}
                HH.all_job.append(all_info)

