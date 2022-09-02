from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QPushButton, QLineEdit, QLabel, \
    QCheckBox, QTableView, QHeaderView, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import sys, datetime
from routes import init_db, add_new_user, check_data_to_login, get_all_phone_book, \
    user_by_first_letters, add_person, update_person, delete_person, get_birth, \
    update_check_log, some_check_log, check_log_to_zero

border_style = '''
            border: 1px solid; 
            border-color:black;
        '''


class Main(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):

        self.resize(500, 300)
        self.setWindowTitle("Окно авторизации")
        self.username = QLineEdit(self)
        self.username.move(100, 20)
        self.username.setFixedSize(300, 35)
        self.username.setStyleSheet(border_style)
        self.username.setPlaceholderText("Имя пользователя")

        self.password_user = QLineEdit(self)
        self.password_user.move(100, 70)
        self.password_user.setFixedSize(300, 35)
        self.password_user.setStyleSheet(border_style)
        self.password_user.setPlaceholderText("Пароль")

        self.enter_login = QPushButton("Войти", self)
        self.enter_login.move(100, 125)
        self.enter_login.setFixedSize(145, 40)
        self.enter_login.setStyleSheet(border_style + 'background-color: #C0C0C0')
        self.enter_login.clicked.connect(self.login)

        self.registration = QPushButton("Регистрация", self)
        self.registration.move(255, 125)
        self.registration.setFixedSize(145, 40)
        self.registration.setStyleSheet(border_style + 'background-color: #C0C0C0')
        self.registration.clicked.connect(self.user_registration)

        self.check_remember = QCheckBox("Запомнить меня", self)
        self.check_remember.setCheckState(Qt.CheckState.Unchecked)
        self.check_remember.move(177, 190)
        self.check_remember.setFixedSize(145, 40)
        self.check_remember.setStyleSheet(border_style + 'background-color: #C0C0C0')

        self.forgot_password = QPushButton("Забыли пароль?", self)
        self.forgot_password.move(177, 250)
        self.forgot_password.setFixedSize(145, 40)
        self.forgot_password.setStyleSheet('border-style: hidden; color: #4169E1; '
                                          'text-decoration: underline;')
        self.forgot_password.clicked.connect(self.password_recovery)

        result_check = some_check_log()
        if result_check:
            QTimer.singleShot(0, self.get_login_with_check)

    def get_login_with_check(self):
        self.window_login = LoginWork(birthday=True)
        self.window_login.show()
        self.close()

    def user_registration(self):
        self.window_registration = Registration(main_class=self)
        self.window_registration.show()

    def password_recovery(self):
        self.window_pass_recovery = PasswordRecovery()
        self.window_pass_recovery.show()

    def login(self):
        username = self.username.text()
        password = self.password_user.text()
        res = check_data_to_login(username, password)

        if res:
            if self.check_remember.isChecked():
                update_check_log(check_log='1', username=username, password=password)

            self.window_login = LoginWork(birthday=True)
            self.window_login.show()
            self.close()
        else:
            self.window_error = NoUserData()
            self.window_error.show()


