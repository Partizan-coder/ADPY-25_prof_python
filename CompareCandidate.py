# -*- coding: utf-8 -*-
import random

import requests
import vk_api
import time
from random import randrange

class CandidateComparison:
    def __init__(self):
    #Инициализируем класс сравнения, задавая параметры поиска.
        user_id = input('Введите ваш id в ВК для поиска:  ')
        user_name = input('Введите ваше имя для поиска:  ')
        user_response = input('Хотите ввести дополнительные параметры для поиска (да / нет):  ')
        if user_response == 'да':
            input('Все параметры обязательны для заполнения (кроме "родной город кандидата")')
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
            candidate_min_age = '18'
            candidate_max_age = '65'
            candidate_sex = '0'
            candidate_city = ''
            candidate_family = '0'
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
        if photos_count > 50:
            photos_count = 50
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

def write_msg(user_id, candidate_id, photos_dict):
# Пишем сообщения в чат и передаем 3 фото или меньше, если в альбоме было меньше 3 фото
    group_vk_access_key = '1b5ff74b46692932fecad7f1e248efce9874c6f7130c0b97af702b5d1fd9571f67deeed11b0351066c01f'
    vk_message = vk_api.VkApi(token=group_vk_access_key)
    candidate_link = f'https://vk.com/id{candidate_id}'
    dict_len = len(photos_dict)
    photos_list = list(photos_dict.values())
    if dict_len >= 3:
        vk_message.method('messages.send', {'user_id': user_id, 'message': candidate_link, 'random_id': randrange(10000000)})
        for i in range(3):
            vk_message.method('messages.send', {'user_id': user_id, 'random_id': randrange(10000000), 'attachment': f'photo{candidate_id}_{photos_list[i-1]}'})
    # Если в альбоме фото профиля пользователя менее трех фото
    else:
        vk_message.method('messages.send', {'user_id': user_id, 'message': candidate_link, 'random_id': -randrange(10000000)})
        for i in range(dict_len):
            vk_message.method('messages.send', {'user_id': user_id, 'random_id': randrange(10000000), 'attachment': f'photo{candidate_id}_{photos_list[i - 1]}'})