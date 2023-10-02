import telebot
from telebot import types

import logging
import msg
import os
import keybords
from config import TOKEN, ADMIN_ID
from datetime import datetime
from sqliteormmagic import SQLiteDB
import pytz

def get_msk_time() -> datetime:
    time_now = datetime.now(pytz.timezone("Europe/Moscow"))
    time_now = time_now.strftime('%Y-%m-%d %H:%M:%S')
    return time_now


db_bass = SQLiteDB('bass.db')
db_users = SQLiteDB('users.db')
def pars_bass_list(num):
    res = db_bass.find_elements_in_column(table_name='bass', key_name=num, column_name='rayon')
    text = 'Выберите бассейн из списка, чтобы продолжить список нажмите кнопку <b>еще</b> ▶️'
    list_buttons = []
    for bass in res:
        text += f"""
<b>{bass[0]} {bass[1]}</b>
<a href="{bass[3]}">{bass[2]}</a>
"""
        list_buttons.append(bass[0])

    return text, list_buttons

def find_bass_trip(num):
    res = db_bass.find_elements_in_column(table_name='bass', key_name=num, column_name='rayon')
    text = """Список бассейнов ⤵️ 
чтобы просмотреть остальные нажмите кнопку <b>еще</b> ▶️"""
    list_buttons = []
    for bass in res:
        text += f"""
<b>{bass[0]} {bass[1]}</b>
<a href="{bass[3]}">{bass[2]}</a>
"""
        list_buttons.append(bass[0])

    return text


bot = telebot.TeleBot(token=TOKEN, parse_mode='HTML', skip_pending=True)    
# bot.set_my_commands(
#     commands=[
#         telebot.types.BotCommand("start", "Запуск бота"),
#     ],)


