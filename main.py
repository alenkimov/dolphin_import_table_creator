import openpyxl
from datetime import datetime
from config import Config


def main():
    config = Config()
    book = openpyxl.Workbook()
    sheet = book.active

    sheet.append(config.first_row)
    sheet.append(config.second_row)

    cookies = config.get_cookies()
    proxies = config.get_proxies()
    proxy_type = config.proxy_type

    number_of_proxies = 0
    if proxies:
        number_of_proxies = len(proxies)

    for i in range(len(cookies)):
        sheet[i + 3][0].value = i + 1
        sheet[i + 3][1].value = cookies[i]
        if i < number_of_proxies:
            sheet[i + 3][2].value = proxy_type
            sheet[i + 3][3].value = proxies[i]

    try:
        book.save(f"Dolphin_profiles_{datetime.now().date()}.xlsx")
    except PermissionError:
        print("Похоже, таблица уже открыта в другой программе. Закройти таблицу и попробуйте снова!")


if __name__ == '__main__':
    main()

