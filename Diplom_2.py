# -*- coding: utf-8 -*-

import requests
import vk_api
import time
import psycopg2
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange

class CandidateComparison:
    def __init__(self):
    #Инициализируем класс сравнения, задавая параметры поиска.
        user_id = input('Введите ваш id в ВК для поиска:  ')
        user_name = input('Введите ваше имя для поиска:  ')
        user_response = input('Хотите ввести дополнительные параметры для поиска (да / нет):  ')
        if user_response == 'да':
            input('Все параметры обязательны для заполнения (за исключением "родной город кандидата"!')
            candidate_min_age = input('\nВведите нижнюю границу возраста кандидата для поиска (по умолчанию 18 лет):  ')
            candidate_max_age = input('\nВведите верхнюю границу возраста кандидата для поиска (по умолчанию 65 лет):  ')
            candidate_sex = input('\nВведите пол кандидата для поиска (по умолчанию - 0):  \n'
                                  '1 — женский;\n'
                                  '2 — мужской;\n'
                                  '0 — пол не указан.\n'
                                  'Укажите число из вариантов выше, соответствующее цели поиска:  ')
            candidate_city = input('\nВведите родной город кандидата для поиска (по умолчанию - не указан):  ')
            candidate_family = input('\nВведите семейное положение кандидата для поиска (по умолчанию - 0):  \n'
                                     '1 — не женат/не замужем; \n'
                                     '2 — есть друг/есть подруга; \n'
                                     '3 — помолвлен/помолвлена; \n'
                                     '4 — женат/замужем; \n'
                                     '5 — всё сложно; \n'
                                     '6 — в активном поиске; \n'
                                     '7 — влюблён/влюблена; \n'
                                     '8 — в гражданском браке; \n'
                                     '0 — не указано. \n'
                                     'Укажите число из вариантов выше, соответствующее цели поиска:  ')
        else:
            user_id = ''
            candidate_min_age = '18'
            candidate_max_age = '65'
            candidate_sex = '0'
            candidate_city = ''
            candidate_family = '0'
        user_id = 646455113
        self.candidate_searching_parameters = {'user_id': user_id, 'user_name': user_name, 'min_age': candidate_min_age, 'max_age': candidate_max_age, 'sex': candidate_sex, 'city': candidate_city, 'family': candidate_family}
        return

    def compare_parameters(self, vk_candidate):
    #Сравниваем кандидата с заданными параметрами и выдаем логический ответ "подходит / не подходит"
        if vk_candidate.candidate_info['response'][0].get('first_name') == 'DELETED':
            logic = False
        else:
            min_age = int(self.candidate_searching_parameters['min_age'])
            max_age = int(self.candidate_searching_parameters['max_age'])
            sex = self.candidate_searching_parameters['sex']
            city = self.candidate_searching_parameters['city']
            family = self.candidate_searching_parameters['family']

            home_town = vk_candidate.candidate_info['response'][0].get('home town')
            candidate_sex = vk_candidate.candidate_info['response'][0].get('sex')
            candidate_bdate = str(vk_candidate.candidate_info['response'][0].setdefault(('bdate'), 2003))
            candidate_bdate = candidate_bdate[-4::]
            if '.' in candidate_bdate or candidate_bdate == None:
                candidate_bdate = 2003
            candidate_age = 2021 - int(candidate_bdate)
            candidate_relation = vk_candidate.candidate_info['response'][0].setdefault('relation','0')
            logic = False
            if min_age <= candidate_age and candidate_age <= max_age:
                if candidate_sex == sex or sex == '0':
                    if home_town == city or city == '':
                        if family == candidate_relation or family == '0':
                            logic = True
        return logic

