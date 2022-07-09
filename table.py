import openpyxl
from datetime import datetime
from config import Config
from prettytable import PrettyTable


class Table(Config):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.book = openpyxl.Workbook()
        self.sheet = self.book.active
        self.sheet.append(self.first_row)
        self.sheet.append(self.second_row)

        self.profile_names = self.get_profile_names()
        self.cookies = self.get_cookies()
        self.proxies = self.get_proxies()

        self.table = PrettyTable(self.first_row)

    def create(self):
        number_of_proxies = 0
        if self.proxies:
            number_of_proxies = len(self.proxies)

        for i in range(len(self.profile_names)):
            data = [self.profile_names[i], self.cookies[i]]
            if i < number_of_proxies:
                data.append(self.proxy_type)
                data.append(self.proxies[i])

            self.sheet.append(data)
            preview_data = [self.profile_names[i], str(self.cookies[i])[:15]]
            if i < number_of_proxies:
                preview_data.append(self.proxy_type)
                preview_data.append(self.proxies[i].split(':', 1)[0])
            else:
                preview_data.extend(('', ''))

            preview_data.extend(('', ''))
            self.table.add_row(preview_data)

        print()
        print("Получилась следующая таблица:")
        print(self.table)

        try:
            table_name = f"Dolphin_profiles_{datetime.now().date()}.xlsx"
            self.book.save(table_name)
            print(f"Таблица {table_name} успешно создана!")
        except PermissionError:
            print("Похоже, таблица уже открыта в другой программе. Закройти таблицу и попробуйте снова!")