def main():
    @bot.message_handler(commands=['start'])
    def start_fnc(message):
        
        db_users.create_table('users', [
            ('from_user_id', 'INTEGER UNIQUE'), 
            ('from_user_username', 'TEXT'),
            ('name', 'TEXT'),
            ('phone', 'TEXT'),
            ('status', 'TEXT'),            
            ('regtime', 'TEXT'),
            ('age', 'TEXT'),            
            ('lvl', 'TEXT'),
            ('bassein', 'TEXT'),
            ('bassein_list', 'INTEGER'),
            ('events', 'TEXT'),
        ])
        db_users.ins_unique_row('users', [
            ('from_user_id', message.from_user.id),
            ('from_user_username', message.from_user.username),
            ('name', '0'),
            ('phone', '0'),
            ('status', '0'),   
             ('regtime', get_msk_time()),
            ('age', '0'),   
            ('lvl', '0'),
            ('bassein', '0'),
            ('bassein_list', 1),            
            ('events', '0'),

        ])
        m = bot.send_message(chat_id=message.from_user.id, text=msg.start_msg)
        bot.register_next_step_handler(m, get_fio)



    @bot.message_handler(content_types=['video'])
    def get_video(message):
        video = message.video.file_id
        file_info = bot.get_file(video)
        video = bot.download_file(file_info.file_path)
         
    @bot.message_handler(content_types=['document'])
    def get_document(message):
        document = message.document.file_id
        file_info = bot.get_file(document)
        document = bot.download_file(file_info.file_path)
        

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        if call.data == 'first':
            status = 'new'
            bot.send_message(chat_id=call.from_user.id, text=msg.age_msg, reply_markup=keybords.age_board())
            db_users.upd_element_in_column(table_name='users', upd_par_name='status', key_par_name=status, upd_column_name='from_user_id', key_column_name=call.from_user.id)      
        
        elif 'age' in call.data:
            age = call.data.split("::")[1]
            bot.send_message(chat_id=call.from_user.id, text=msg.age_msg, reply_markup=keybords.lvl_board())
            db_users.upd_element_in_column(table_name='users', upd_par_name='age', key_par_name=age, upd_column_name='from_user_id', key_column_name=call.from_user.id)      
        
        elif 'lvl' in call.data:
            lvl = call.data.split("::")[1]
            res = db_users.find_elements_by_keyword(table_name='users', key_name=call.from_user.id, column_name='from_user_id')
            print(res)
            res = res [0]
            num = res[9]
            text, list_buttons = pars_bass_list(num=num)
            print(list_buttons)
            bot.send_message(call.from_user.id, text=text, disable_web_page_preview= True, reply_markup=keybords.choice_bassein_board(list_bass=list_buttons)) 
            db_users.upd_element_in_column(table_name='users', upd_par_name='lvl', key_par_name=lvl, upd_column_name='from_user_id', key_column_name=call.from_user.id)      

        elif 'bas_next' in call.data:
            res = db_users.find_elements_by_keyword(table_name='users', key_name=call.from_user.id, column_name='from_user_id')
            print(res)
            res = res [0]
            num = res[9]
            if num == 5:
                num = 1
            else:
                num = num + 1

            text, list_buttons = pars_bass_list(num=num)
            print(list_buttons)
            bot.send_message(call.from_user.id, text=text, disable_web_page_preview= True, reply_markup=keybords.choice_bassein_board(list_bass=list_buttons)) 
            db_users.upd_element_in_column(table_name='users', upd_par_name='bassein_list', key_par_name=num, upd_column_name='from_user_id', key_column_name=call.from_user.id)      
        
        elif 'bass' in call.data:

            bassein = call.data.split("::")[1]
            bot.send_message(call.from_user.id, text=msg.success_input_voronka_msg, disable_web_page_preview= True, reply_markup=keybords.back()) 
            db_users.upd_element_in_column(table_name='users', upd_par_name='bassein', key_par_name=bassein, upd_column_name='from_user_id', key_column_name=call.from_user.id)      

            res_user = db_users.find_elements_by_keyword(table_name='users', key_name=call.from_user.id, column_name='from_user_id')
            res_user = res_user[0]
            print(res_user)

            res_bass = db_bass.find_elements_in_column(table_name='bass', key_name=bassein, column_name='num')
            res_bass = res_bass[0]
            print(res_bass)
            text = f"""
Имя {res_user[2]}
Username {res_user[1]}
Статус {res_user[4]}
Тел. {res_user[3]}
Возраст {res_user[6]}
Уровень {res_user[7]}
Бассейн № {res_bass[0]}
{res_bass[1]}
{res_bass[2]}
"""
            bot.send_message(chat_id=ADMIN_ID, text=text)
            db_users.upd_element_in_column(table_name='users', upd_par_name='status', key_par_name='old', upd_column_name='from_user_id', key_column_name=call.from_user.id)      
        
        
        elif call.data == 'no_first':
            status = 'old'
            bot.send_message(call.from_user.id, text=msg.back_msg, disable_web_page_preview= True, reply_markup=keybords.main_board()) 
            db_users.upd_element_in_column(table_name='users', upd_par_name='status', key_par_name=status, upd_column_name='from_user_id', key_column_name=call.from_user.id)      

        elif call.data == 'discount':

            m = bot.send_message(chat_id=call.from_user.id, text=msg.discount_msg)
            bot.register_next_step_handler(m, get_discount)

        elif call.data =='trip':
            res = db_users.find_elements_by_keyword(table_name='users', key_name=call.from_user.id, column_name='from_user_id')
            print(res)
            res = res [0]
            num = res[9]
            text = find_bass_trip(num=num)
            bot.send_message(chat_id=call.from_user.id, text=text, disable_web_page_preview= True, reply_markup=keybords.trip_bassein_board())    

        elif 'trip_next' in call.data:
            res = db_users.find_elements_by_keyword(table_name='users', key_name=call.from_user.id, column_name='from_user_id')
            print(res)
            res = res [0]
            num = res[9]
            if num == 5:
                num = 1
            else:
                num = num + 1

            text = find_bass_trip(num=num)

            bot.send_message(call.from_user.id, text=text, disable_web_page_preview= True, reply_markup=keybords.trip_bassein_board()) 
            db_users.upd_element_in_column(table_name='users', upd_par_name='bassein_list', key_par_name=num, upd_column_name='from_user_id', key_column_name=call.from_user.id)      
        
        elif call.data == 'abon_pay':
            res = db_users.find_elements_by_keyword(table_name='users', key_name=call.from_user.id, column_name='from_user_id')
            print(res)
            res = res [0]
            num = res[9]
            text, list_buttons = pars_bass_list(num=num)
            print(list_buttons)
            bot.send_message(call.from_user.id, text=text, disable_web_page_preview= True, reply_markup=keybords.abon_bassein_board(list_bass=list_buttons)) 
        
        elif call.data == 'abon_next':
            res = db_users.find_elements_by_keyword(table_name='users', key_name=call.from_user.id, column_name='from_user_id')
            print(res)
            res = res [0]
            num = res[9]
            if num == 5:
                num = 1
            else:
                num = num + 1

            text, list_buttons = pars_bass_list(num=num)
            print(list_buttons)
            bot.send_message(call.from_user.id, text=text, disable_web_page_preview= True, reply_markup=keybords.abon_bassein_board(list_bass=list_buttons)) 
            db_users.upd_element_in_column(table_name='users', upd_par_name='bassein_list', key_par_name=num, upd_column_name='from_user_id', key_column_name=call.from_user.id)      
        
        elif 'abon' in call.data:
            bassein = call.data.split("::")[1]
            #здесь надо по номеру бассейна найти цену
            res_bass = db_bass.find_elements_in_column(table_name='bass', key_name=bassein, column_name='num')
            res_bass = res_bass[0]
            name_bassein = res_bass[1]
            price = res_bass[6]
            print(res_bass)
            bot.send_message(call.from_user.id, text=msg.abon_price_msg.format(bassein=name_bassein, price=price), disable_web_page_preview= True, reply_markup=keybords.back()) 
            db_users.upd_element_in_column(table_name='users', upd_par_name='bassein', key_par_name=bassein, upd_column_name='from_user_id', key_column_name=call.from_user.id)      
            

        elif call.data == 'events_all':
            bot.send_message(chat_id=call.from_user.id, text=msg.events_msg, reply_markup=keybords.events_board())


        elif call.data == 'sorevnovaniya':
            bot.send_message(call.from_user.id, text=msg.sorevnovaniya_msg, disable_web_page_preview= True, reply_markup=keybords.record_event_board(event='Соревнования')) 
        elif call.data == 'viezdi':
                    bot.send_message(call.from_user.id, text=msg.viezdi_msg, disable_web_page_preview= True, reply_markup=keybords.record_event_board(event='Выезды')) 
        elif call.data == 'intensivi':
                    bot.send_message(call.from_user.id, text=msg.intensivi_msg, disable_web_page_preview= True, reply_markup=keybords.record_event_board(event='Интенсивы')) 

        elif 'record' in call.data:
            print(call.data)
            record = call.data.split("::")[1]
            
            res_user = db_users.find_elements_by_keyword(table_name='users', key_name=call.from_user.id, column_name='from_user_id')
            print(res_user)
            res_user = res_user[0]
            text = f"""
Имя {res_user[2]}
Username {res_user[1]}
Тел. {res_user[3]}
Записался на {record}
"""
            bot.send_message(chat_id=ADMIN_ID, text=text)
            bot.send_message(chat_id=call.from_user.id, text=msg.event_success, reply_markup=keybords.back())
            db_users.upd_element_in_column(table_name='users', upd_par_name='events', key_par_name=record, upd_column_name='from_user_id', key_column_name=call.from_user.id)      
        elif call.data == 'back':
            bot.send_message(call.from_user.id, text=msg.back_msg, disable_web_page_preview= True, reply_markup=keybords.main_board()) 
        
        

    @bot.message_handler(content_types=['text'])
    def get_fio(message):
        print(f"message {message.text}")
        name = message.text
        db_users.upd_element_in_column(table_name='users', upd_par_name='name', key_par_name=name, upd_column_name='from_user_id', key_column_name=message.from_user.id)      
        m = bot.send_message(chat_id=message.from_user.id, text=msg.phone_msg)
        bot.register_next_step_handler(m, get_phone)

    def get_phone(message):
        print(f"message {message.text}")
        phone = message.text
        db_users.upd_element_in_column(table_name='users', upd_par_name='phone', key_par_name=phone, upd_column_name='from_user_id', key_column_name=message.from_user.id)      
        bot.send_message(chat_id=message.from_user.id, text=msg.first_visit_msg, reply_markup=keybords.first_visit_board())
        
    
    @bot.message_handler(content_types=['photo'])
    def get_discount(message):
        foto = message.photo[len(message.photo) - 1].file_id
        file_info = bot.get_file(foto)
        photo = bot.download_file(file_info.file_path)
        res_user = db_users.find_elements_by_keyword(table_name='users', key_name=message.from_user.id, column_name='from_user_id')
        res_user = res_user[0]
        print(res_user)
        text = f"""
Имя {res_user[2]}
Username {res_user[1]}
Тел. {res_user[3]}
"""
        bot.send_photo(chat_id=ADMIN_ID, photo=photo, caption=text)
        bot.send_message(chat_id=message.from_user.id, text=msg.success_discount_msg, reply_markup=keybords.back())
        
    def get_chek(message):
        foto = message.photo[len(message.photo) - 1].file_id
        file_info = bot.get_file(foto)
        photo = bot.download_file(file_info.file_path)
        res_user = db_users.find_elements_by_keyword(table_name='users', key_name=message.from_user.id, column_name='from_user_id')
        res_user = res_user[0]
        bassein = res_user[8]
        res_bass = db_bass.find_elements_in_column(table_name='bass', key_name=bassein, column_name='num')
        res_bass = res_bass[0]
        name_bassein = res_bass[1]

        price = res_bass[6]
        print(res_user)
        text = f"""
Имя {res_user[2]}
Username {res_user[1]}
Тел. {res_user[3]}
Бассейн {name_bassein}
Стоимость {price} руб.
"""
        bot.send_photo(chat_id=ADMIN_ID, photo=photo, caption=text)
        bot.send_message(chat_id=message.from_user.id, text=msg.success_abon_msg, reply_markup=keybords.back())
                
    bot.infinity_polling(skip_pending=True)

if __name__ == "__main__":
    main()

    