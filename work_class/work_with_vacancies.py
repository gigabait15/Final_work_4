import json
import re


class Work_With_Vacancies:
    job_sj = []
    job_hh = []

    def __init__(self):
        self.__name = None  # название вакансии
        self.__link = None  # ссылка на вакансию
        self.__correct_salary = None  # зарплата
        self.__currency = None  # валюта заработной платы
        self.__requirement = None  # требования
        self.__responsibility = None  # обязанности
        self.__address = None   # адрес вакансии
        self.__metro = None  # станция метро на которой находиться вакансия
        self.__experience = None  # требуемый опыт работы для данной вакансии
        self.__employer = None  # название компании
        self.__area = None  # город вакансии

    def save_hh(self):
        """Выбираем данные с которыми будет работать далее и сохраняем их словарь"""
        with open(f'../json_dir/HH.json', 'r', encoding="utf-8") as file:
            data = json.load(file)
            for num, value in enumerate(data['items']):
                self.__name = value['name']  # название вакансии
                salary = value['salary']  # Данные по заработное плате
                salary_from = salary['from'] if isinstance(value['salary'], dict) \
                    and salary['from'] is not None else 0  # итоговый порог заработной платы
                salary_to = salary['to'] if isinstance(value['salary'], dict) \
                    and salary['to'] is not None else 0  # начальный порог заработной платы
                self.__currency = salary['currency'] if isinstance(value['salary'], dict) \
                    else "Уточнить у работодателя"  # валюта заработной платы
                # Здесь начинается расчет и конвертация заработной платы
                # Курс может немного отличаться от нынешнего
                self.__correct_salary = salary_from if salary_from > salary_to else salary_to
                if self.__currency == "Уточнить у работодателя":
                    self.__correct_salary = ''
                elif self.__currency == "KZT":
                    self.__correct_salary = int(self.__correct_salary * 0.19)
                    self.__currency = "RUR"
                elif self.__currency == "BYR":
                    self.__correct_salary = int(self.__correct_salary * 33.07)
                    self.__currency = "RUR"
                elif self.__currency == "KGS":
                    self.__correct_salary = int(self.__correct_salary * 0.96)
                    self.__currency = "RUR"
                elif self.__currency == "UZS":
                    self.__correct_salary = int(self.__correct_salary * 0.0073)
                    self.__currency = "RUR"
                elif self.__currency == "USD":
                    self.__correct_salary = int(self.__correct_salary * 84.55)
                    self.__currency = "RUR"
                elif self.__currency == "EUR":
                    self.__correct_salary = int(self.__correct_salary * 91.05)
                    self.__currency = "RUR"
                self.__link = value['alternate_url']  # ссылка на вакансию
                self.__employer = value['employer']['name']  # название компании
                self.__requirement = value['snippet']['requirement']  # требования
                self.__responsibility = value['snippet']['responsibility'] \
                    if value['snippet']['responsibility'] is not None else "Уточнить у работодателя"  # обязанности
                self.__address = value['address']['raw'] if isinstance(value['address'], dict) \
                    else "Уточнить у работодателя"  # адрес вакансии
                self.__metro = value['address']['metro']['station_name'] if isinstance(value['address'], dict) \
                    and value['address']['metro'] is not None else "Уточнить у работодателя"  # станция метро вакансии
                self.__area = value['area']['name']  # город вакансии
                self.__experience = value["experience"]["name"]  # требуемый опыт работы для данной вакансии
                all_info = {"название вакансии": self.__name, "ссылка на вакансию": self.__link,
                            "зарплата": self.__correct_salary, "валюта": self.__currency, "требования": self.__requirement,
                            "обязанности": self.__responsibility, "адрес": self.__address, "метро": self.__metro,
                            "требуемый опыт": self.__experience, "название компании": self.__employer, "город вакансии": self.__area}
                self.job_hh.append(all_info)

    def save_sj(self):
        """Выбираем данные с которыми будет работать далее и сохраняем их словарь"""
        with open(f'../json_dir/SuperJob.json', 'r', encoding="utf-8") as file:
            data = json.load(file)
            for index, value in enumerate(data["items"]):
                self.__name = value["profession"]  # название вакансии
                self.__link = value["link"]  # ссылка на вакансию
                s_from = value["payment_from"] if value["payment_from"]\
                    is not None else 0   # начальный порог заработной платы
                s_to = value["payment_to"] if value["payment_to"] \
                    is not None else 0  # итоговый порог заработной платы
                self.__correct_salary = s_from if s_from > s_to else s_to
                self.__currency = value["currency"]  # валюта заработной платы
                self.__responsibility = value['vacancyRichText']  # обязанности. требования. предложения
                self.__responsibility = re.sub('<.*?>', '', self.__responsibility) \
                    if self.__responsibility is not None else ""
                self.__address = value["address"] if value["address"] \
                    is not None else "Уточнить у работодателя"  # адрес вакансии
                self.__metro = value["metro"][0]["title"] if value["metro"] != [] \
                    else "Уточнить у работодателя"  # станция метро на которой находиться вакансия
                self.__experience = value["experience"]["title"]  # требуемый опыт работы для данной вакансии
                self.__employer = value["firm_name"]  # название компании
                all_info = {"название вакансии": self.__name, "ссылка на вакансию": self.__link,
                            "зарплата": self.__correct_salary, "валюта": self.__currency,
                            "обязанности": self.__responsibility, "адрес": self.__address,
                            "метро": self.__metro, "опыт": self.__experience, "название компании": self.__employer}
                self.job_sj.append(all_info)

    def run(self):
        """Метод для запуска функций и сохранения в словари с двух файлов"""
        self.save_hh()
        self.save_sj()

    def __eq__(self, other):
        """Метод для равенства =="""
        self.run()
        return self.job_sj == self.job_hh

    def __ne__(self, other):
        """Метод для неравенства !="""
        self.run()
        return self.job_sj != self.job_hh

    def __lt__(self, other):
        """Метод для оператора меньше <"""
        self.run()
        return self.job_sj < self.job_hh

    def __le__(self, other):
        """Метод для оператора меньше или равно <="""
        self.run()
        return self.job_sj <= self.job_hh

    def __gt__(self, other):
        """Метод для оператора больше >"""
        self.run()
        return self.job_sj > self.job_hh

    def __ge__(self, other):
        """Метод для оператора больше или равно >="""
        self.run()
        return self.job_sj >= self.job_hh