class LoginWork(QtWidgets.QWidget):
    def __init__(self, parent=None, birthday=False):
        super().__init__(parent)

        self.init_login()

        if birthday:
            self.birthday_week()

    def init_login(self):
        self.setWindowTitle("Данные пользователей")
        self.resize(600, 600)
        all_data = get_all_phone_book()

        len_data = len(all_data)
        self.model = QStandardItemModel(len_data, 3)

        self.model.setHorizontalHeaderLabels(['Имя', 'Телефон', 'Дата рождения'])

        self.tableview = QTableView()

        self.tableview.setModel(self.model)
        self.tableview.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        for i in range(len_data):
            for j in range(3):
                if j == 2:
                    data_add = datetime.datetime.strftime(all_data[i][j + 1], "%d-%m-%Y")
                else:
                    data_add = all_data[i][j + 1]
                self.model.setItem(i, j, QStandardItem(str(data_add)))

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableview)
        self.setLayout(self.layout)

        self.button1 = QPushButton("АБВГДЕ", self)
        self.button1.move(435, 42)
        self.button1.setFixedSize(145, 40)
        self.button1.setStyleSheet(border_style + 'background-color: #C0C0C0')
        self.button1.clicked.connect(self.view_data)

        self.button2 = QPushButton("ЖЗИЙКЛ", self)
        self.button2.move(435, 87)
        self.button2.setFixedSize(145, 40)
        self.button2.setStyleSheet(border_style + 'background-color: #C0C0C0')
        self.button2.clicked.connect(self.view_data)

        self.button3 = QPushButton("МНОПРС", self)
        self.button3.move(435, 132)
        self.button3.setFixedSize(145, 40)
        self.button3.setStyleSheet(border_style + 'background-color: #C0C0C0')
        self.button3.clicked.connect(self.view_data)

        self.button4 = QPushButton("ТУФХЦЧ", self)
        self.button4.move(435, 177)
        self.button4.setFixedSize(145, 40)
        self.button4.setStyleSheet(border_style + 'background-color: #C0C0C0')
        self.button4.clicked.connect(self.view_data)

        self.button5 = QPushButton("ШЩЪЫЬЭ", self)
        self.button5.move(435, 222)
        self.button5.setFixedSize(145, 40)
        self.button5.setStyleSheet(border_style + 'background-color: #C0C0C0')
        self.button5.clicked.connect(self.view_data)

        self.button6 = QPushButton("ЮЯ", self)
        self.button6.move(435, 267)
        self.button6.setFixedSize(145, 40)
        self.button6.setStyleSheet(border_style + 'background-color: #C0C0C0')
        self.button6.clicked.connect(self.view_data)

        self.button_add_new_user = QPushButton("Добавить контакт", self)
        self.button_add_new_user.move(435, 312)
        self.button_add_new_user.setFixedSize(145, 40)
        self.button_add_new_user.setStyleSheet(border_style + 'background-color: #C0C0C0')
        self.button_add_new_user.clicked.connect(self.add_new_person)

        self.button_update_user = QPushButton("Обновить контакт", self)
        self.button_update_user.move(435, 357)
        self.button_update_user.setFixedSize(145, 40)
        self.button_update_user.setStyleSheet(border_style + 'background-color: #C0C0C0')
        self.button_update_user.clicked.connect(self.update_person)

        self.button_delete_user = QPushButton("Удалить контакт", self)
        self.button_delete_user.move(435, 402)
        self.button_delete_user.setFixedSize(145, 40)
        self.button_delete_user.setStyleSheet(border_style + 'background-color: #C0C0C0')
        self.button_delete_user.clicked.connect(self.delete_person)

        self.exit = QPushButton("Разлогиниться", self)
        self.exit.move(435, 447)
        self.exit.setFixedSize(145, 40)
        self.exit.setStyleSheet(border_style + 'background-color: #C0C0C0')
        self.exit.clicked.connect(self.menu)

        self.close_app = QPushButton("Выйти", self)
        self.close_app.move(435, 492)
        self.close_app.setFixedSize(145, 40)
        self.close_app.setStyleSheet(border_style + 'background-color: #C0C0C0')
        self.close_app.clicked.connect(self.close_app_f)

    def birthday_week(self):
        self.win_birth = BirthdayWeekWin()
        self.win_birth.show()

    def menu(self):
        self.close()
        check_log_to_zero()
        self.win_menu = Main()
        self.win_menu.show()

    def close_app_f(self):
        self.close()
        sys.exit()

    def delete_person(self):
        self.window_delete_user = DeleteUser(new_user_class=self)
        self.window_delete_user.show()

    def update_person(self):
        self.window_update_user = UpdateUser(new_user_class=self)
        self.window_update_user.show()

    def add_new_person(self):
        self.window_add_new_user = AddNewUser(new_user_class=self)
        self.window_add_new_user.show()

    def view_data(self):
        button_text = QApplication.instance().sender().text()
        res = user_by_first_letters(button_text)

        self.window_finded = FindByLetters(data=res, letters=button_text)
        self.window_finded.show()


class BirthdayWeekWin(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ближайшие дни рождения")
        self.resize(430, 400)
        self.move(100, 100)

        all_data = get_birth()
        len_data = len(all_data)

        self.model = QStandardItemModel(len_data, 3)

        self.model.setHorizontalHeaderLabels(['Имя', 'Телефон', 'Дата рождения'])

        self.tableview = QTableView()

        self.tableview.setModel(self.model)
        for i in range(3):
            self.tableview.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
        for i in range(len_data):
            for j in range(3):
                if j == 2:
                    data_add = datetime.datetime.strftime(all_data[i][j + 1], "%d-%m-%Y")
                else:
                    data_add = all_data[i][j + 1]
                self.model.setItem(i, j, QStandardItem(str(data_add)))

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableview)
        self.setLayout(self.layout)


