from abc import ABC, abstractmethod


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
        pass


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
        pass

    @abstractmethod
    def json_get(self, pick: int):
        """Функция для получения вакансии из файла"""
        pass

    @abstractmethod
    def json_del(self, pick: int, value: dict):
        """Функция для удаления вакансии из файла"""
        pass

    @abstractmethod
    def json_add(self, pick: int, value: dict):
        """Функция для добавления вакансии из файла"""
        pass
