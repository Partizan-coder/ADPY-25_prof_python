# -*- coding: utf-8 -*-

import SqlWork
import CompareCandidate
import vk_api
from random import randrange

if __name__ == '__main__':
# Из базы данных получаем список ID пользователей, которые уже попадали в выборку, случайным образом выбираем заданное количество
# пользователей ВК, сравниваем их с введенными параметрами и при сооответствии посылаем в чат фото кандидата и добавляем его ID в таблицу
# базы данных.
    sql = SqlWork.SqlRequest()
    sql.open_connection('Diplome_module_2')
    candidate_list = sql.get_data('Diplom_2')
    new_candidate_list = []
    comparison = CompareCandidate.CandidateComparison()
    candidate_count = input('Введите количество кандидатов для поиска:  ')
    for i in range(int(candidate_count)):
        candidate_id = randrange(10 ** 7)
        if candidate_id not in candidate_list:
            candidate = CompareCandidate.VkCandidate(candidate_id)
            if comparison.compare_parameters(candidate) == True:
                vk_request = candidate.get_photo(candidate_id)
                if candidate.no_photo != True:
                    photos_dict = candidate.get_photos_dict(vk_request)
                    if candidate.dict_is_empty != True:
                        new_candidate_list.append(candidate_id)
                        CompareCandidate.write_msg(comparison.candidate_searching_parameters.get('user_id'), candidate_id, photos_dict)

    len_new_cand_list = len(new_candidate_list)
    len_cand_list = len(candidate_list)
    for i in range(len_new_cand_list):
        added_candidate = new_candidate_list[i]
        sql.insert_data('Diplom_2', added_candidate, len_cand_list + i - 1)
    sql.close_connection()
