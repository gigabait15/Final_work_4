from work_class.HH import HH
from work_class.Super_job import SuperJob

class JobSearch:
    def __init__(self):
        self.hh = HH()
        self.superjob = SuperJob()
        self.job_platforms = {
            "1": self.hh,
            "2": self.superjob
        }

    def display_menu(self):
        """Функция выбора пользователем дальнейших действий"""
        print("=== Меню поиска работы ===")
        print("1. Получить список вакансий с HeadHunter (hh.ru)")
        print("2. Получить список вакансий с SuperJob (superjob.ru)")
        print("3. Поиск вакансий")
        print("4. Получить топ N вакансий по зарплате(указать количество вакансий)")
        print("5. Получить отсортированный список вакансий(указать количество вакансий)")
        print("6. Поиск вакансий по ключевым словам")
        print("7. Добавление новой вакансии")
        print("8. Удаление вакансии")
        print("0. Выход")

    def fetch_job_listings(self, platform):
        """Функция для получения вакансий с платформы
        и сохранения их в json файл по названию платформы"""
        if platform not in self.job_platforms:
            print("Недопустимая платформа. Пожалуйста, попробуйте ещё раз.")
            return

        job_platform = self.job_platforms[platform]
        filename = f"{job_platform.__class__.__name__}_listings"
        job_platform.dump_json(filename)
        print(f"Список вакансий получен с {job_platform.__class__.__name__} и сохранён в файле {filename}.json")

    def load_jod_listings(self):
        """Функция для открытия записанных файлов и объединения их в один список"""
        filename1 = f"{self.job_platforms['1'].__class__.__name__}_listings"
        filename2 = f"{self.job_platforms['2'].__class__.__name__}_listings"
        self.hh.loads_json(filename1)
        self.superjob.loads_json(filename2)
        self.all_job_listings = self.hh.all_job + self.superjob.all_job


    def search_job_listings(self, query):
        """Функция для поиска по названию вакансии"""
        if not query:
            print("Вы не ввели поисковый запрос. Пожалуйста, попробуйте ещё раз.")
            return
        self.load_jod_listings()
        matching_listings = [item for item in self.all_job_listings if query.lower() in item["название вакансии"].lower()]
        if matching_listings:
            print(f"Найдено {len(matching_listings)} вакансий, соответствующих запросу '{query}':")
            for item in matching_listings:
                print(*item.values())
        else:
            print("Вакансий, соответствующих поисковому запросу, не найдено.")

    def get_top_job_listings_by_salary(self, n):
        """ Получение отсортированного списка зарплат
        n - число вывода вакансий (Топ)"""
        if not isinstance(n, int):
            print("Введено недопустимое значение. Пожалуйста, введите число.")
            return

        self.load_jod_listings()

        sorted_listings = sorted(self.all_job_listings, key=lambda x: int(x["зарплата"]), reverse=True)
        top_n_listings = sorted_listings[:n]

        if top_n_listings:
            print(f"Топ {n} вакансий по зарплате"
                  f"(указана средняя зарплата, для получения более точной информации перейти по ссылке):")
            for item in top_n_listings:
                print(*item.values())
        else:
            print("Вакансий не найдено.")

    def get_sorted_job_listings(self, n):
        """Функция выводит отсортированный список вакансий"""
        self.load_jod_listings()

        sorted_listings = sorted(self.all_job_listings, key=lambda x: x["название вакансии"])
        top_n_listings = sorted_listings[:int(n)]

        if top_n_listings:
            print("Отсортированный список вакансий:")
            for item in top_n_listings:
                print(*item.values())
        else:
            print("Вакансий не найдено.")

    def search_job_listings_by_keywords(self, keywords):
        """Функция для поиска по ключевым словам"""
        if not keywords:
            print("Вы не ввели ключевые слова. Пожалуйста, попробуйте ещё раз.")
            return

        self.load_jod_listings()
        matching_listings = []
        for item in self.all_job_listings:
            item_values = [value for value in item.values()]
            if all(keyword.strip().capitalize() in item_values for keyword in keywords):
                matching_listings.append(item)

        if matching_listings:
            print(f"Найдено {len(matching_listings)} вакансий, соответствующих ключевым словам:")
            for item in matching_listings:
                print(item)
                print()
        else:
            print("Вакансий, соответствующих ключевым словам, не найдено.")


    def add_job_listing(self, job_listing):
        """Функция добавляет вакансию в список"""
        default_values = {
        "название вакансии": "","ссылка на вакансию": "","зарплата": 0,
                      "валюта": "","требования": "","обязанности": "","город": "","улица": "",
                      "метро": "","опыт": "","тип занятости": "","название компании": ""
        }

        # Заполняем отсутствующие значения по умолчанию
        for key, value in default_values.items():
            job_listing[key] = job_listing.get(key, value)

        self.all_job_listings.append(job_listing)
        print(f"Вакансия успешно добавлена.{job_listing}")

    def remove_job_listing(self, job_listing):
        """Функция удаляет вакансию из списка"""
        if job_listing in self.all_job_listings:
            self.all_job_listings.remove(job_listing)
            print("Вакансия успешно удалена.")
        else:
            print("Указанная вакансия не найдена в списке.")

    def run(self):
        """Функция для взаимодействия с пользователем"""
        while True:
            self.display_menu()
            choice = str(input("Введите ваш выбор: "))

            if choice == "0":
                print("Выход...")
                break

            elif choice == "1" or choice == "2":
                self.fetch_job_listings(choice)

            elif choice == "3":
                query = input("Введите поисковый запрос"
                              "(указать название вакансии или ключевое слово в названии): ")
                self.search_job_listings(query)

            elif choice == "4":
                n = input("Введите количество вакансий: ")
                self.get_top_job_listings_by_salary(n)

            elif choice == "5":
                n = input("Введите число вакансий для вывода: ")
                self.get_sorted_job_listings(n)

            elif choice == "6":
                keywords = input("Введите ключевые слова (через ;): ").split(";")
                print("вывод вакансий будет по всем содержащимся ключевым словам в вакансии")
                self.search_job_listings_by_keywords(keywords)
            elif choice == "7":
                print("введите данные для новой вакансии")
                job_listing = {"название вакансии": input("название вакансии:"), "ссылка на вакансию": input("ссылка на вакансию:"),
                               "зарплата": int(input("зарплата:")), "валюта": input("валюта:"),
                            "требования": input("требования:"), "обязанности": input("обязанности:"),
                               "город": input("город:"), "улица":input("улица:"),
                            "метро": input("метро:"), "опыт": input("опыт:"), "тип занятости": input("тип занятости:"),
                               "название компании": input("название компании:")}
                self.add_job_listing(job_listing)
            elif choice == "8":
                print("введите данные для удаления вакансии")
                job_listing = {"название вакансии": input("название вакансии:"),
                               "ссылка на вакансию": input("ссылка на вакансию:"),
                               "зарплата": int(input("зарплата:")), "валюта": input("валюта:"),
                               "требования": input("требования:"), "обязанности": input("обязанности:"),
                               "город": input("город:"), "улица": input("улица:"),
                               "метро": input("метро:"), "опыт": input("опыт:"),
                               "тип занятости": input("тип занятости:"),
                               "название компании": input("название компании:")}
                self.remove_job_listing(job_listing)
            else:
                print("Недопустимый выбор. Пожалуйста, попробуйте ещё раз.")

if __name__ == '__main__':
    js = JobSearch()
    js.run()

