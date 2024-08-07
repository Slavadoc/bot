# модуль
import csv

def import_data_visitors(data, sep=','):
    print(type(data))
    print(data.message)
    # print(data.message.date)
    print(data.message.from_user)

#2024-08-06 23:21:12,406 - telegram.ext.Application - INFO - Application started
# Update(message=Message(channel_chat_created=False, 
#  chat=Chat(first_name='Sebastian Pereira', id=397081859, type=<ChatType.PRIVATE>, username='SlavaDoc'), 
# date=datetime.datetime(2024, 8, 6, 20, 21, 18, tzinfo=datetime.timezone.utc), 
# delete_chat_photo=False, entities=(MessageEntity(length=6, offset=0, type=<MessageEntityType.BOT_COMMAND>),), 
# from_user=User(first_name='Sebastian Pereira', id=397081859, is_bot=False, language_code='ru', username='SlavaDoc'), 
# group_chat_created=False, message_id=1056, supergroup_chat_created=False, text='/start'), update_id=34404894)


#     first_name= data.first_name  #'Sebastian Pereira'
#     id_visitor = data.id #397081859, 
#     is_bot = data.is_bot # False, 
#     language_code = data.language_code #'ru', 
#     username = data.username #'SlavaDoc'
#     print(first_name +  str(id_visitor) + str(is_bot) + language_code )
#     username = data.username #'SlavaDoc')

#     d = open('visitors.csv', 'r')
#     s = d.read()
#     id = 1
#     if s == '':
#         id = 1
#     else:
#         for i in s:
#             if i == '\n':
#                 id += 1
#     d.close()
# #  with open('flats.csv', 'w', encoding='utf-8-sig') as file
#     with open('visitors.csv', 'a+', encoding='utf-8-sig') as file:
#         file.write(str(id)+ sep  + first_name + sep + username + sep + str(id_visitor) + sep + language_code + sep + str(is_bot))
#         file.write(f"\n")
        # if sep == None:
        #     for i in da:
        #         file.write(f"{i}\n")
        #     file.write(f"\n")
        # else:
        #     file.write(str(id) + sep + sep.join(da))
        #     file.write(f"\n")

