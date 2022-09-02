import mysql.connector as mariadb
import datetime
from config import user, password, host, database


def init_db():
    mariadb_connection = mariadb.connect(user=user, password=password, host=host)
    cursor = mariadb_connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS vista")
    mariadb_connection = mariadb.connect(user=user, password=password,
                                         host=host, database=database)
    cursor = mariadb_connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users ("
                   "user_id INT PRIMARY KEY AUTO_INCREMENT, "
                   "username VARCHAR(30) NOT NULL, "
                   "password VARCHAR(50) NOT NULL, "
                   "birthday DATE NOT NULL, "
                   "check_log VARCHAR(1) DEFAULT '0')")
    cursor.execute("CREATE TABLE IF NOT EXISTS phone_book ("
                   "user_id INT PRIMARY KEY AUTO_INCREMENT, "
                   "book_name VARCHAR(30) NOT NULL, "
                   "number VARCHAR(50) NOT NULL, "
                   "birthday DATETIME NOT NULL )")
    cursor.close()


def add_new_user(username, password, birtday):
    mariadb_connection = mariadb.connect(user=user, password=password,
                                         host=host, database=database)
    cursor = mariadb_connection.cursor()

    if username and password and birtday:

        birtday = datetime.datetime.strptime(birtday, "%d-%m-%Y")

        cursor.execute("SELECT * FROM users where username = %s;",
                       (username, ))
        check_user = cursor.fetchall()

        if check_user:
            return "Пользователь с таким именем уже существует!"

        cursor.fetchall()
        cursor.execute(f"INSERT INTO users (username, password, birthday) VALUES (%s, %s, %s)",
                       (username, password, birtday,))
        mariadb_connection.commit()
        return "Пользователь успешно добавлен!"
    else:
        return "Одно или несколько полей - пустые!"


def check_data_to_login(username, password):
    if username and password:
        mariadb_connection = mariadb.connect(user=user, password=password,
                                             host=host, database=database)
        cursor = mariadb_connection.cursor()
        cursor.execute("SELECT * FROM users where username = %s and password = %s;",
                       (username, password,))
        check_user = cursor.fetchall()
        return check_user
    else:
        return False


def get_all_phone_book():
    mariadb_connection = mariadb.connect(user=user, password=password,
                                         host=host, database=database)
    cursor = mariadb_connection.cursor()
    cursor.execute("SELECT * FROM phone_book ORDER BY book_name")
    result = cursor.fetchall()
    return result


def user_by_first_letters(letters):
    mariadb_connection = mariadb.connect(user=user, password=password,
                                         host=host, database=database)
    cursor = mariadb_connection.cursor()

    list_data = []
    for letter in letters:
        cursor.execute(f"SELECT * FROM phone_book WHERE book_name LIKE '{letter}%'")
        list_data += cursor.fetchall()

    return list_data


def add_person(username, number, birthday):
    mariadb_connection = mariadb.connect(user=user, password=password,
                                         host=host, database=database)
    cursor = mariadb_connection.cursor()

    if username and number and birthday:

        birthday = datetime.datetime.strptime(birthday, "%d-%m-%Y")

        cursor.execute("SELECT * FROM phone_book where book_name = %s and number = %s and birthday = %s;",
                       (username, number, birthday))
        check_user = cursor.fetchall()

        if check_user:
            return "Пользователь с такими данными уже существует!"

        cursor.fetchall()
        cursor.execute(f"INSERT INTO phone_book (book_name, number, birthday) VALUES (%s, %s, %s)",
                       (username, number, birthday,))
        mariadb_connection.commit()
        return f"Контакт успешно добавлен в список с буквой: {username[:1]}!"
    else:
        return "Одно или несколько полей - пустые!"


def update_person(username, number, birthday, new_username, new_number, new_birtday):
    mariadb_connection = mariadb.connect(user=user, password=password,
                                         host=host, database=database)
    cursor = mariadb_connection.cursor()

    if username and number and birthday and new_number and new_username and new_birtday:

        birthday = datetime.datetime.strptime(birthday, "%d-%m-%Y")
        new_birtday = datetime.datetime.strptime(new_birtday, "%d-%m-%Y")

        cursor.execute("SELECT * FROM phone_book where book_name = %s and number = %s and birthday = %s;",
                       (username, number, birthday))
        check_user = cursor.fetchall()

        if not check_user:
            return "Пользователя с такими данными не существует!"

        cursor.fetchall()
        cursor.execute(f"UPDATE phone_book SET book_name = %s, number = %s, birthday = %s "
                       f"WHERE book_name = %s and number = %s and birthday = %s;",
                       (new_username, new_number, new_birtday, username, number, birthday, ))
        mariadb_connection.commit()
        return f"Контакт успешно обновлён в список с буквой: {new_username[:1]}!"
    else:
        return "Одно или несколько полей - пустые!"


def delete_person(username, number, birthday):
    mariadb_connection = mariadb.connect(user=user, password=password,
                                         host=host, database=database)
    cursor = mariadb_connection.cursor()

    if username and number and birthday:

        birthday = datetime.datetime.strptime(birthday, "%d-%m-%Y")

        cursor.execute("SELECT * FROM phone_book where book_name = %s and number = %s and birthday = %s;",
                       (username, number, birthday))
        check_user = cursor.fetchall()

        if not check_user:
            return "Контакта с такими данными не существует!"

        cursor.fetchall()
        cursor.execute(f"DELETE FROM phone_book WHERE book_name = %s and number = %s and birthday = %s;",
                       (username, number, birthday, ))
        mariadb_connection.commit()
        return f"Контакт успешно удалён из списка с буквой: {username[:1]}!"
    else:
        return "Одно или несколько полей - пустые!"


def get_birth():
    today = datetime.datetime.now()
    end_day = today + datetime.timedelta(days=7)

    mariadb_connection = mariadb.connect(user=user, password=password,
                                         host=host, database=database)
    cursor = mariadb_connection.cursor()

    cursor.execute("SELECT * FROM phone_book")
    res = cursor.fetchall()
    list_res = []
    for data in res:
        date = data[3]
        if today.month <= date.month <= end_day.month and today.day <= date.day <= end_day.day:
            list_res.append(data)
    return list_res


def update_check_log(check_log, username, password):
    mariadb_connection = mariadb.connect(user=user, password=password,
                                         host=host, database=database)
    cursor = mariadb_connection.cursor()

    cursor.execute(f"UPDATE users SET check_log = %s WHERE username = %s and password = %s;",
                   (check_log, username, password))
    mariadb_connection.commit()


def some_check_log():
    mariadb_connection = mariadb.connect(user=user, password=password,
                                         host=host, database=database)
    cursor = mariadb_connection.cursor()

    cursor.execute(f"SELECT username, password FROM users WHERE check_log = '1';")
    return cursor.fetchall()


def check_log_to_zero():
    mariadb_connection = mariadb.connect(user=user, password=password,
                                         host=host, database=database)
    cursor = mariadb_connection.cursor()

    cursor.execute(f"UPDATE users SET check_log = '0';")
    mariadb_connection.commit()
