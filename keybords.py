from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
def menu_start():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Погнали дальше?", callback_data="next"),
    )

    return markup

def main_board():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Оплата абонемента", callback_data="abon_pay"),
        InlineKeyboardButton("Как добраться в бассейн", callback_data="trip"),
        InlineKeyboardButton("Участие в мероприятиях", callback_data="events_all"),        
        InlineKeyboardButton("Получить скидку", callback_data="discount"),           
    )

    return markup

def first_visit_board():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Да", callback_data="first"),
        InlineKeyboardButton("Нет", callback_data="no_first"),
    )

    return markup


def age_board():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("от 3 до 6", callback_data="age::от 3 до 6"),
        InlineKeyboardButton("от 6 до 18", callback_data="age::от 6 до 18"),
        InlineKeyboardButton("от 18", callback_data="age::от 18"),        
    )

    return markup

def lvl_board():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Новичок", callback_data="lvl::Новичок"),
        InlineKeyboardButton("Средний", callback_data="lvl::Средний"),
        InlineKeyboardButton("Мастер", callback_data="lvl::Мастер"),        
    )

    return markup


def choice_bassein_board(list_bass):
    markup = InlineKeyboardMarkup()


    list_butt = []
    for butt in list_bass:
        list_butt.append(InlineKeyboardButton(butt, callback_data=f"bass::{butt}"))
    markup.add(*list_butt)
    markup.add(InlineKeyboardButton('еще ▶️', callback_data=f"bas_next"))
 
    return markup

def abon_bassein_board(list_bass):
    markup = InlineKeyboardMarkup()


    list_butt = []
    for butt in list_bass:
        list_butt.append(InlineKeyboardButton(butt, callback_data=f"abon::{butt}"))
    markup.add(*list_butt)
    markup.add(InlineKeyboardButton('еще ▶️', callback_data=f"abon_next"))
 
    return markup

def trip_bassein_board():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('еще ▶️', callback_data=f"trip_next::"))
    markup.add(InlineKeyboardButton('Назад', callback_data=f"back"))
    return markup

def events_board():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Cоревнования", callback_data="sorevnovaniya"),
        InlineKeyboardButton("Выезды", callback_data="viezdi"),
        InlineKeyboardButton("Интенсивы", callback_data="intensivi"),        
         
    )

    return markup

def record_event_board(event):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Записаться", callback_data=f"record::{event}"),
        InlineKeyboardButton('Назад', callback_data=f"back"),    
     
    )
    return markup





def back():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Назад', callback_data=f"back"))
 
    return markup