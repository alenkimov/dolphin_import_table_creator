from utils import bool_question
import openpyxl
from datetime import datetime
from config import Config
from prettytable import PrettyTable
import json


class Table(Config):
    def __init__(self, sorting_type=None, refresh_sorting_type=True, **kwargs):
        super().__init__(**kwargs)
        self.book = openpyxl.Workbook()
        self.sheet = self.book.active
        self.sheet.append(self.first_row)
        self.sheet.append(self.second_row)

        if sorting_type is not None:
            self.change_sorting_type(sorting_type)
        else:
            self.load_sorting_type_from_config_json()
            if refresh_sorting_type:
                self.refresh_sorting_type()

    def show_preview(self):
        table = PrettyTable(self.first_row)

        profile_names = self.get_profile_names()
        cookies = self.get_cookies()
        proxies = self.get_proxies()
        proxy_type = self.proxy_type

        number_of_proxies = 0
        if proxies:
            number_of_proxies = len(proxies)

        for i in range(len(profile_names)):
            preview_data = [profile_names[i], str(cookies[i])[:15]]
            if i < number_of_proxies:
                preview_data.append(proxy_type)
                preview_data.append(proxies[i].split(':', 1)[0])
            else:
                preview_data.extend(('', ''))

            preview_data.extend(('', ''))
            table.add_row(preview_data)
        print()
        print("Получилась следующая таблица:")
        print(table)

    def refresh_sorting_type(self):
        while True:
            self.show_preview()
            print(self.sorting_descriptions[self.sorting_type])
            print("Внимание! Сортируются только названия профилей и их cookie данные! Колонка прокси остается неизменной!")
            print(f"Введите тип сортировки для изменения {self.sorting_types} или оставьте ввод пустым, чтобы продолжить")
            new_sorting_type = input(">> ")
            if not new_sorting_type:
                break
            self.change_sorting_type(new_sorting_type)

    def create(self):
        profile_names = self.get_profile_names()
        cookies = self.get_cookies()
        proxies = self.get_proxies()
        proxy_type = self.proxy_type

        number_of_proxies = 0
        if proxies:
            number_of_proxies = len(proxies)

        for i in range(len(profile_names)):
            data = [profile_names[i], cookies[i]]
            if i < number_of_proxies:
                data.append(proxy_type)
                data.append(proxies[i])
            self.sheet.append(data)

    def save(self):
        self.show_preview()
        try:
            table_name = f"Dolphin_profiles_{datetime.now().date()}.xlsx"
            self.book.save(table_name)
            print(f"Таблица {table_name} успешно создана!")
        except PermissionError:
            print("Похоже, таблица уже открыта в другой программе. Закройти таблицу и попробуйте снова!")