from pprint import pprint
import csv
import re

class csv_correct():
    def __init__(self, filename):
        # читаем адресную книгу в формате CSV в список contacts_list

        with open(filename, encoding='utf-8') as f:
            rows = csv.reader(f, delimiter=",")
            self.contacts_list = list(rows)


    def correct_fio_by_list(self):
        # исправление фио в контакт-листе
        for list_str in self.contacts_list:
            fio = f'{list_str[0]} {list_str[1]} {list_str[2]}'
            fio_list = fio.split()
            for index, word in enumerate(fio_list):
                list_str[index] = word


    def correct_phones_by_list(self):
        # приведение телефонов к общему виду (regexp)
        pattern = re.compile(r'(\+7|8)?\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]?(\d{2})[\s-]?'
                             r'(\d{2})\s*\(?(доб.)?\s*(\d*)\)?')

        substitution = r"+7(\2)\3-\4-\5 \6\7"
        for list_str in self.contacts_list:
            phone = list_str[5]
            result = pattern.sub(substitution, phone)
            list_str[5] = result


    def create_union_list(self):
        #считаем, что человек одинаковый, если совпадает Фамилия и имя
        #алгоритм: в словаре union_dict ключом будет Фамилия + ' ' + Имя, значением - индекс в итоговом списке
        #на каждом витке цикла ищем запись в словаре по ключу, если есть - объединяем с уже существующим в итоговом
        #списке, если нет - добавляем и в список, и в словарь.
        #при объединении считаем что существующая запись приоритетная, туда только добавляются не заполненные поля

        union_list = []
        union_dict = {}
        for list_str in self.contacts_list:
            key = list_str[0] + ' ' + list_str[1]
            final_index = union_dict.get(key)
            if final_index is None:
                #новая строка, просто добавляем в финальный список
                union_list.append(list_str)
                union_dict[key] = len(union_list)-1
            else:
                #объединение каждого столбца, всего их 7, проходим в цикле
                for str_index in range(7):
                    if union_list[final_index][str_index] == '':
                        union_list[final_index][str_index] = list_str[str_index]
        return union_list

    def save_correct_contactslist_to_file(self, filename):
        self.correct_fio_by_list()
        self.correct_phones_by_list()
        correct_list = self.create_union_list()

        with open(filename, "w", encoding='utf-8', newline='') as f:
            datawriter = csv.writer(f, delimiter=',')
            datawriter.writerows(correct_list)


if __name__ == '__main__':
    filename = 'files\phonebook_raw.csv'
    new_filename = 'files\phonebook.csv'

    csv_correct_obj = csv_correct(filename)
    csv_correct_obj.save_correct_contactslist_to_file(new_filename)
