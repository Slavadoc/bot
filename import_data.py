# модуль
import csv

def import_data(data, sep=','):
    name, number = "",""
    for key, value in data.items():
        if isinstance(value, dict):
            print(value)
            for k,v in value.items(): 
                if k == '\x11':
                    name = v
                    print(f" name: {v}")
                if k == '\x10':
                    number = v
                    print(f" number: {v}")
    d = open('customers.csv', 'r')
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
    with open('customers.csv', 'a+', encoding='utf-8-sig') as file:
        file.write(str(id)+ sep  + name + sep + number)
        file.write(f"\n")
        # if sep == None:
        #     for i in da:
        #         file.write(f"{i}\n")
        #     file.write(f"\n")
        # else:
        #     file.write(str(id) + sep + sep.join(da))
        #     file.write(f"\n")

