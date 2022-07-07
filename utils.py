def bool_question() -> bool:
    while True:
        user_input = input("(Y,Enter/N) >> ").lower()
        if user_input not in ('y', 'n', ''):
            print("Неверный ответ! Введите Y, Enter или N")
        else:
            break

    if user_input in ('y', ''):
        return True
    else:
        return False

