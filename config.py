from utils import bool_question
import json
from os import path, listdir
from pathlib import Path
from os.path import getctime, getmtime


class Config:
    def __init__(self, proxies_path=None, cookies_path=None, proxy_type=None,
                 refresh_cookies=True, refresh_proxies=True):
        self.first_row = None
        self.second_row = None
        self.load_rows_from_config_json()

        self.sorting_type = "ctime"
        self.sorting_types = ("ctime", "mtime", "name", "num")
        self.sorting_descriptions = {"ctime": "Сортировка по дате создания файла cookie",
                                     "mtime": "Сортировка по дате изменения файла cookie",
                                     "name": "Сортировка по имени файла cookie",
                                     "num": "Сортировка по имени файла cookie, если имя профиля представляет число"}
        self.reversed_sorting = False
        self.load_sorting_type_from_config_json()

        self.proxies_path = None
        if proxies_path is not None:
            self.change_proxies_path(proxies_path)
        else:
            self.load_proxies_path_from_config_json()
            if refresh_proxies:
                self.refresh_proxies_path()

        self.cookies_path = None
        if cookies_path is not None:
            self.change_cookies_path(cookies_path)
        else:
            self.load_cookies_path_from_config_json()
            if refresh_cookies:
                self.refresh_cookies_path()

        self.proxy_type = "http"
        self.proxy_types = ("http", "https", "socks5", "ssh")
        if proxy_type is not None:
            self.change_proxy_type(proxy_type)
        else:
            self.load_proxy_type_from_config_json()

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
            self.change_proxy_type("http")
            return False

    def load_rows_from_config_json(self):
        with open("config.json", "r") as file:
            data = json.load(file)

        self.first_row = data["first_row"]
        self.second_row = data["second_row"]

    def load_sorting_type_from_config_json(self):
        with open("config.json", "r") as file:
            data = json.load(file)

        if data["sorting_type"] in self.sorting_types:
            self.sorting_type = data["sorting_type"]
            return True
        else:
            print("Неверный тип сортировки!")
            self.change_sorting_type("ctime")
            return False

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

    def get_sorted_by_ctime_cookie_paths(self, reverse=False) -> list:
        folder = Path(self.cookies_path)
        paths = list(folder.iterdir())
        paths.sort(key=getctime, reverse=reverse)
        return paths

    def get_sorted_by_mtime_cookie_paths(self, reverse=False) -> list:
        folder = Path(self.cookies_path)
        paths = list(folder.iterdir())
        paths.sort(key=getmtime, reverse=reverse)
        return paths

    def get_sorted_by_name_cookie_paths(self, reverse=False) -> list:
        folder = Path(self.cookies_path)
        paths = list(folder.iterdir())
        paths.sort(reverse=reverse)
        return paths

    @staticmethod
    def num_sorting(path):
        return int(str(path.name).replace("dolphin-anty-cookies-", "").replace(".txt", ""))

    def get_sorted_by_number_cookie_paths(self, reverse=False) -> list:
        folder = Path(self.cookies_path)
        paths = list(folder.iterdir())
        paths.sort(reverse=reverse, key=self.num_sorting)
        return paths

    def get_sorted_cookie_paths(self, sorting_type, reverse=False):
        if sorting_type == "ctime":
            return self.get_sorted_by_ctime_cookie_paths(reverse)
        elif sorting_type == "mtime":
            return self.get_sorted_by_mtime_cookie_paths(reverse)
        elif sorting_type == "name":
            return self.get_sorted_by_name_cookie_paths(reverse)
        elif sorting_type == "num":
            try:
                return self.get_sorted_by_number_cookie_paths(reverse)
            except:
                print("Невозможно отсортировать по номеру профиля: в названии профилей содержаться буквы")
                self.change_sorting_type("name")
                return self.get_sorted_cookie_paths(self.sorting_type, reverse)

    def get_cookies(self) -> list:
        cookies = list()
        cookie_paths = self.get_sorted_cookie_paths(self.sorting_type, self.reversed_sorting)
        for path in cookie_paths:
            with open(path, 'r') as file:
                cookies.append(file.read())
        return cookies

    def get_profile_names(self) -> list:
        profile_names = list()

        file_names = [path.name for path in self.get_sorted_cookie_paths(self.sorting_type, self.reversed_sorting)]
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
        cookie_paths = self.get_sorted_cookie_paths(self.sorting_type, self.reversed_sorting)
        if cookie_paths:
            print(f"В папке \"{self.cookies_path}\" содержиться {len(cookie_paths)} файлов:")
            if len(cookie_paths) > length:
                for i in range(length):
                    print(cookie_paths[i].name)
                print("...")
                print(self.sorting_descriptions[self.sorting_type])
                print("Тип сортировки можно будет изменить потом")
            else:
                for file_name in cookie_paths:
                    print(file_name.name)
                print(self.sorting_descriptions[self.sorting_type])
        else:
            print("Указанная папка пуста!")

    def refresh_proxies_path(self):
        if self.proxies_path:
            print(f"Ранее был указан файл по пути \"{self.proxies_path}\"")
            self.print_proxies_from_proxies_file()
            print("Хотите использовать этот файл (Y)? Или хотите указать новый файл / изменить тип прокси / не использовать прокси вовсе (N)?")
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

    def change_sorting_type(self, new_sorting_type) -> bool:
        if new_sorting_type in (None, self.proxy_type):
            return True
        elif new_sorting_type in self.sorting_types:
            with open("config.json", "r") as file:
                data = json.load(file)
            data["sorting_type"] = new_sorting_type
            with open("config.json", "w") as file:
                json.dump(data, file, indent=4)
            self.load_sorting_type_from_config_json()
            return True
        else:
            print("Неверный тип сортировки!")
            return False