class DeleteUser(QtWidgets.QWidget):
    def __init__(self, new_user_class=None):
        super().__init__()

        self.setWindowTitle(f"Удаление контакта из книги")
        self.resize(400, 200)

        self.class_user = new_user_class

        self.username = QLineEdit(self)
        self.username.move(50, 20)
        self.username.setFixedSize(300, 35)
        self.username.setStyleSheet(border_style)
        self.username.setPlaceholderText("Имя пользователя")

        self.number = QLineEdit(self)
        self.number.move(50, 70)
        self.number.setFixedSize(300, 35)
        self.number.setStyleSheet(border_style)
        self.number.setPlaceholderText("Телефон")

        self.birthday = QLineEdit(self)
        self.birthday.move(50, 120)
        self.birthday.setFixedSize(300, 35)
        self.birthday.setStyleSheet(border_style)
        self.birthday.setPlaceholderText("Дата рождения а формате: DD-MM-YYYY")

        self.button_add_new_user = QPushButton("Удалить контакт", self)
        self.button_add_new_user.move(100, 165)
        self.button_add_new_user.setFixedSize(200, 30)
        self.button_add_new_user.setStyleSheet(border_style + 'background-color: #C0C0C0')
        self.button_add_new_user.clicked.connect(self.delete_from_db)

    def delete_from_db(self):
        res = delete_person(self.username.text(), self.number.text(), self.birthday.text())
        self.class_user.close()
        self.close()
        self.window_res = ResultFinishRegistr(result=res)
        self.window_res.show()


class UpdateUser(QtWidgets.QWidget):
    def __init__(self, new_user_class=None):
        super().__init__()

        self.setWindowTitle(f"Обновление контакта")
        self.resize(750, 200)

        self.class_user = new_user_class

        self.username = QLineEdit(self)
        self.username.move(50, 20)
        self.username.setFixedSize(300, 35)
        self.username.setStyleSheet(border_style)
        self.username.setPlaceholderText("Имя пользователя")

        self.username_new = QLineEdit(self)
        self.username_new.move(400, 20)
        self.username_new.setFixedSize(300, 35)
        self.username_new.setStyleSheet(border_style)
        self.username_new.setPlaceholderText("Новое имя пользователя")

        self.number = QLineEdit(self)
        self.number.move(50, 70)
        self.number.setFixedSize(300, 35)
        self.number.setStyleSheet(border_style)
        self.number.setPlaceholderText("Телефон")

        self.number_new = QLineEdit(self)
        self.number_new.move(400, 70)
        self.number_new.setFixedSize(300, 35)
        self.number_new.setStyleSheet(border_style)
        self.number_new.setPlaceholderText("Новый телефон или введите старый номер")

        self.birthday = QLineEdit(self)
        self.birthday.move(50, 120)
        self.birthday.setFixedSize(300, 35)
        self.birthday.setStyleSheet(border_style)
        self.birthday.setPlaceholderText("Дата рождения а формате: DD-MM-YYYY")

        self.birthday_new = QLineEdit(self)
        self.birthday_new.move(400, 120)
        self.birthday_new.setFixedSize(300, 35)
        self.birthday_new.setStyleSheet(border_style)
        self.birthday_new.setPlaceholderText("Дата рождения а формате: DD-MM-YYYY")

        self.button_add_new_user = QPushButton("Обновить контакт", self)
        self.button_add_new_user.move(275, 165)
        self.button_add_new_user.setFixedSize(200, 30)
        self.button_add_new_user.setStyleSheet(border_style + 'background-color: #C0C0C0')
        self.button_add_new_user.clicked.connect(self.update_db)

    def update_db(self):
        res = update_person(self.username.text(), self.number.text(), self.birthday.text(),
                         self.username_new.text(), self.number_new.text(), self.birthday_new.text())
        self.class_user.close()
        self.window_res = ResultFinishRegistr(result=res)
        self.window_res.show()


class AddNewUser(QtWidgets.QWidget):
    def __init__(self, new_user_class=None):
        super().__init__()
        self.class_user = new_user_class

        self.setWindowTitle(f"Добавление нового контакта в книгу")
        self.resize(400, 200)

        self.username = QLineEdit(self)
        self.username.move(50, 20)
        self.username.setFixedSize(300, 35)
        self.username.setStyleSheet(border_style)
        self.username.setPlaceholderText("Имя пользователя")

        self.number = QLineEdit(self)
        self.number.move(50, 70)
        self.number.setFixedSize(300, 35)
        self.number.setStyleSheet(border_style)
        self.number.setPlaceholderText("Телефон")

        self.birthday = QLineEdit(self)
        self.birthday.move(50, 120)
        self.birthday.setFixedSize(300, 35)
        self.birthday.setStyleSheet(border_style)
        self.birthday.setPlaceholderText("Дата рождения а формате: DD-MM-YYYY")

        self.button_add_new_user = QPushButton("Добавить контакт", self)
        self.button_add_new_user.move(100, 165)
        self.button_add_new_user.setFixedSize(200, 30)
        self.button_add_new_user.setStyleSheet(border_style + 'background-color: #C0C0C0')
        self.button_add_new_user.clicked.connect(self.add_to_db)

    def add_to_db(self):
        res = add_person(self.username.text(), self.number.text(), self.birthday.text())
        self.class_user.close()
        self.close()
        self.window_res = ResultFinishRegistr(result=res)
        self.window_res.show()


