from calendar import Calendar
from datetime import date, datetime
from aiogram import types

from dateutil.relativedelta import relativedelta


def calender_buttons(today, typefr_to):
    calendar = Calendar()
    weeks = calendar.monthdays2calendar(today.year, today.month)

    markup = types.InlineKeyboardMarkup(row_width=8)
    previous = types.InlineKeyboardButton(text="<-----------", callback_data=f'prev{today}')
    next = types.InlineKeyboardButton(text="----------->", callback_data=f'next{today}')

    markup.row(previous, next)

    monday_ = types.InlineKeyboardButton(text="Пн", callback_data='skip')
    tuesday_ = types.InlineKeyboardButton(text="Вт", callback_data='skip')
    wednesday_ = types.InlineKeyboardButton(text="Ср", callback_data='skip')
    thursday_ = types.InlineKeyboardButton(text="Чт", callback_data='skip')
    friday_ = types.InlineKeyboardButton(text="Пт", callback_data='skip')
    saturday_ = types.InlineKeyboardButton(text="Сб", callback_data='skip')
    sunday_ = types.InlineKeyboardButton(text="Вс", callback_data='skip')

    markup.row(monday_, tuesday_, wednesday_,
               thursday_, friday_, saturday_, sunday_)

    for week in weeks:
        markup_row_ = list()
        for day in week:
            number = day[0]
            button = types.InlineKeyboardButton(str(number),
                                                callback_data=f'dt{typefr_to}{str(today)[:8]}{str(number) if len(str(number)) >= 2 else f"0{str(number)}"}')
            markup_row_.append(button)
        markup.row(*markup_row_)
    return markup


def change_date_by_months(date_str, months_to_add):
    date = datetime.strptime(date_str, '%Y-%m-%d')
    new_date = date + relativedelta(months=months_to_add)
    return new_date
