import sys

from tables.people_table import *
from tables.phones_table import *

# from keysinterrupt import *

sys.path.append('tables')

from project_config import *
from dbconnection import *


class Main:
    config = ProjectConfig()
    connection = DbConnection(config)

    def __init__(self):
        DbTable.dbconn = self.connection
        return

    def db_init(self):
        pt = PeopleTable()
        pht = PhonesTable()
        pt.create()
        pht.create()
        return

    def db_insert_somethings(self):
        pt = PeopleTable()
        pht = PhonesTable()
        pt.insert_one(["Test", "Test", "Test"])
        pt.insert_one(["Test2", "Test2", "Test2"])
        pt.insert_one(["Test3", "Test3", "Test3"])
        pht.insert_one([1, "123"])
        pht.insert_one([2, "123"])
        pht.insert_one([3, "123"])

    def db_drop(self):
        pht = PhonesTable()
        pt = PeopleTable()
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
            # print("***")
            print("Выбран не верный пункт меню! Повторите ввод!")
            next_step = input("=> ").strip()
        return next_step


    def show_people(self):
        self.person_id = -1
        menu = """Просмотр списка людей!
№\tФамилия\tИмя\tОтчество"""
        print(menu)
        lst = PeopleTable().all()
        for i in lst:
            print(str(i[0]) + "\t" + str(i[1]) + "\t" + str(i[2]) + "\t" + str(i[3]))
        menu = """Дальнейшие операции: 
    0 - возврат в главное меню;
    3 - добавление нового человека;
    4 - удаление человека;
    5 - изменение информации о человеке;
    6 - просмотр телефонов человека;
    9 - выход."""
        print(menu)
        return

    def show_add_person(self):
        # Не реализована проверка на максимальную длину строк. Нужно доделать самостоятельно!
        data = []

        data.append(input("Введите имя (-1 - отмена): ").strip())
        if data[0] == "-1":
            return
        # else:
        #     data.append(input().strip())
        while len(data[0].strip()) == 0 or len(data[0].strip()) > 32:
            if len(data[0].strip()) == 0:
                data[0] = input("Имя не может быть пустым! Введите имя заново (-1 - отмена): ").strip()
                if data[0] == "-1":
                    return
            if len(data[0].strip()) > 32:
                data[0] = input("Имя не может быть длиннее 32 символов! Введите имя заново (-1 - отмена): ").strip()
                if data[0] == "-1":
                    return
        data.append(input("Введите фамилию (-1 - отмена): ").strip())
        if data[1] == "-1":
            return
        while len(data[1].strip()) == 0 or len(data[1].strip()) > 32:
            if len(data[1].strip()) == 0:
                data[1] = input("Фамилия не может быть пустой! Введите фамилию заново (-1 - отмена): ").strip()
                if data[1] == "-1":
                    return
            if len(data[1].strip()) > 32:
                data[1] = input(
                    "Фамилия не может быть длиннее 32 символов! Введите фамилию заново (-1 - отмена): ").strip()
                if data[1] == "-1":
                    return
        data.append(input("Введите отчество (-1 - отмена): ").strip())
        if data[2] == "-1":
            return
        while len(data[2].strip()) > 5000:
            data[2] = input(
                "Отчество не может быть длиннее 32 символов! Введите отчество заново (-1 - отмена): ").strip()
            if data[2] == "-1":
                return
        pt = PeopleTable()
        pt.insert_one(data)
        return

    def show_phones_by_people(self):
        if self.person_id == -1:
            while True:
                num = input("Укажите ID человека, о котором вы хотите просмотреть информацию (-1 - отмена): ")
                if num == "-1":
                    return "1"
                while len(num.strip()) == 0:
                    num = input(
                        "Пустая строка. Повторите ввод! Укажите ID человека, о котором вы хотите просмотреть информацию (-1 - отмена): ")
                if num == "-1":
                    return "1"
                person = PeopleTable().find_by_id(int(num))
                if not person:
                    print("Введено число, неудовлетворяющее ниодному ID!")
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

    def search_person_by_id(self, title):
        num = input(f"Укажите ID пользователя, {title} (-1 - отмена): ")
        if num == "-1":
            return "-1"
        while len(num.strip()) == 0:
            num = input(
                "Пустая строка. Повторите ввод! Укажите ID пользователья, которого вы хотите удалить (-1 - отмена): ")
            if num == "-1":
                return "-1"
        person = PeopleTable().find_by_id(int(num))
        print(person)
        if not person:
            print("Введен ID, неудовлетворяющий ниодному человеку!")
            return "-1"
        return num

    def delete_person(self):
        title = 'которого вы хотите удалить'
        num = self.search_person_by_id(title)
        if num == "-1":
            return
        pt = PeopleTable()
        pht = PhonesTable()
        pht.delete_phones_by_person(int(num))
        pt.delete(int(num))

    def update_person(self):
        title = 'информацию о котором вы хотите изменить'
        num = self.search_person_by_id(title)
        print(num)
        if num == "-1":
            return
        # Не реализована проверка на максимальную длину строк. Нужно доделать самостоятельно!
        data = []
        print(PeopleTable().find_by_id(num))
        data.append(input("Введите имя (-1 - отмена, -2 - пропустить поле): ").strip())
        if data[0] == "-1":
            return
        elif data[0] == "-2":
            data[0] = str(PeopleTable().find_by_id(num)[1])
        while len(data[0].strip()) == 0 or len(data[0].strip()) > 32:
            if len(data[0].strip()) == 0:
                data[0] = input(
                    "Имя не может быть пустым! Введите имя заново (-1 - отмена, -2 - пропустить поле): ").strip()
                if data[0] == "-1":
                    return
                elif data[0] == "-2":
                    data[0] = str(PeopleTable().find_by_id(num)[1])
            if len(data[0].strip()) > 32:
                data[0] = input(
                    "Имя не может быть длиннее 32 символов! Введите имя заново (-1 - отмена, -2 - пропустить поле): ").strip()
                if data[0] == "-1":
                    return
                elif data[0] == "-2":
                    data[0] = str(PeopleTable().find_by_id(num)[1])
        data.append(input("Введите фамилию (-1 - отмена, -2 - пропустить поле): ").strip())
        if data[1] == "-1":
            return
        elif data[1] == "-2":
            data[1] = str(PeopleTable().find_by_id(num)[2])
        while len(data[1].strip()) == 0 or len(data[1].strip()) > 32:
            if len(data[1].strip()) == 0:
                data[1] = input(
                    "Фамилия не может быть пустой! Введите фамилию заново (-1 - отмена, -2 - пропустить поле): ").strip()
                if data[1] == "-1":
                    return
                elif data[1] == "-2":
                    data[1] = str(PeopleTable().find_by_id(num)[2])
            if len(data[1].strip()) > 32:
                data[1] = input(
                    "Фамилия не может быть длиннее 32 символов! Введите фамилию заново (-1 - отмена, -2 - пропустить поле): ").strip()
                if data[1] == "-1":
                    return
                elif data[1] == "-2":
                    data[1] = str(PeopleTable().find_by_id(num)[2])
        data.append(input("Введите отчество (-1 - отмена, -2 - пропустить поле): ").strip())
        if data[2] == "-1":
            return
        elif data[2] == "-2":
            data[2] = str(PeopleTable().find_by_id(num)[3])
        while len(data[2].strip()) > 5000:
            data[2] = input(
                "Отчество не может быть длиннее 32 символов! Введите отчество заново (-1 - отмена, -2 - пропустить поле): ").strip()
            if data[2] == "-1":
                return
            elif data[2] == "-2":
                data[2] = str(PeopleTable().find_by_id(num)[3])
        pt = PeopleTable()
        pt.update(num, data)

    def insert_new_phone(self):
        # Не реализована проверка на максимальную длину строк. Нужно доделать самостоятельно!

        data = []
        data.append(self.person_id)
        data.append(input("Введите телефон, который хотите добавить (-1 - отмена): ").strip())
        print(data)
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

    def search_phone(self, title):
        tel = input(f"Введите номер телефона, который хотите {title} (-1 - отмена): ")
        if tel == "-1":
            return "-1"
        while len(tel.strip()) == 0 or PhonesTable().check_number(self.person_id, tel) == False:
            if len(tel.strip()) == 0:
                tel = input(
                    "Пустая строка. Повторите ввод! Повторите ввод номера телефона, который хотите удалить (-1 - отмена): ")
                if tel == "-1":
                    return "-1"
            if PhonesTable().check_number(self.person_id, tel) == False:
                tel = input(
                    f'Номера {tel} не существует! Повторите ввод номера телефона, который хотите удалить (-1 - отмена): ')
                if tel == "-1":
                    return "-1"
        print(self.person_id, tel)
        return tel

    def delete_phone(self):
        title = "удалить"
        num = self.search_phone(title)
        if num == "-1":
            return
        pht = PhonesTable()
        pht.delete_phone(num)
        return

    def update_phone(self):
        # Не реализована проверка на максимальную длину строк. Нужно доделать самостоятельно!
        title = "изменить"
        tel = self.search_phone(title)
        if tel == "-1":
            return
        data = ''
        # data.append(self.person_id)
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
                    f'Номер {tel_new} совпадает с добавляемым! Повторите ввод номера телефона, который хотите добавить (-1 - отмена): ').strip()
                if tel_new == "-1":
                    return
        print(data, tel)
        pht = PhonesTable()
        pht.update_phone(tel, tel_new)
        return

    def phones_table_transporter(self, current_menu):
        check_lst = ("0", "1", "6", "7", "8", "9")
        if current_menu not in check_lst:
            # print("phones_table_transporter")
            print("Выбран не верный пукт меню! Повторите ввод!")
            return "input_err"
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

    def people_menu_transporter(self, current_menu):
        check_lst = ("0", "1", "3", "4", "5", "6", "9", "input_err")
        while True:
            if current_menu not in check_lst:
                # print("people_menu_transporter")
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
                # DONE!!! # print("Пока не реализовано!") # Переписать поиск
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
            elif current_menu == "input_err":
                next_step = self.read_next_step()
                current_menu = self.phones_table_transporter(next_step)

    def main_menu_transporter(self, current_menu):
        check_lst = ("0", "1", "2", "9", "input_err")
        while True:
            if current_menu not in check_lst:
                # print("main_menu_transporter")
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