class FindByLetters(QtWidgets.QWidget):
    def __init__(self, parent=None, data=None, letters=None):
        super().__init__(parent)

        self.setWindowTitle(f"Данные пользователей по буквам {letters}")
        self.resize(410, 400)

        len_data = len(data)
        self.model = QStandardItemModel(len_data, 3)

        self.model.setHorizontalHeaderLabels(['Имя', 'Телефон', 'Дата рождения'])

        self.tableview = QTableView()

        self.tableview.setModel(self.model)
        self.tableview.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for i in range(len_data):
            for j in range(3):
                if j == 2:
                    data_add = datetime.datetime.strftime(data[i][j + 1], "%d-%m-%Y")
                else:
                    data_add = data[i][j + 1]
                self.model.setItem(i, j, QStandardItem(str(data_add)))

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableview)
        self.setLayout(self.layout)


class Registration(QtWidgets.QWidget):
    def __init__(self, parent=None, main_class=None):
        super().__init__(parent)
        self.resize(400, 350)
        self.setWindowTitle("Регистрация")

        self.main_class = main_class

        self.username = QLineEdit(self)
        self.username.move(50, 50)
        self.username.setFixedSize(300, 35)
        self.username.setStyleSheet(border_style)
        self.username.setPlaceholderText("Имя пользователя")

        self.password = QLineEdit(self)
        self.password.move(50, 95)
        self.password.setFixedSize(300, 35)
        self.password.setStyleSheet(border_style)
        self.password.setPlaceholderText("Пароль")

        self.password_reply = QLineEdit(self)
        self.password_reply.move(50, 140)
        self.password_reply.setFixedSize(300, 35)
        self.password_reply.setStyleSheet(border_style)
        self.password_reply.setPlaceholderText("Повторите пароль")

        self.birthday = QLineEdit(self)
        self.birthday.move(50, 185)
        self.birthday.setFixedSize(300, 35)
        self.birthday.setStyleSheet(border_style)
        self.birthday.setPlaceholderText("Дата рождения а формате: DD-MM-YYYY")

        self.new_user = QPushButton("Завершить регистрацию", self)
        self.new_user.move(100, 230)
        self.new_user.setFixedSize(200, 35)
        self.new_user.setStyleSheet(border_style + 'background-color: #C0C0C0')
        self.new_user.clicked.connect(self.finish_registration)

    def finish_registration(self):
        res = add_new_user(self.username.text(), self.password.text(), self.birthday.text())
        self.close()
        self.window_res = ResultFinishRegistr(result=res, main_class=self.main_class)
        self.window_res.show()


class ResultFinishRegistr(QtWidgets.QWidget):
    def __init__(self, parent=None, result=None, main_class=None):
        super().__init__(parent)
        self.result = result
        self.main_class = main_class
        self.check_reg = False

        self.resize(400, 200)
        self.res_str = QLabel(f"{self.result}", self)
        font = self.res_str.font()
        self.res_str.setFont(font)

        if self.main_class:
            if self.result == "Пользователь успешно добавлен!":
                self.check_reg = True
                self.main_class.close()
                self.open_login()
        else:
            self.open_login()

    def open_login(self):
        self.window_login = LoginWork(birthday=self.check_reg)
        self.window_login.show()


class PasswordRecovery(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(400, 350)
        self.setWindowTitle("Восстановление пароля")

        self.email = QLineEdit(self)
        self.email.move(100, 100)
        self.email.setFixedSize(200, 35)
        self.email.setStyleSheet(border_style)
        self.email.setPlaceholderText("Адрес электронной почты")

        self.new_pass = QPushButton("Сменить пароль", self)
        self.new_pass.move(125, 150)
        self.new_pass.setFixedSize(150, 35)
        self.new_pass.setStyleSheet(border_style + 'background-color: #C0C0C0')


class NoUserData(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(500, 200)
        self.setWindowTitle("Ошибка данных")
        self.error = QLabel("Пользователь с такими данными не найден или пустые записи!", self)
        font = self.error.font()
        self.error.setFont(font)

        self.error.adjustSize()


if __name__ == '__main__':

    init_db()
    app = QApplication(sys.argv)

    window = Main()
    window.show()

    app.exec()
