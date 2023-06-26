import json
from abc import ABC, abstractmethod
from typing import List, Any

import requests


class Abstract_basic(ABC):

    def __init__(self):
        self.url = None  # url сайта
        self.all_job = []

    def __str__(self):
        """Информация о классе"""
        return f"Info(name class ='{self.__class__.__name__}')"

    def __repr__(self):
        """Информация о классе"""
        return f"Info(url ='{self.url}')"

    @abstractmethod
    def requests_json(self):
        """Получение данных с сайта"""
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.json()
        else:
            print("неверный запрос")


class Abstract_JSON(ABC):

    def __init__(self):
        self.name = __class__.__name__
        self.all_job = []

    def __str__(self):
        """Информация о классе"""
        return f"Info(name class ='{self.name}')"

    @abstractmethod
    def json_save(self, pick: int):
        """Функция для сохранения вакансии в файл"""
        with open(f'file', 'r', encoding="utf-8") as file:
            json.dump({"items": None}, file, ensure_ascii=False, indent=2)

    @abstractmethod
    def json_get(self, pick: int):
        """Функция для получения вакансии из файла"""
        with open('file', 'r', encoding="utf-8") as file:
            data = json.load(file)
            self.all_job = data["items"]
        return self.all_job

    @abstractmethod
    def json_del(self, pick: int, value: dict):
        """Функция для удаления вакансии из файла"""
        with open('file', 'r', encoding="utf-8") as file:
            data = json.load(file)

            for items in data:
                if items == value:
                    del items

        with open('file', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    @abstractmethod
    def json_add(self, pick: int, value: dict):
        """Функция для добавления вакансии из файла"""
        with open('file', 'r', encoding="utf-8") as file:
            data = json.load(file)

            data.expend(value)

        with open('file', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)