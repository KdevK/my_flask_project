import math
import sqlite3
import time


class FlaskDataBase:

    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_menu(self):
        """Returns all menu items from mainmenu table."""
        query = "SELECT * from mainmenu"
        try:
            self.__cur.execute(query)
            res = self.__cur.fetchall()
            if res:
                return res
        except Exception as e:
            print(f"Unexpected exception {e}")
        return []

    def add_post(self, title, content):
        pub_date = math.floor(time.time())
        try:
            self.__cur.execute(
                "INSERT INTO posts VALUES (NULL, ?, ?, ?)",
                (title, content, pub_date)
            )
            self.__db.commit()
        except sqlite3.Error as e:
            print(f"Error adding post to database: {e}")
            return False
        return True

    def get_posts(self):
        try:
            self.__cur.execute(
                "SELECT id, title, content FROM posts ORDER BY pub_date DESC"
            )
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print(f"Exception in getting posts list: {e}")
        return []

    def get_post_content(self, post_id):
        try:
            self.__cur.execute(
                f"SELECT title, content FROM posts WHERE id = {post_id}"
            )
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print(f"Exception in getting post by id {post_id}: {e}")
        return False, False

    def add_user(self, name, email, hpsw):
        try:
            self.__cur.execute(f'SELECT COUNT() as `count` FROM users WHERE email LIKE "{email}"')
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('Пользователь с таким email уже существует')
                return False

            tm = math.floor(time.time())
            self.__cur.execute('INSERT INTO users VALUES(NULL, ?, ?, ?, ?)', (name, email, hpsw, tm))

            self.__db.commit()
        except sqlite3.Error as e:
            print(f'Ошибка добавления пользователя в БД: {e}')
            return False

        return True

    def get_user(self, user_id):
        try:
            self.__cur.execute(f'SELECT * FROM users WHERE id = {user_id} LIMIT 1')
            res = self.__cur.fetchone()
            if not res:
                print('Пользователь не найден')
                return False

            return res

        except sqlite3.Error as e:
            print(f'Ошибка получения данных из БД: {e}')

        return False

    def get_user_by_email(self, email):
        try:
            self.__cur.execute(f'SELECT * FROM users WHERE email = "{email}" LIMIT 1')
            res = self.__cur.fetchone()
            if not res:
                print('Пользователь не найден')
                return False

            return res

        except sqlite3.Error as e:
            print(f'Ошибка получения данных из БД: {e}')

        return False



