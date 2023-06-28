import json
from work_class.REQUEST_CLASS import HH, SuperJob
from work_class.ABSTRACT_CLASS import Abstract_JSON


class JSONLD(Abstract_JSON):

    def __init__(self):
        super().__init__()
        self.hh = HH()
        self.sj = SuperJob()
        self.choices = {1: self.hh,
                        2: self.sj
                        }

    def json_save(self, pick: int):
        """Функция для создания файла
         и сохранения вакансии в него"""
        choice = self.choices[pick]
        with open(f'../json_dir/{choice.__class__.__name__}.json', 'w', encoding="utf-8") as file:
            json.dump({"items": choice.requests_json()}, file, ensure_ascii=False, indent=2)

    def json_get(self, pick: int):
        """Функция для получения вакансии из файла"""
        choice = self.choices[pick]
        with open(f'../json_dir/{choice.__class__.__name__}.json', 'r', encoding="utf-8") as file:
            data = json.load(file)
            return data

    def json_del(self, pick: int, value: dict):
        """Функция для удаления вакансии из файла"""
        choice = self.choices[pick]
        with open(f'../json_dir/{choice.__class__.__name__}.json', 'r', encoding="utf-8") as file:
            data = json.load(file)

        for items in data["items"]:
            if items == value:
                del items

        with open(f'../json_dir/{choice.__class__.__name__}.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def json_add(self, pick: int, value: dict):
        """Функция для добавления вакансии из файла"""
        choice = self.choices[pick]
        with open(f'../json_dir/{choice.__class__.__name__}.json', 'r', encoding="utf-8") as file:
            data = json.load(file)

            data["items"].expend(value)

        with open(f'../json_dir/{choice.__class__.__name__}.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)


