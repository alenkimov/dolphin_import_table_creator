from utils import bool_question
import json
from os import path, listdir
from pathlib import Path


class Config:
    def __init__(self,refresh_cookies=True, refresh_proxies=True):
        self.proxies_path = None
        self.cookies_path = None
        self.first_row = None
        self.second_row = None
        self.proxy_type = "http"
        self.proxy_types = ("http", "https", "socks5", "ssh")

        self.load_proxies_path_from_config_json()
        self.load_cookies_path_from_config_json()
        self.load_rows_from_config_json()

        if refresh_cookies:
            self.refresh_cookies_path()

        if refresh_proxies:
            self.refresh_proxies_path()

    def load_proxies_path_from_config_json(self) -> bool:
        with open("config.json", "r") as file:
            data = json.load(file)

        if data["proxies_path"] is None or path.exists(data["proxies_path"]):
            self.proxies_path = data["proxies_path"]
            return True
        else:
            print(f'Файл прокси по пути \"{data["proxies_path"]}\" не найден!')
            self.change_proxies_path(None)
            return False

    def load_cookies_path_from_config_json(self) -> bool:
        with open("config.json", "r") as file:
            data = json.load(file)

        if data["cookies_path"] is None or path.exists(data["cookies_path"]):
            self.cookies_path = data["cookies_path"]
            return True
        else:
            print(f'Папка с cookie по пути \"{data["cookies_path"]}\" не найдена!')
            self.change_cookies_path(None)
            return False

    def load_proxy_type_from_config_json(self) -> bool:
        with open("config.json", "r") as file:
            data = json.load(file)

        if data["proxy_type"] in self.proxy_types:
            self.proxy_type = data["proxy_type"]
            return True
        else:
            print("Неверный тип прокси!")
            self.change_cookies_path("http")
            return False

    def load_rows_from_config_json(self):
        with open("config.json", "r") as file:
            data = json.load(file)

        self.first_row = data["first_row"]
        self.second_row = data["second_row"]

    def change_proxies_path(self, new_proxies_path) -> bool:
        if new_proxies_path is None or path.exists(new_proxies_path):
            with open("config.json", "r") as file:
                data = json.load(file)
            data["proxies_path"] = new_proxies_path
            with open("config.json", "w") as file:
                json.dump(data, file, indent=4)
            self.load_proxies_path_from_config_json()
            return True
        else:
            print("Файл не найден!")
            return False

    def change_cookies_path(self, new_cookies_path) -> bool:
        if new_cookies_path is None or path.exists(new_cookies_path):
            with open("config.json", "r") as file:
                data = json.load(file)
            data["cookies_path"] = new_cookies_path
            with open("config.json", "w") as file:
                json.dump(data, file, indent=4)
            self.load_cookies_path_from_config_json()
            return True
        else:
            print("Файл не найден!")
            return False

    def change_proxy_type(self, new_proxy_type) -> bool:
        if new_proxy_type in (None, self.proxy_type):
            return True
        elif new_proxy_type in self.proxy_types:
            with open("config.json", "r") as file:
                data = json.load(file)
            data["proxy_type"] = new_proxy_type
            with open("config.json", "w") as file:
                json.dump(data, file, indent=4)
            self.load_proxy_type_from_config_json()
            return True
        else:
            print("Неверный тип прокси!")
            return False

    def get_proxies(self) -> tuple:
        if self.proxies_path:
            with open(self.proxies_path, "r") as file:
                return tuple(proxy.strip() for proxy in file.readlines())
        else:
            return tuple()

    def get_cookies(self) -> list:
        cookies = list()
        for filename in listdir(self.cookies_path):
            with open(path.join(self.cookies_path, filename), 'r') as file:
                cookies.append(file.read())
        return cookies

    def get_profile_names(self) -> list:
        profile_names = list()

        file_names = listdir(self.cookies_path)
        for file_name in file_names:
            profile_names.append(str(file_name).replace("dolphin-anty-cookies-", "").replace(".txt", ""))

        return profile_names

    def print_proxies_from_proxies_file(self, length=5):
        proxies = self.get_proxies()
        if proxies:
            print(f"Найдено {len(proxies)} прокси:")
            if len(proxies) > length:
                for i in range(length):
                    print(proxies[i])
                print("...")
            else:
                for proxy in proxies:
                    print(proxy)
        else:
            print("Указанный файл с прокси пустой!")

    def print_cookie_files(self, length=5):
        folder = Path(self.cookies_path)
        file_names = list(folder.iterdir())
        if file_names:
            print(f"В папке \"{self.cookies_path}\" содержиться {len(file_names)} файлов:")
            if len(file_names) > length:
                for i in range(length):
                    print(file_names[i].name)
                print("...")
            else:
                for file_name in file_names:
                    print(file_name.name)
        else:
            print("Указанная папка пуста!")

    def refresh_proxies_path(self):
        if self.proxies_path:
            print(f"Ранее был указан файл по пути \"{self.proxies_path}\"")
            self.print_proxies_from_proxies_file()
            print("Хотите использовать этот файл (Y) или хотите указать новый файл / не использовать прокси вовсе (N)?")
            if bool_question():
                return

        while True:
            print("Укажите путь до файла (например: \"proxies.txt\") либо оставьте ввод пустым (Enter), если прокси не используются")
            new_proxies_path = input(">> ")
            if not new_proxies_path:
                new_proxies_path = None
                if self.change_proxies_path(new_proxies_path):
                    print("Продолжить (Y)? Таким образом, прокси не будут заполнены")
                    if bool_question():
                        break
            else:
                if self.change_proxies_path(new_proxies_path):
                    self.print_proxies_from_proxies_file()
                    print("Продолжить (Y) или указать другой путь (N)?")
                    if bool_question():
                        self.refresh_proxy_type()
                        break

    def refresh_cookies_path(self):
        if self.cookies_path:
            self.print_cookie_files()
            print("Хотите использовать эту папку (Y) или хотите указать другой путь (N)?")
            if bool_question():
                return

        while True:
            print("Укажите путь до файла (например: \"cookies\")")
            new_cookies_path = input(">> ")
            if self.change_cookies_path(new_cookies_path):
                self.print_cookie_files()
                print("Продолжить (Y) или указать другой путь (N)?")
                if bool_question():
                    break

    def refresh_proxy_type(self):
        print(f"Установлен тип прокси \"{self.proxy_type}\"")
        print(f"Введите тип прокси для изменения {self.proxy_types} или оставьте ввод пустым, чтобы продолжить")
        while True:
            new_proxy_type = input(">> ")
            if not new_proxy_type: new_proxy_type = None
            if self.change_proxy_type(new_proxy_type):
                print(f"Установлен тип прокси \"{self.proxy_type}\"")
                break
