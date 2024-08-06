# модуль
import csv

def import_data_visitors(data, sep=','):
    # print(data)
    first_name= data.first_name  #'Sebastian Pereira'
    id_visitor = data.id #397081859, 
    is_bot = data.is_bot # False, 
    language_code = data.language_code #'ru', 
    username = data.username #'SlavaDoc'
    print(first_name +  str(id_visitor) + str(is_bot) + language_code )
    username = data.username #'SlavaDoc')

    d = open('visitors.csv', 'r')
    s = d.read()
    id = 1
    if s == '':
        id = 1
    else:
        for i in s:
            if i == '\n':
                id += 1
    d.close()
#  with open('flats.csv', 'w', encoding='utf-8-sig') as file
    with open('visitors.csv', 'a+', encoding='utf-8-sig') as file:
        file.write(str(id)+ sep  + first_name + sep + username + sep + str(id_visitor) + sep + language_code + sep + str(is_bot))
        file.write(f"\n")
        # if sep == None:
        #     for i in da:
        #         file.write(f"{i}\n")
        #     file.write(f"\n")
        # else:
        #     file.write(str(id) + sep + sep.join(da))
        #     file.write(f"\n")

