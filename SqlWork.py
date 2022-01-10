# -*- coding: utf-8 -*-

import psycopg2

class SqlRequest:
# Предполагается, что база данных и таблица уже созданы, необходимо указать пароль в init

    def __init__(self):
        self.sql_login = 'postgres'
        self.sql_pass = ''
        return

    def open_connection(self, db):
        print(f'host=localhost dbname={db} user={self.sql_login} password=<your password> port=5432')
        self.connection = psycopg2.connect(f'host=localhost dbname={db} user={self.sql_login} password={self.sql_pass} port=5432')
        self.cursor = self.connection.cursor()
        print("Соединение с PostgreSQL установлено")
        return

    def close_connection(self):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        print("Соединение с PostgreSQL закрыто")
        return

    def create_table(self, table):
        query = f'CREATE TABLE {table} (' \
                f'ID INT PRIMARY KEY NOT NULL,' \
                f'ID_VK INT NOT NULL' \
                f');'
        self.cursor.execute(query)
        self.connection.commit()
        print(f'Таблица {table} успешно создана')
        return

    def get_data(self, table):
        query = f'SELECT * from {table}'
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        id_dict = dict(data)
        id_list = list(id_dict.values())
        return id_list

    def insert_data(self, table, vk_id, number):
        query = f'INSERT INTO {table} (ID, ID_VK) VALUES ({number}, {vk_id})'
        self.cursor.execute(query)
        return

