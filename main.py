import openpyxl
from datetime import datetime
from config import Config
from prettytable import PrettyTable


def main():
    config = Config()
    book = openpyxl.Workbook()
    sheet = book.active

    table = PrettyTable(config.first_row)

    sheet.append(config.first_row)
    sheet.append(config.second_row)

    profile_names = config.get_profile_names()
    cookies = config.get_cookies()
    proxies = config.get_proxies()
    proxy_type = config.proxy_type

    number_of_proxies = 0
    if proxies:
        number_of_proxies = len(proxies)

    for i in range(len(profile_names)):
        data = [profile_names[i], cookies[i]]
        if i < number_of_proxies:
            data.append(proxy_type)
            data.append(proxies[i])

        sheet.append(data)
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

    try:
        table_name = f"Dolphin_profiles_{datetime.now().date()}.xlsx"
        book.save(table_name)
        print(f"Таблица {table_name} успешно создана!")
    except PermissionError:
        print("Похоже, таблица уже открыта в другой программе. Закройти таблицу и попробуйте снова!")


if __name__ == '__main__':
    main()

