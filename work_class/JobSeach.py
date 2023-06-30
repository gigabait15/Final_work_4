import os
from pprint import pprint
from work_class.work_with_vacancies import Work_With_Vacancies
from work_class.JSON_LD import JSONLD


class JobSearch:
    def __init__(self):
        self.wwv = Work_With_Vacancies()
        self.jld = JSONLD()
        self.hh = self.wwv.save_hh()
        self.sj = self.wwv.save_sj()
        self.all_job_listings = self.wwv.job_hh + self.wwv.job_sj

    @staticmethod
    def display_menu():
        """Функция выбора пользователем дальнейших действий"""
        print("=== Меню поиска работы ===")
        print("1. Получить список вакансий")
        print("2. Поиск вакансий")
        print("3. Получить топ N вакансий по зарплате(указать количество вакансий)")
        print("4. Получить отсортированный список вакансий(указать количество вакансий)")
        print("5. Поиск вакансий по ключевым словам")
        print("6. Добавление новой вакансии")
        print("7. Удаление вакансии")
        print("8. Сохранить вакансию в файл")
        print("0. Выход")

    def run_listings(self):
        """Функция для записи списков рабочего класса """
        self.wwv.save_hh()
        self.wwv.save_sj()

    def fetch_job_listings(self):
        """Функция для получения вакансий в полном формате"""
        pprint(self.all_job_listings)

    def search_job_listings(self, query):
        """Функция для поиска по названию вакансии"""
        if not query:
            print("Вы не ввели поисковый запрос. Пожалуйста, попробуйте ещё раз.")
            return
        matching_listings = [item for item in self.all_job_listings if
                             query.lower() in item["название вакансии"].lower()]
        if matching_listings:
            print(f"Найдено {len(matching_listings)} вакансий, соответствующих запросу '{query}':")
            for item in matching_listings:
                print(f"Должность: {item['название вакансии']}\n"
                      f"Ссылка для отклика: {item['ссылка на вакансию']}\n"
                      f"Размер заработной платы: {item['зарплата']} {item['валюта']}\n"
                      f"Адрес: {item['адрес']}\n")
        else:
            print("Вакансий, соответствующих поисковому запросу, не найдено.")

    def get_top_job_listings_by_salary(self, n):
        """ Получение отсортированного списка зарплат
        n - число вывода вакансий (Топ)"""
        if not isinstance(n, int):
            print("Введено недопустимое значение. Пожалуйста, введите число.")
            return
        sorted_listings = sorted(self.all_job_listings, key=lambda x: int(x["зарплата"])
            if x.get("зарплата") else 0, reverse=True)
        top_n_listings = sorted_listings[:n]

        if top_n_listings:
            print(f"Топ {n} вакансий по зарплате "
                  f"(указана средняя зарплата, для получения более точной информации перейти по ссылке):")
            for num, item in enumerate(top_n_listings):
                print(f"Номер {num + 1}\n"
                      f"Должность: {item['название вакансии']}\n"
                      f"Ссылка для отклика: {item['ссылка на вакансию']}\n"
                      f"Размер заработной платы: {item['зарплата']} {item['валюта']}\n"
                      f"Адрес: {item['адрес']}\n")
        else:
            print("Вакансий не найдено.")

    def get_sorted_job_listings(self, n):
        """Функция выводит отсортированный список вакансий"""

        sorted_listings = sorted(self.all_job_listings, key=lambda x: x["название вакансии"])
        top_n_listings = sorted_listings[:int(n)]

        if top_n_listings:
            print("Отсортированный список вакансий:")
            for item in top_n_listings:
                print(f"Должность: {item['название вакансии']}\n"
                      f"Ссылка для отклика: {item['ссылка на вакансию']}\n"
                      f"Размер заработной платы: {item['зарплата']} {item['валюта']}\n"
                      f"Адрес: {item['адрес']}\n")
        else:
            print("Вакансий не найдено.")

    def search_job_listings_by_keywords(self, keywords):
        """Функция для поиска по ключевым словам"""
        if not keywords:
            print("Вы не ввели ключевые слова. Пожалуйста, попробуйте ещё раз.")
            return
        matching_listings = []
        for item in self.all_job_listings:
            item_values = [value for value in item.values()]
            if all(keyword.strip().capitalize() in item_values for keyword in keywords):
                matching_listings.append(item)

        if matching_listings:
            print(f"Найдено {len(matching_listings)} вакансий, соответствующих ключевым словам:")
            for item in matching_listings:
                print(f"Должность: {item['название вакансии']}\n"
                      f"Ссылка для отклика: {item['ссылка на вакансию']}\n"
                      f"Размер заработной платы: {item['зарплата']} {item['валюта']}\n"
                      f"Адрес: {item['адрес']}\n")
        else:
            print("Вакансий, соответствующих ключевым словам, не найдено.")

    def add_job_listing(self, pick: int, job_listing: dict):
        """Функция добавляет вакансию в список"""
        self.jld.json_add(pick, job_listing)

    def remove_job_listing(self, pick: int, job_listing: dict):
        """Функция удаляет вакансию из списка"""
        self.jld.json_del(pick, job_listing)

    def run(self):
        """Функция для взаимодействия с пользователем"""
        self.run_listings()
        while True:
            self.display_menu()
            choice = int(input("Введите ваш выбор: "))

            if choice == 0:
                print("Выход...")
                break

            elif choice == 1:
                self.fetch_job_listings()

            elif choice == 2:
                query = input("Введите поисковый запрос"
                              "(указать название вакансии или ключевое слово в названии): ")
                self.search_job_listings(query)

            elif choice == 3:
                n = int(input("Введите количество вакансий: "))
                self.get_top_job_listings_by_salary(n)

            elif choice == 4:
                n = input("Введите число вакансий для вывода: ")
                self.get_sorted_job_listings(n)

            elif choice == 5:
                keywords = input("Введите ключевые слова (через ;): ").split(";")
                print("вывод вакансий будет по всем содержащимся ключевым словам в вакансии")
                self.search_job_listings_by_keywords(keywords)

            elif choice == 6:
                if not os.path.exists(__class__.directory):
                    print("С начало сохраните файл")
                else:
                    print("введите файл вакансии:\n"
                          "1 - HH\n"
                          "2 - SuperJob")
                    pick = int(input())
                    print("введите данные для новой вакансии")

                    job_listing = \
                        {"название вакансии": input("название вакансии:"),
                         "ссылка на вакансию": input("ссылка на вакансию:"),
                         "зарплата": int(input("зарплата:")), "валюта": input("валюта:"),
                         "требования": input("требования:"), "обязанности": input("обязанности:"), "адрес": input("адрес:"),
                         "метро": input("метро:"), "требуемый опыт": input("требуемый опыт:"),
                         "название компании": input("название компании:"), "город вакансии": input("город вакансии:")
                         }
                    self.add_job_listing(pick, job_listing)

            elif choice == 7:
                if not os.path.exists(__class__.directory):
                    print("С начало сохраните файл")
                else:
                    print("введите файл вакансии:\n"
                          "1 - HH\n"
                          "2 - SuperJob")
                    pick = int(input())
                    print("введите данные для удаления вакансии")

                    job_listing = \
                        {"название вакансии": input("название вакансии:"),
                         "ссылка на вакансию": input("ссылка на вакансию:"),
                         "зарплата": int(input("зарплата:")), "валюта": input("валюта:"),
                         "требования": input("требования:"), "обязанности": input("обязанности:"),
                         "адрес": input("адрес:"), "метро": input("метро:"),
                         "требуемый опыт": input("требуемый опыт:"), "название компании": input("название компании:"),
                         "город вакансии": input("город вакансии:")
                         }

                    self.remove_job_listing(pick, job_listing)

            elif choice == 8:
                print("Сохранить файл с вакансиями:\n"
                      "1 - HH\n"
                      "2 - SuperJob")
                pick = int(input("введите номер:"))
                self.jld.json_save(pick)

            else:
                print("Недопустимый выбор. Пожалуйста, попробуйте ещё раз.")


