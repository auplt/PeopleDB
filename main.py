import sys

from tables.people_table import *
from tables.phones_table import *

sys.path.append('tables')

from project_config import *
from dbconnection import *


# from people_table import *
# from phones_table import *

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
        return input("=> ").strip()

    def after_main_menu(self, next_step):
        if next_step == "2":
            self.db_drop()
            self.db_init()
            self.db_insert_somethings()
            print("Таблицы созданы заново!")
            return "0"
        elif next_step != "1" and next_step != "9":
            print("Выбрано неверное число! Повторите ввод!")
            return "0"
        else:
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
    5 - просмотр телефонов человека;
    9 - выход."""
        print(menu)
        return

    def after_show_people(self, next_step):
        while True:
            if next_step == "4":
                # DONE!!! # print("Пока не реализовано!") # Переписать поиск
                self.delete_person()
                return "1"
            elif next_step == "6":
                # DONE!!! # print("Пока не реализовано!") # Ограничесние целостности
                self.insert_new_phone()
                next_step = "5"
            elif next_step == "7":
                # DONE!!! # print("Пока не реализовано!") # Переписать поиск
                self.delete_phone()
                next_step = "5"
            elif next_step == "5":
                next_step = self.show_phones_by_people()
            elif next_step == "12":
                self.update_phone()
                next_step = "5"
            elif next_step != "0" and next_step != "9" and next_step != "3":
                print("Выбрано неверное число! Повторите ввод!")
                return "1"
            else:
                return next_step

    def show_add_person(self):
        # Не реализована проверка на максимальную длину строк. Нужно доделать самостоятельно!
        data = []
        data.append(input("Введите имя (1 - отмена): ").strip())
        if data[0] == "1":
            return
        while len(data[0].strip()) == 0 or len(data[0].strip()) > 32:
            if len(data[0].strip()) == 0:
                data[0] = input("Имя не может быть пустым! Введите имя заново (1 - отмена): ").strip()
                if data[0] == "1":
                    return
            if len(data[0].strip()) > 32:
                data[0] = input("Имя не может быть длиннее 32 символов! Введите имя заново (1 - отмена): ").strip()
                if data[0] == "1":
                    return
        data.append(input("Введите фамилию (1 - отмена): ").strip())
        if data[1] == "1":
            return
        while len(data[1].strip()) == 0 or len(data[1].strip()) > 32:
            if len(data[1].strip()) == 0:
                data[1] = input("Фамилия не может быть пустой! Введите фамилию заново (1 - отмена): ").strip()
                if data[1] == "1":
                    return
            if len(data[1].strip()) > 32:
                data[1] = input(
                    "Фамилия не может быть длиннее 32 символов! Введите фамилию заново (1 - отмена): ").strip()
                if data[1] == "1":
                    return
        data.append(input("Введите отчество (1 - отмена): ").strip())
        if data[2] == "1":
            return
        while len(data[2].strip()) > 5000:
            data[2] = input(
                "Отчество не может быть длиннее 32 символов! Введите отчество заново (1 - отмена): ").strip()
            if data[2] == "1":
                return
        pt = PeopleTable()
        pt.insert_one(data)
        return

    def show_phones_by_people(self):
        if self.person_id == -1:
            while True:
                num = input("Укажите номер строки, в которой записана интересующая Вас персона (0 - отмена): ")
                while len(num.strip()) == 0:
                    num = input(
                        "Пустая строка. Повторите ввод! Укажите номер строки, в которой записана интересующая Вас персона (0 - отмена): ")
                if num == "0":
                    return "1"
                person = PeopleTable().find_by_position(int(num))
                if not person:
                    print("Введено число, неудовлетворяющее количеству людей!")
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
    12 - изменение телефона;
    9 - выход."""
        print(menu)
        return self.read_next_step()

        return self.read_next_step()

    def main_cycle(self):
        current_menu = "0"
        next_step = None
        while (current_menu != "9"):
            if current_menu == "0":
                self.show_main_menu()
                next_step = self.read_next_step()
                current_menu = self.after_main_menu(next_step)
            elif current_menu == "1":
                self.show_people()
                next_step = self.read_next_step()
                current_menu = self.after_show_people(next_step)
            elif current_menu == "2":
                self.show_main_menu()
            elif current_menu == "3":
                self.show_add_person()
                current_menu = "1"
        print("До свидания!")
        return

    def delete_person(self):
        num = input("Укажите ID пользователья, которого вы хотите удалить (0 - отмена): ")
        while len(num.strip()) == 0:
            num = input(
                "Пустая строка. Повторите ввод! Укажите ID пользователья, которого вы хотите удалить (0 - отмена): ")
            if num == "0":
                return "1"
            person = PeopleTable().find_by_position(int(num))
            if not person:
                print("Введено число, неудовлетворяющее количеству людей!")
        pt = PeopleTable()
        pht = PhonesTable()
        pht.delete_phones_by_person(int(num))
        pt.delete(int(num))

    def insert_new_phone(self):
        # Не реализована проверка на максимальную длину строк. Нужно доделать самостоятельно!

        data = []
        data.append(self.person_id)
        data.append(input("Введите телефон, который хотите добавить (1 - отмена): ").strip())
        if data[1] == "1":
            return
        while (len(data[1].strip()) == 0) or (len(data[1].strip()) > 12) or (
                (not (data[1][1:].isdigit() and data[1][0] == '+') and not (
                        data[1].isdigit())) == True) or PhonesTable().check_number(self.person_id,
                                                                                   data[1].strip()) == True:
            if len(data[1].strip()) == 0:
                data[1] = input(
                    "Номер телефона не может быть пустым! Введите номер телефона заново (1 - отмена): ").strip()
                if data[1] == "1":
                    return
            elif len(data[1].strip()) > 12:
                data[1] = input(
                    "Номер телефона не может быть длинее 12 цифр! Введите номер телефона заново (1 - отмена): ").strip()
                if data[1] == "1":
                    return
            elif (not (data[1][1:].isdigit() and data[1][0] == '+') and not (data[1].isdigit())) == True:
                data[1] = input(
                    "Номер телефона должен состоять только из цифр или знака + и цифр! Введите номер телефона заново (1 - отмена): ").strip()
                if data[1] == "1":
                    return
            elif PhonesTable().check_number(self.person_id, data[1].strip()) == True:
                data[1] = input(
                    f'Номер {data[1]} уже существует! Повторите ввод номера телефона, который хотите добавить (0 - отмена): ').strip()
                if data[1] == "0":
                    return "1"
        pht = PhonesTable()
        pht.insert_one(data)
        return


    def search_phone(self):
        tel = input("Введите номер телефона, который хотите удалить (0 - отмена): ")
        while len(tel.strip()) == 0 or PhonesTable().check_number(self.person_id, tel) == False:
            if len(tel.strip()) == 0:
                tel = input(
                    "Пустая строка. Повторите ввод! Повторите ввод номера телефона, который хотите удалить (0 - отмена): ")
                if tel == "0":
                    return "1"
            if PhonesTable().check_number(self.person_id, tel) == False:
                if tel == "0":
                    return "1"
                tel = input(
                    f'Номера {tel} не существует! Повторите ввод номера телефона, который хотите удалить (0 - отмена): ')
                # if tel == "0":
                #     return "1"
        print(self.person_id, tel)
        # delete_phone(tel)
        return tel

    def delete_phone(self):
        num = self.search_phone()
        pht = PhonesTable()
        pht.delete_phone(num)
        return

    # def update_phone(self):
    #     tel = self.search_phone()
    #     num = input("Введите номер телефона, который хотите удалить (0 - отмена): ")
    #     while len(num.strip()) == 0 or PhonesTable().check_number(self.person_id, num) == False:
    #         if len(num.strip()) == 0:
    #             num = input(
    #                 "Пустая строка. Повторите ввод! Повторите ввод номера телефона, который хотите удалить (0 - отмена): ")
    #             if num == "0":
    #                 return "1"
    #         if PhonesTable().check_number(self.person_id, num) == False:
    #             num = input(
    #                 f'Номера {num} не существует! Повторите ввод номера телефона, который хотите удалить (0 - отмена): ')
    #             if num == "0":
    #                 return "1"
    #     pht = PhonesTable()
    #     pht.update_phone(tel, num)

    def update_phone(self):
        # Не реализована проверка на максимальную длину строк. Нужно доделать самостоятельно!

        tel = self.search_phone()

        data = ''
        # data.append(self.person_id)
        tel_new = input("Введите телефон, который хотите добавить (1 - отмена): ").strip()
        if tel_new == "1":
            return
        while (len(tel_new.strip()) == 0) or (len(tel_new.strip()) > 12) or (
                (not (tel_new[1:].isdigit() and tel_new[0] == '+') and not (
                        tel_new.isdigit())) == True) or tel_new == tel:
            if len(tel_new.strip()) == 0:
                tel_new = input(
                    "Номер телефона не может быть пустым! Введите номер телефона заново (1 - отмена): ").strip()
                if tel_new == "1":
                    return
            elif len(tel_new.strip()) > 12:
                tel_new = input(
                    "Номер телефона не может быть длинее 12 цифр! Введите номер телефона заново (1 - отмена): ").strip()
                if tel_new == "1":
                    return
            elif (not (tel_new[1:].isdigit() and tel_new[0] == '+') and not (tel_new.isdigit())) == True:
                tel_new = input(
                    "Номер телефона должен состоять только из цифр или знака + и цифр! Введите номер телефона заново (1 - отмена): ").strip()
                if tel_new == "1":
                    return
            elif tel_new == tel:
                tel_new = input(
                    f'Номер {tel_new} совпадает с добавляемым! Повторите ввод номера телефона, который хотите добавить (0 - отмена): ').strip()
                if tel_new == "0":
                    return "1"
        print(data, tel)
        pht = PhonesTable()
        pht.update_phone(tel, tel_new)
        return


m = Main()
m.main_cycle()
