import datetime
from datetime import datetime

from project_config import *
from tables.people_table import *
from tables.phones_table import *
from tables.docs_table import *


def date_format_check(date):
    try:
        datetime.strptime(date, '%d.%m.%Y')
        return True
    except ValueError:
        return False


def date_check(date):
    try:
        date = datetime.strptime(date, '%d.%m.%Y').date()
        present = datetime.today().date()
    except ValueError:
        return False
    if present < date:
        return False
    else:
        return True


def int_format_check(num):
    try:
        int(num)
        return True
    except ValueError:
        return False


def number_check(num):
    try:
        int(num)
        num = int(num)
    except ValueError:
        return False
    if num <= 0:
        return False
    else:
        return True


class Main:
    config = ProjectConfig()
    connection = DbConnection(config)

    def __init__(self):
        DbTable.dbconn = self.connection
        return

    def db_init(self):
        pt = PeopleTable()
        pht = PhonesTable()
        dt = DocsTable()
        pt.create()
        pht.create()
        dt.create()
        return

    def db_insert_somethings(self):
        pt = PeopleTable()
        pht = PhonesTable()
        dt = DocsTable()
        pt.insert_one(["LastName1", "FirstName1", "SecondName1"])
        pt.insert_one(["LastName2", "FirstName2", "SecondName2"])
        pt.insert_one(["LastName3", "FirstName3", "SecondName3"])
        pht.insert_one([1, "111"])
        pht.insert_one([2, "222"])
        pht.insert_one([3, "333"])
        dt.insert_one([2, "insurance", "2121", "2211", "02.02.2002"])
        dt.insert_one([1, "driving licence", "1111", "1", "03.03.2003"])
        dt.insert_one([3, "passport", "3131", "333111", "01.01.2001"])

    def db_drop(self):
        dt = DocsTable()
        pht = PhonesTable()
        pt = PeopleTable()
        dt.drop()
        pht.drop()
        pt.drop()

        return

    def show_main_menu(self):
        menu = """Добро пожаловать! 
Основное меню (выберите цифру в соответствии с необходимым действием): 
    1 - просмотр людей;
    2 - сброс и инициализация таблиц;
    9 - выход."""
        print(menu)
        return

    def read_next_step(self):
        next_step = input("=> ").strip()
        while next_step == "input_err":
            print("Выбран не верный пункт меню! Повторите ввод!")
            next_step = input("=> ").strip()
        return next_step

    def show_people(self):
        self.person_id = -1
        menu = """Просмотр списка людей!
№         Фамилия             Имя                 Отчество"""
        print(menu)
        lst = PeopleTable().all()
        num = 1
        for i in lst:
            print(str(num).ljust(10) + str(i[1]).ljust(20) + str(i[2]).ljust(20) + str(i[3]).ljust(20))
            num += 1
        menu = """Дальнейшие операции: 
    0 - возврат в главное меню;
    3 - добавление нового человека;
    4 - удаление человека;
    5 - изменение информации о человеке;
    6 - просмотр телефонов человека;
    7 - просмотр докуметов человека;
    8 - постраничный просмотр людей;
    9 - выход."""
        print(menu)
        return

    def pages_menu_transporter(self):
        lim = input("Введите количество записей на странице (-1 - отмена): ")
        if lim == "-1":
            return
        while not int_format_check(lim):
            lim = input(
                "Число страниц должно быть числом! Повторно введите количество записей на странице (-1 - отмена): ")
            if lim == -1:
                return
        while not number_check(lim):
            lim = input(
                "Число страниц должно быть положительно! Повторно введите количество записей на странице (-1 - отмена): ")
            if lim == -1:
                return

        menu = """Дальнейшие операции: 
    1 - вывести следующую страницу;
    2 - вывести предыдущую страницу;
    3 - вывести страницу по номеру;
    -1 - выход;
    -2 - изменить число записей на странице."""
        print(menu)
        page = 0
        rows_total = PeopleTable().count_check()

        while True:
            stage = self.read_next_step()

            if stage == "-1":
                return

            elif stage == "1":
                page = int(page)
                if (page + 1) * int(lim) <= int(rows_total[0] + int(lim) - 1):
                    page += 1
                    t = 1
                    lst = PeopleTable().print_list(int(lim), page * int(lim) - int(lim))
                    print(f"Страница {page}")
                    print("{:<10}{:<20}{:<20}{:<20}".format("№", "Фамилия", "Имя", "Отчество"))
                    for i in lst:
                        print(f"{(page - 1) * int(lim) + t:<10}{i[1]:<20}{i[2]:<20}{i[3]:<20}")
                        t += 1
                else:
                    print(f"Страница {page} была последней")

                    if lim == "1":
                        l_page = int(rows_total[0]) // int(lim)
                    else:
                        l_page = (int(rows_total[0]) + 1) // int(lim)
                    t = 1
                    lst = PeopleTable().print_list(int(lim), l_page * int(lim) - int(lim))
                    print(f"Страница {l_page}")
                    print("{:<10}{:<20}{:<20}{:<20}".format("№", "Фамилия", "Имя", "Отчество"))
                    for i in lst:
                        print(f"{(l_page - 1) * int(lim) + t:<10}{i[1]:<20}{i[2]:<20}{i[3]:<20}")
                        t += 1
                print(menu)

            elif stage == "2":
                page = int(page)
                if (page - 1) * int(lim) > 0:
                    page -= 1
                    t = 1
                    lst = PeopleTable().print_list(int(lim), page * int(lim) - int(lim))
                    print(f"Страница {page}")
                    print("{:<10}{:<20}{:<20}{:<20}".format("№", "Фамилия", "Имя", "Отчество"))
                    for i in lst:
                        print(f"{(page - 1) * int(lim) + t:<10}{i[1]:<20}{i[2]:<20}{i[3]:<20}")
                        t += 1
                else:
                    print(f"Страница {page} первая")
                    f_page = 1
                    t = 1
                    lst = PeopleTable().print_list(int(lim), f_page * int(lim) - int(lim))
                    print(f"Страница {f_page}")
                    print("{:<10}{:<20}{:<20}{:<20}".format("№", "Фамилия", "Имя", "Отчество"))
                    for i in lst:
                        print(f"{(f_page - 1) * int(lim) + t:<10}{i[1]:<20}{i[2]:<20}{i[3]:<20}")
                        t += 1
                print(menu)

            elif stage == "3":
                prev_page = page
                if lim == "1":
                    print(
                        f"Введите номер страницы в диапазоне {1} - {int(rows_total[0]) // int(lim)} (-1 - отмена): ",
                        end='')
                else:
                    print(
                        f"Введите номер страницы в диапазоне {1} - {(int(rows_total[0]) + 1) // int(lim)} (-1 - отмена): ",
                        end='')
                page = input()
                if lim == -1:
                    page = prev_page
                    return
                while not int_format_check(page):
                    page = input(
                        "Число страниц должно быть числом! Повторно введите количество записей на странице (-1 - отмена): ")
                    if lim == -1:
                        page = prev_page
                        return
                if (lim != "1" and 0 < int(page) and int(page) <= (rows_total[0] + 1) // int(lim)):
                    t = 1
                    lst = PeopleTable().print_list(int(lim), int(page) * int(lim) - int(lim))
                    print(f"Страница {page}")
                    print("{:<10}{:<20}{:<20}{:<20}".format("№", "Фамилия", "Имя", "Отчество"))
                    for i in lst:
                        print(f"{(int(page) - 1) * int(lim) + t:<10}{i[1]:<20}{i[2]:<20}{i[3]:<20}")
                        t += 1
                elif (lim == "1" and 0 < int(page) and int(page) <= rows_total[0] // int(lim)):
                    t = 1
                    lst = PeopleTable().print_list(int(lim), int(page) * int(lim) - int(lim))
                    print(f"Страница {page}")
                    print("{:<10}{:<20}{:<20}{:<20}".format("№", "Фамилия", "Имя", "Отчество"))
                    for i in lst:
                        print(f"{(int(page) - 1) * int(lim) + t:<10}{i[1]:<20}{i[2]:<20}{i[3]:<20}")
                        t += 1
                else:
                    print(f"Страницы {page} не существует")
                    page = prev_page
                print(menu)
            elif stage == "-2":
                lim = input("Введите количество записей на странице (-1 - отмена): ")
                if lim == "-1":
                    return
                while not int_format_check(lim):
                    lim = input(
                        "Число страниц должно быть числом! Повторно введите количество записей на странице (-1 - отмена): ")
                    if lim == -1:
                        return
                while not number_check(lim):
                    lim = input(
                        "Число страниц должно быть положительно! Повторно введите количество записей на странице (-1 - отмена): ")
                    if lim == -1:
                        return
                page = 0
                print(menu)

            else:
                print("Повторите ввод!")

    def show_add_person(self):
        data = []
        data.append(input("Введите Фамилию (-1 - отмена): ").strip())
        if data[0] == "-1":
            return
        while len(data[0].strip()) == 0 or len(data[0].strip()) > 32:
            if len(data[0].strip()) == 0:
                data[0] = input("Фамилия не может быть пустой! Введите Фамилию заново (-1 - отмена): ").strip()
                if data[0] == "-1":
                    return
            if len(data[0].strip()) > 32:
                data[0] = input(
                    "Фамилия не может быть длиннее 32 символов! Введите Фамилию заново (-1 - отмена): ").strip()
                if data[0] == "-1":
                    return
        data.append(input("Введите Имя (-1 - отмена): ").strip())
        if data[1] == "-1":
            return
        while len(data[1].strip()) == 0 or len(data[1].strip()) > 32:
            if len(data[1].strip()) == 0:
                data[1] = input("Имя не может быть пустым! Введите Имя заново (-1 - отмена): ").strip()
                if data[1] == "-1":
                    return
            if len(data[1].strip()) > 32:
                data[1] = input("Имя не может быть длиннее 32 символов! Введите Имя заново (-1 - отмена): ").strip()
                if data[1] == "-1":
                    return
        data.append(input("Введите Отчество (-1 - отмена): ").strip())
        if data[2] == "-1":
            return
        while len(data[2].strip()) > 32:
            data[2] = input(
                "Отчество не может быть длиннее 32 символов! Введите Отчество заново (-1 - отмена): ").strip()
            if data[2] == "-1":
                return
        pt = PeopleTable()
        pt.insert_one(data)
        return

    def show_phones_by_people(self):
        if self.person_id == -1:
            while True:
                num = input(
                    "Укажите номер строки, в которой записан человек, о котором вы хотите просмотреть информацию (-1 - отмена): ")
                if num == "-1":
                    return "1"
                while len(num.strip()) == 0:
                    num = input(
                        "Пустая строка. Повторите ввод! Укажите номер строки, в которой записан человек, о котором вы хотите просмотреть информацию (-1 - отмена): ")
                if num == "-1":
                    return "1"
                while not int_format_check(num):
                    num = input(
                        f"Не существует номера строки {num} Повторите ввод! Укажите номер строки, в которой записан человек, о котором вы хотите просмотреть информацию (-1 - отмена): ")
                if num == "-1":
                    return "1"

                person = PeopleTable().find_by_position(int(num))
                if not person:
                    print("Введено номер строки, неудовлетворяющий ни одному человеку!")
                else:
                    self.person_id = int(person[0])
                    self.person_obj = person
                    break
        print("Выбран человек: " + self.person_obj[1] + " " + self.person_obj[2] + " " + self.person_obj[3])
        print("Телефоны: ")
        lst = PhonesTable().all_by_person_id(self.person_id)
        for i in lst:
            print(i[1])
        menu = """Дальнейшие операции:
    0 - возврат в главное меню;
    1 - возврат в просмотр людей;
    6 - добавление нового телефона;
    7 - удаление телефона;
    8 - изменение телефона;
    9 - выход."""
        print(menu)

    def show_docs_by_people(self):
        if self.person_id == -1:
            while True:
                num = input(
                    "Укажите номер строки, в которой указан человек, о котором вы хотите просмотреть информацию (-1 - отмена): ")
                if num == "-1":
                    return "1"
                while len(num.strip()) == 0:
                    num = input(
                        "Пустая строка. Повторите ввод! Укажите номер строки, в которой указан человек, о котором вы хотите просмотреть информацию (-1 - отмена): ")
                if num == "-1":
                    return "1"
                while not int_format_check(num):
                    num = input(
                        f"Не существует номера строки {num} Повторите ввод! Укажите номер строки, в которой записан человек, о котором вы хотите просмотреть информацию (-1 - отмена): ")
                if num == "-1":
                    return "1"

                person = PeopleTable().find_by_position(int(num))
                if not person:
                    print("Введено число, неудовлетворяющее ни одной строке!")
                else:
                    self.person_id = int(person[0])
                    self.person_obj = person
                    break
        print("Выбран человек: " + self.person_obj[1] + " " + self.person_obj[2] + " " + self.person_obj[3])
        menu = """Просмотр списка документов!
№    Тип                 Серия          Номер          Дата"""
        print(menu)
        lst = DocsTable().all_by_person_id(self.person_id)
        t = 1
        for i in lst:
            print(
                str(t).ljust(5) + str(i[2]).ljust(20) + str(i[3]).ljust(15) + str(i[4]).ljust(15) + str(i[5]).ljust(15))
            t += 1
        menu = """Дальнейшие операции:
    0 - возврат в главное меню;
    1 - возврат в просмотр людей;
    6 - добавление нового документа;
    7 - удаление документа;
    8 - изменение документа;
    9 - выход."""
        print(menu)

    def search_person_by_pos(self, title):
        while True:
            num = input(f"Укажите номер строки, в которой записан человек, {title} (-1 - отмена): ")
            if num == "-1":
                return "-1"
            while len(num.strip()) == 0:
                num = input(
                    "Пустая строка. Повторите ввод! Укажите номер строки, в которой записан человек (-1 - отмена): ")
            if num == "-1":
                return "-1"
            while not int_format_check(num):
                num = input(
                    f"Не существует номера строки {num} Повторите ввод! Укажите номер строки, в которой записан человек, о котором вы хотите просмотреть информацию (-1 - отмена): ")
            if num == "-1":
                return "1"
            person = PeopleTable().find_by_position(int(num))
            if not person:
                print("Введен номер строки, неудовлетворяющий ни одному человеку!")
                return "-1"
            return person[0]

    def delete_person(self):
        title = 'которого вы хотите удалить'
        num = self.search_person_by_pos(title)
        if num == "-1":
            return
        dt = DocsTable()
        pt = PeopleTable()
        pht = PhonesTable()
        dt.delete_docs_by_person(int(num))
        pht.delete_phones_by_person(int(num))
        pt.delete(int(num))

    def update_person(self):
        title = 'информацию о котором вы хотите изменить'
        num = self.search_person_by_pos(title)
        if num == "-1":
            return
        data = []
        data.append(input("Введите Фамилию (-1 - отмена, -2 - пропустить поле): ").strip())
        if data[0] == "-1":
            return
        elif data[0] == "-2":
            data[0] = str(PeopleTable().find_by_id(num)[1])
        else:
            while len(data[0].strip()) == 0 or len(data[0].strip()) > 32:
                if len(data[0].strip()) == 0:
                    data[0] = input(
                        "Фамилия не может быть пустой! Введите Фамилию заново (-1 - отмена, -2 - пропустить поле): ").strip()
                    if data[0] == "-1":
                        return
                    elif data[0] == "-2":
                        data[0] = str(PeopleTable().find_by_id(num)[1])
                if len(data[0].strip()) > 32:
                    data[0] = input(
                        "Фамилия не может быть длиннее 32 символов! Введите Фамилию заново (-1 - отмена, -2 - пропустить поле): ").strip()
                    if data[0] == "-1":
                        return
                    elif data[0] == "-2":
                        data[0] = str(PeopleTable().find_by_id(num)[1])
        data.append(input("Введите Имя (-1 - отмена, -2 - пропустить поле): ").strip())
        if data[1] == "-1":
            return
        elif data[1] == "-2":
            data[1] = str(PeopleTable().find_by_id(num)[2])
        else:
            while len(data[1].strip()) == 0 or len(data[1].strip()) > 32:
                if len(data[1].strip()) == 0:
                    data[1] = input(
                        "Имя не может быть пустым! Введите Имя заново (-1 - отмена, -2 - пропустить поле): ").strip()
                    if data[1] == "-1":
                        return
                    elif data[1] == "-2":
                        data[1] = str(PeopleTable().find_by_id(num)[2])
                if len(data[1].strip()) > 32:
                    data[1] = input(
                        "Имя не может быть длиннее 32 символов! Введите Имя заново (-1 - отмена, -2 - пропустить поле): ").strip()
                    if data[1] == "-1":
                        return
                    elif data[1] == "-2":
                        data[1] = str(PeopleTable().find_by_id(num)[2])
        data.append(input("Введите Отчество (-1 - отмена, -2 - пропустить поле): ").strip())
        if data[2] == "-1":
            return
        elif data[2] == "-2":
            data[2] = str(PeopleTable().find_by_id(num)[3])
        else:
            while len(data[2].strip()) > 32:
                data[2] = input(
                    "Отчество не может быть длиннее 32 символов! Введите Отчество заново (-1 - отмена, -2 - пропустить поле): ").strip()
                if data[2] == "-1":
                    return
                elif data[2] == "-2":
                    data[2] = str(PeopleTable().find_by_id(num)[3])
            pt = PeopleTable()
            pt.update(num, data)

    def insert_new_phone(self):
        data = []
        data.append(self.person_id)
        data.append(input("Введите телефон, который хотите добавить (-1 - отмена): ").strip())
        if data[1] == "-1":
            return
        while (len(data[1].strip()) == 0) or (len(data[1].strip()) > 12) or (
                (not (data[1][1:].isdigit() and data[1][0] == '+') and not (
                        data[1].isdigit())) == True) or PhonesTable().check_number(self.person_id,
                                                                                   data[1].strip()) == True:
            if len(data[1].strip()) == 0:
                data[1] = input(
                    "Номер телефона не может быть пустым! Введите номер телефона заново (-1 - отмена): ").strip()
                if data[1] == "-1":
                    return
            elif len(data[1].strip()) > 12:
                data[1] = input(
                    "Номер телефона не может быть длинее 12 цифр! Введите номер телефона заново (-1 - отмена): ").strip()
                if data[1] == "-1":
                    return
            elif (not (data[1][1:].isdigit() and data[1][0] == '+') and not (data[1].isdigit())) == True:
                data[1] = input(
                    "Номер телефона должен состоять только из цифр или знака + и цифр! Введите номер телефона заново (-1 - отмена): ").strip()
                if data[1] == "-1":
                    return
            elif PhonesTable().check_number(self.person_id, data[1].strip()) == True:
                data[1] = input(
                    f'Номер {data[1]} уже существует! Повторите ввод номера телефона, который хотите добавить (-1 - отмена): ').strip()
                if data[1] == "-1":
                    return
        pht = PhonesTable()
        pht.insert_one(data)
        return

    def insert_new_doc(self):
        data = []
        data.append(self.person_id)
        data.append(input("Введите Тип (-1 - отмена): ").strip())
        if data[1] == "-1":
            return
        while len(data[1].strip()) == 0 or len(data[1].strip()) > 32:
            if len(data[1].strip()) == 0:
                data[1] = input("Тип не может быть пустой! Введите Тип заново (-1 - отмена): ").strip()
                if data[1] == "-1":
                    return
            if len(data[1].strip()) > 32:
                data[1] = input(
                    "Тип не может быть длиннее 32 символов! Введите Тип заново (-1 - отмена): ").strip()
                if data[1] == "-1":
                    return
        data.append(input("Введите Серию (-1 - отмена): ").strip())
        if data[2] == "-1":
            return
        while len(data[2].strip()) == 0 or len(data[1].strip()) > 32:
            if len(data[2].strip()) == 0:
                data[2] = input("Серия не может быть пустой! Введите Серия заново (-1 - отмена): ").strip()
                if data[2] == "-1":
                    return
            if len(data[2].strip()) > 32:
                data[2] = input(
                    "Серия не может быть длиннее 32 символов! Введите Серия заново (-1 - отмена): ").strip()
                if data[1] == "-1":
                    return
        data.append(input("Введите Номер (-1 - отмена): ").strip())
        if data[3] == "-1":
            return
        while len(data[3].strip()) == 0 or len(data[3].strip()) > 32:
            if len(data[3].strip()) == 0:
                data[3] = input("Номер не может быть пустой! Введите Номер заново (-1 - отмена): ").strip()
                if data[3] == "-1":
                    return
            if len(data[3].strip()) > 32:
                data[3] = input(
                    "Номер не может быть длиннее 32 символов! Введите Номер заново (-1 - отмена): ").strip()
                if data[3] == "-1":
                    return
        data.append(input("Введите Дату в формате ДД.ММ.ГГГГ (-1 - отмена): ").strip())
        if data[4] == "-1":
            return
        while len(data[4].strip()) == 0 or len(data[4].strip()) > 10 or not date_format_check(
                data[4].strip()) or not date_check(data[4]):
            if len(data[4].strip()) == 0:
                data[4] = input("Дата не может быть пустой! Введите Дату заново (-1 - отмена): ").strip()
                if data[4] == "-1":
                    return
            elif len(data[4].strip()) > 10:
                data[4] = input(
                    "Дата не может быть длиннее 10 символов! Введите Дату заново (-1 - отмена): ").strip()
                if data[4] == "-1":
                    return
            elif not date_format_check(data[4].strip()):
                data[4] = input("Неправильный формат. Введите ДД.ММ.ГГГГ (-1 - отмена): ").strip()
                if data[4] == "-1":
                    return
            elif not date_check(data[4]):
                data[4] = input(f"Дата не может быть раньше сегоднешней. Введите дату заново (-1 - отмена): ").strip()
                if data[4] == "-1":
                    return
        dt = DocsTable()
        dt.insert_one(data)
        return

    def search_phone(self, title):
        tel = input(f"Введите номер телефона, который хотите {title} (-1 - отмена): ").strip()
        if tel == "-1":
            return "-1"
        while len(tel.strip()) == 0 or PhonesTable().check_number(self.person_id, tel) == False:
            if len(tel.strip()) == 0:
                tel = input(
                    "Пустая строка. Повторите ввод! Повторите ввод номера телефона, который хотите удалить (-1 - отмена): ").strip()
                if tel == "-1":
                    return "-1"
            if PhonesTable().check_number(self.person_id, tel) == False:
                tel = input(
                    f'Номера {tel} не существует! Повторите ввод номера телефона, который хотите удалить (-1 - отмена): ').strip()
                if tel == "-1":
                    return "-1"
        return tel

    def search_docs(self, title):
        while True:
            pos = input(
                f"Введите номер строки, в которой записан документ, который хотите {title} (-1 - отмена): ").strip()
            if pos == "-1":
                return "1"
            while len(pos.strip()) == 0:
                pos = input(
                    f"Пустая строка. Повторите ввод! Укажите номер строки, в которой записан документ, который хотите {title} (-1 - отмена): ").strip()
            if pos == "-1":
                return "1"
            while not int_format_check(pos):
                pos = input(
                    f"Не существует номера строки {pos} Повторите ввод! Укажите номер строки, в которой записан документ, который хотите {title} (-1 - отмена): ").strip()
            if pos == "-1":
                return "1"
            pos = DocsTable().find_by_position(int(pos), self.person_id)
            while pos == None:
                pos = input(
                    f'Запрашиваемого документа не существует! Повторите ввод! Укажите номер строки, в которой записан документ, который хотите {title} (-1 - отмена): ')
            id = pos[0]
            if id == "-1":
                return "-1"
            return int(id)

    def delete_phone(self):
        title = "удалить"
        num = self.search_phone(title)
        if num == "-1":
            return
        pht = PhonesTable()
        pht.delete_phone(num)
        return

    def delete_docs(self):
        title = "удалить"
        num = self.search_docs(title)
        if num == "-1":
            return
        pht = DocsTable()
        pht.delete_docs(num)
        return

    def update_phone(self):
        title = "изменить"
        tel = self.search_phone(title)
        if tel == "-1":
            return
        data = ''
        tel_new = input("Введите телефон, который хотите добавить (-1 - отмена): ").strip()
        if tel_new == "-1":
            return
        while (len(tel_new.strip()) == 0) or (len(tel_new.strip()) > 12) or (
                (not (tel_new[1:].isdigit() and tel_new[0] == '+') and not (
                        tel_new.isdigit())) == True) or tel_new == tel:
            if len(tel_new.strip()) == 0:
                tel_new = input(
                    "Номер телефона не может быть пустым! Введите номер телефона заново (-1 - отмена): ").strip()
                if tel_new == "-1":
                    return
            elif len(tel_new.strip()) > 12:
                tel_new = input(
                    "Номер телефона не может быть длинее 12 цифр! Введите номер телефона заново (-1 - отмена): ").strip()
                if tel_new == "-1":
                    return
            elif (not (tel_new[1:].isdigit() and tel_new[0] == '+') and not (tel_new.isdigit())) == True:
                tel_new = input(
                    "Номер телефона должен состоять только из цифр или знака + и цифр! Введите номер телефона заново (-1 - отмена): ").strip()
                if tel_new == "-1":
                    return
            elif tel_new == tel:
                tel_new = input(
                    'Номер {tel_new} совпадает с добавляемым! Повторите ввод номера телефона, который хотите добавить (-1 - отмена): ').strip()
                if tel_new == "-1":
                    return
        pht = PhonesTable()
        pht.update_phone(tel, tel_new)
        return

    def update_docs(self):
        title = 'изменить'
        num = self.search_docs(title)
        if num == "-1":
            return
        data = []
        data.append(input("Введите Тип (-1 - отмена, -2 - пропустить поле): ").strip())
        if data[0] == "-1":
            return
        elif data[0] == "-2":
            data[0] = str(DocsTable().find_by_id(num)[2])
        else:
            while len(data[0].strip()) == 0 or len(data[0].strip()) > 32:
                if len(data[0].strip()) == 0:
                    data[0] = input(
                        "Тип не может быть пустым! Введите Тип заново (-1 - отмена, -2 - пропустить поле): ").strip()
                    if data[0] == "-1":
                        return
                    elif data[0] == "-2":
                        data[0] = str(DocsTable().find_by_id(num)[2])
                if len(data[0].strip()) > 32:
                    data[0] = input(
                        "Тип не может быть длиннее 32 символов! Введите Тип заново (-1 - отмена, -2 - пропустить поле): ").strip()
                    if data[0] == "-1":
                        return
                    elif data[0] == "-2":
                        data[0] = str(DocsTable().find_by_id(num)[1])
        data.append(input("Введите Серию (-1 - отмена, -2 - пропустить поле): ").strip())
        if data[1] == "-1":
            return
        elif data[1] == "-2":
            data[1] = str(DocsTable().find_by_id(num)[3])
        else:
            while len(data[1].strip()) == 0 or len(data[1].strip()) > 32:
                if len(data[1].strip()) == 0:
                    data[1] = input(
                        "Серия не может быть пустой! Введите Серию заново (-1 - отмена, -2 - пропустить поле): ").strip()
                    if data[1] == "-1":
                        return
                    elif data[1] == "-2":
                        data[1] = str(PeopleTable().find_by_id(num)[3])
                if len(data[1].strip()) > 32:
                    data[1] = input(
                        "Серия не может быть длиннее 32 символов! Введите Серию заново (-1 - отмена, -2 - пропустить поле): ").strip()
                    if data[1] == "-1":
                        return
                    elif data[1] == "-2":
                        data[1] = str(PeopleTable().find_by_id(num)[3])
        data.append(input("Введите Номер (-1 - отмена, -2 - пропустить поле): ").strip())
        if data[2] == "-1":
            return
        elif data[2] == "-2":
            data[2] = str(DocsTable().find_by_id(num)[4])
        while len(data[2].strip()) == 0 or len(data[2].strip()) > 32:
            if len(data[2].strip()) == 0:
                data[2] = input("Номер не может быть пустой! Введите Номер заново (-1 - отмена): ").strip()
                if data[2] == "-1":
                    return
            if len(data[2].strip()) > 32:
                data[2] = input(
                    "Номер не может быть длиннее 32 символов! Введите Номер заново (-1 - отмена, -2 - пропустить поле): ").strip()
            if data[2] == "-1":
                return
            elif data[2] == "-2":
                data[2] = str(DocsTable().find_by_id(num)[4])
        data.append(input("Введите Дату в формате ДД.ММ.ГГГГ (-1 - отмена, -2 - пропустить поле): ").strip())
        if data[3] == "-1":
            return
        elif data[3] == "-2":
            data[3] = str(DocsTable().find_by_id(num)[5])
        else:
            while len(data[3].strip()) == 0 or len(data[3].strip()) > 32 or (
                    not date_format_check(data[3].strip()) and data[3].strip() != "-2"):
                if len(data[3].strip()) == 0:
                    data[3] = input(
                        "Дата не может быть пустой! Введите Дату заново (-1 - отмена, -2 - пропустить поле): ").strip()
                    if data[3] == "-1":
                        return
                    elif data[3] == "-2":
                        data[3] = str(DocsTable().find_by_id(num)[5])
                elif len(data[3].strip()) > 10:
                    data[3] = input(
                        "Дата не может быть длиннее 10 символов! Введите Дату заново (-1 - отмена, -2 - пропустить поле): ").strip()
                    if data[3] == "-1":
                        return
                    elif data[3] == "-2":
                        data[3] = str(DocsTable().find_by_id(num)[5])
                elif not date_format_check(data[3].strip()):
                    data[3] = input(
                        "Неправильный формат. Введите ДД.ММ.ГГГГ (-1 - отмена, -2 - пропустить поле): ").strip()
                    if data[3] == "-1":
                        return
                    elif data[3] == "-2":
                        data[3] = str(DocsTable().find_by_id(num)[5])
                elif not date_check(data[3]):
                    data[3] = input(
                        f"Дата не может быть раньше сегоднешней. Введите дату заново (-1 - отмена, -2 - пропустить поле): ").strip()
                    if data[3] == "-1":
                        return
                    elif data[3] == "-2":
                        data[3] = str(DocsTable().find_by_id(num)[5])
        dt = DocsTable()
        dt.update_docs(num, data)
        return

    def phones_table_transporter(self, current_menu):
        check_lst = ("0", "1", "6", "7", "8", "9")
        if current_menu not in check_lst:
            print("Выбран не верный пукт меню! Повторите ввод!")
            return "phones_table_err"
        elif current_menu == "0":
            return "0"
        elif current_menu == "1":
            return "1"
        elif current_menu == "6":
            self.insert_new_phone()
            return "6"
        elif current_menu == "7":
            self.delete_phone()
            return "6"
        elif current_menu == "8":
            self.update_phone()
            return "6"
        elif current_menu == "9":
            return "9"

    def docs_table_transporter(self, current_menu):
        check_lst = ("0", "1", "6", "7", "8", "9")
        if current_menu not in check_lst:
            print("Выбран не верный пукт меню! Повторите ввод!")
            return "docs_table_err"
        elif current_menu == "0":
            return "0"
        elif current_menu == "1":
            return "1"
        elif current_menu == "6":
            self.insert_new_doc()
            return "7"
        elif current_menu == "7":
            self.delete_docs()
            return "7"
        elif current_menu == "8":
            self.update_docs()
            return "7"
        elif current_menu == "9":
            return "9"

    def people_menu_transporter(self, current_menu):
        check_lst = ("0", "1", "3", "4", "5", "6", "7", "8", "9", "phones_table_err", "docs_table_err", "page_err")
        while True:
            if current_menu not in check_lst:
                print("Выбран не верный пукт меню! Повторите ввод!")
                return "input_err"
            elif current_menu == "0":
                return "0"
            elif current_menu == "9":
                return "9"
            elif current_menu == "1":
                return "1"
            elif current_menu == "3":
                self.show_add_person()
                current_menu = "1"
            elif current_menu == "4":
                self.delete_person()
                current_menu = "1"
            elif current_menu == "5":
                self.update_person()
                current_menu = "1"
            elif current_menu == "6":
                current_menu = self.show_phones_by_people()
                if current_menu != "1":
                    next_step = self.read_next_step()
                    current_menu = self.phones_table_transporter(next_step)
            elif current_menu == "7":
                current_menu = self.show_docs_by_people()
                if current_menu != "1":
                    next_step = self.read_next_step()
                    current_menu = self.docs_table_transporter(next_step)
            elif current_menu == "8":
                self.pages_menu_transporter()
                current_menu = "1"
            elif current_menu == "phones_table_err":
                next_step = self.read_next_step()
                current_menu = self.phones_table_transporter(next_step)
            elif current_menu == "docs_table_err":
                next_step = self.read_next_step()
                current_menu = self.docs_table_transporter(next_step)
            elif current_menu == "page_err":
                next_step = self.read_next_step()
                current_menu = self.pages_menu_transporter(next_step)

    def main_menu_transporter(self, current_menu):
        check_lst = ("0", "1", "2", "7", "9", "input_err")
        while True:
            if current_menu not in check_lst:
                print("Выбран не верный пункт меню! Повторите ввод!")
                return "input_err"
            elif current_menu == "1":
                self.show_people()
                next_step = self.read_next_step()
                current_menu = self.people_menu_transporter(next_step)
            elif current_menu == "2":
                self.db_drop()
                self.db_init()
                self.db_insert_somethings()
                print("Таблицы созданы заново!")
                return "0"
            elif current_menu == "0":
                return "0"
            elif current_menu == "9":
                return "9"
            elif current_menu == "input_err":
                next_step = self.read_next_step()
                current_menu = self.people_menu_transporter(next_step)

    def main_cycle(self, current_menu="0"):
        while (current_menu != "9"):
            if current_menu == "0":
                self.show_main_menu()
                next_step = self.read_next_step()
                current_menu = self.main_menu_transporter(next_step)
            elif current_menu == "input_err":
                next_step = self.read_next_step()
                current_menu = self.main_menu_transporter(next_step)
        print("До свидания!")
        return


m = Main()
m.main_cycle()
