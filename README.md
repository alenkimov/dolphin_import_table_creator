# Dolphin import table creator
-> [Статья на teletype](https://teletype.in/@alenkimov/dolphin_import_table_creator)

В первую очередь нам нужно [скачать](https://www.python.org/downloads/) и установить Python.

Далее [скачиваем](https://github.com/AlenKimov/dolphin_import_table_creator/archive/refs/heads/main.zip) и распаковываем проект.

Для удобства в папке со скриптом создаем новую папку и перемещаем туда экспортированные `.txt` файлы *cookie*. Также рядом со скриптом помещаем файл с прокси (если используются). Прокси должны быть вида:
```
192.168.0.1:8000:login:password
или
login:password@host:port
```

Запускаем **start.bat**: этот файл установит отсутствующие библиотеки и запустит скрипт. На выходе получим нужный нам `.xlsx` файл. Удачного импорта!
