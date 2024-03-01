import json

import requests
from aiogram.utils.exceptions import MessageToDeleteNotFound
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TG_token
from aiogram import Bot, Dispatcher, executor, types
import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import date
from bot.buttons.buttons import calender_buttons, change_date_by_months

bot = Bot(TG_token)
dp = Dispatcher(bot, storage=MemoryStorage())

message_delete = {}
months = ['Январь', "Февраль", "Март", "Апрель", "Май", "Июнь",
          "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

async def add_del_message(message):
    message_delete[message.chat.id] = message_delete.get(message.chat.id, set()) | {message.message_id}


async def del_messages(id):
    for mes in message_delete.get(id, set()):
        try:
            await bot.delete_message(id, mes)
        except MessageToDeleteNotFound:
            pass
    message_delete.pop(id, None)


class Form(StatesGroup):
    city_state = State()
    area_state = State()
    type_state = State()
    price_min_state = State()
    price_max_state = State()
    from_date_state = State()
    to_date_state = State()

def get_link(city, area, topologia:list, price_from, price_to):
    price = f'search%5Bfilter_float_price%3Afrom%5D={price_from}&search%5Bfilter_float_price%3Ato%5D={price_to}'
    f'search%5Bfilter_float_price%3Ato%5D={price_to}'
    f'search%5Bfilter_float_price%3Afrom%5D={price_from}'
    topologia = '&search%5Bfilter_enum_rooms_num%5D%5B2%5D='.join(topologia)[1:]
    'search%5Border%5D=created_at_first%3Adesc' # сортировка по дате анонса
    # url = f'https://www.imovirtual.com/ajax/geo6/autosuggest/?data={city}%20{area}&lowPriorityStreetsSearch=true&levels%5B0%5D=REGION&levels%5B1%5D=SUBREGION&levels%5B2%5D=CITY&levels%5B3%5D=DISTRICT&levels%5B4%5'
    url = 'https://www.imovirtual.com/ajax/geo6/autosuggest/?data=lisabon%20mafra&lowPriorityStreetsSearch=true&levels%5B0%5D=REGION&levels%5B1%5D=SUBREGION&levels%5B2%5D=CITY&levels%5B3%5D=DISTRICT&levels%5B4%5'
    'https://www.imovirtual.com/comprar/apartamento/anadia/?search%5Bregion_id%5D=1&search%5Bsubregion_id%5D=3'
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        data = response.json()
        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    print(topologia)

get_link('lisabon', 'c',['1','2','3'],4,45)