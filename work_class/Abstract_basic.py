from abc import ABC, abstractmethod
import requests


class Abstract_basic(ABC):

    def __init__(self):
        self.url = None  # url сайта
        self.__name = None  # название вакансии
        self.__link = None  # ссылка на вакансию
        self.__salary_from = None  # зарплата
        self.__currency = None  # валюта заработной платы
        self.__requirement = None  # требования
        self.__responsibility = None  # обязанности
        self.__city = None  # город в котором находиться вакансия
        self.__street = None  # улица на которой находиться вакансия
        self.__metro = None  # станция метро на которой находиться вакансия
        self.__experience = None  # требуемый опыт работы для данной вакансии
        self.__employment = None  # тип занятости
        self.__employer = None  # название компании

    @abstractmethod
    def dump_json(self):
        """Функция открывает файл вакансий, создает словарь из ключевых значений и записывает их в список класса"""
        pass