class VkCandidate:

    def __init__(self, candidate_id):
        self.vk_access_token = '14ecbd7414ecbd7414ecbd748d149baf43114ec14ecbd7474b10e46ed414ad017577f67'
        # self.vk_access_token = '81aa405d81aa405d81aa405d6581d0e21b881aa81aa405de06326507d3ba5e73b2279a0'
        candidate = f'https://api.vk.com/method/users.get?user_ids={candidate_id}&fields=bdate,home_town,sex,relation&rev=0&v=5.131&access_token={self.vk_access_token}'
        time.sleep(1)
        self.candidate_info = requests.get(candidate).json()
        self.photo_url_list = []
        self.likes_list = []
        self.sizes = []
        return

    def get_photo(self, candidate_id):
        request = f'https://api.vk.com/method/photos.get?owner_id={candidate_id}&album_id=profile&extended=1&rev=0&v=5.131&access_token={self.vk_access_token}'
        time.sleep(1)
        request_photo = requests.get(request).json()
        if request_photo.setdefault('response') is None:
            request_photo = ''
            self.no_photo = True
        else:
            self.no_photo = False
        return request_photo

    def get_photos_dict(self, request):
    # Создаем словарь типа {количество лайков: id_фоторафии} на основании полученных фото из get_photo
        photos_count = int(request['response']['count'])
        self.photos_dict = {}
        for i in range(photos_count):
            key_likes = request['response']['items'][i]['likes'].setdefault('count', 0)
            value_url = request['response']['items'][i]['id']
            self.photos_dict[key_likes] = value_url
        sorted_photos_dict = sorted(self.photos_dict.items(), key=lambda x: x[0], reverse=True)
        self.photos_dict = dict(sorted_photos_dict)
        if len(self.photos_dict) > 0:
            self.dict_is_empty = False
        else:
            self.dict_is_empty = True
        return self.photos_dict

class SqlRequest:
# Предполагается, что база данных и таблица уже созданы, необходимо указать пароль в init

    def __init__(self):
        self.sql_login = 'postgres'
        self.sql_pass = ''
        return

    def open_connection(self, db):
        print(f'host=localhost dbname={db} user={self.sql_login} password={self.sql_pass} port=5432')
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

def write_msg(user_id, candidate_id, photos_dict):
# Пишем сообщения в чат и передаем 3 фото или меньше, если в альбоме было меньше 3 фото
    group_vk_access_key = '1b5ff74b46692932fecad7f1e248efce9874c6f7130c0b97af702b5d1fd9571f67deeed11b0351066c01f'
    vk_message = vk_api.VkApi(token=group_vk_access_key)
    candidate_link = f'https://vk.com/id{candidate_id}'
    dict_len = len(photos_dict)
    photos_list = list(photos_dict.values())
    if dict_len >= 3:
        vk_message.method('messages.send', {'user_id': user_id, 'message': candidate_link, 'random_id': randrange(10 ** 7)})
        for i in range(3):
            vk_message.method('messages.send', {'user_id': user_id, 'random_id': randrange(10 ** 7), 'attachment': f'photo{candidate_id}_{photos_list[i-1]}'})
    else:
        vk_message.method('messages.send', {'user_id': user_id, 'message': candidate_link, 'random_id': randrange(10 ** 7)})
        for i in range(dict_len):
            vk_message.method('messages.send', {'user_id': user_id, 'random_id': randrange(10 ** 7), 'attachment': f'photo{candidate_id}_{photos_list[i - 1]}'})

if __name__ == '__main__':
# Из базы данных получаем список ID пользователей, которые уже попадали в выборку, генерируем заданное количество
# пользователей ВК, сравниваем их с заданными параметрами и при сооответствии посылаем в чат и добавляем в таблицу
# базы данных.
    sql = SqlRequest()
    sql.open_connection('Diplome_module_2')
    candidate_list = sql.get_data('Diplom_2')
    new_candidate_list = []
    comparison = CandidateComparison()
    candidate_count = input('Введите количество кандидатов для поиска:  ')
    for i in range(int(candidate_count)):
        candidate_id = randrange(10 ** 7)
        if candidate_id not in candidate_list:
            candidate = VkCandidate(candidate_id)
            if comparison.compare_parameters(candidate) == True:
                print('Кандидат подходит по параметрам')
                vk_request = candidate.get_photo(candidate_id)
                if candidate.no_photo == True:
                    print('У кандидата нет фото_1')
                else:
                    print('VK_request для фото:\n', vk_request)
                    photos_dict = candidate.get_photos_dict(vk_request)
                    if candidate.dict_is_empty != True:
                        new_candidate_list.append(candidate_id)
                        write_msg(comparison.candidate_searching_parameters.get('user_id'), candidate_id, photos_dict)
            else:
                print('Кандидат не подходит по параметрам')

    len_new_cand_list = len(new_candidate_list)
    len_cand_list = len(candidate_list)
    for i in range(len_new_cand_list):
        added_candidate = new_candidate_list[i]
        sql.insert_data('Diplom_2', added_candidate, len_cand_list + i - 1)

    sql.close_connection()
