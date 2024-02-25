import aiogram
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from calendar import Calendar
from datetime import date, datetime
from aiogram import Bot, Dispatcher, executor, types

from buttons.buttons import calender_buttons, change_date_by_months
from config import TG_token

months = ['Январь', "Февраль", "Март", "Апрель", "Май", "Июнь",
          "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
bot = Bot(TG_token)
dp = Dispatcher(bot, storage=MemoryStorage())

message_delete = {}


class Form(StatesGroup):
    city_state = State()
    area_state = State()
    date_from_state = State()
    date_to_state = State()


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message, state: FSMContext):
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("Выбрать жильё", callback_data="quiz")
    markup.add(button1)
    await message.answer(f"Здравствуйте!", reply_markup=markup)


@dp.callback_query_handler(lambda query: query.data == 'quiz')
async def callback_giveaway(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(chat_id=callback_query.message.chat.id, text="Введите город")
    await Form.city_state.set()


@dp.message_handler(state=Form.city_state)
async def process_name(message: types.Message, state: FSMContext):
    city = message.text
    async with state.proxy() as data:
        data['city'] = city
    await message.answer("Введите район")
    await Form.area_state.set()


@dp.message_handler(state=Form.area_state)
async def process_name1(message: types.Message, state: FSMContext):
    area = message.text
    async with state.proxy() as data:
        data['area'] = area
    await state.finish()
    today = date.today()
    markup = calender_buttons(today, typefr_to="fr")
    await message.answer(f"Текущая дата: {months[today.month - 1]} {today.year} Года", reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data not in ['skip'])
async def callback(call):
    if 'ne' in call.data[:2] or 'pr' in call.data[:2]:
        today = str(call.data)[4:14]  # '2023-12-25'
        today = change_date_by_months(today, 1 if 'ne' == call.data[:2] else -1)
        markup = calender_buttons(today, typefr_to=call.data[2:4])
        await call.message.delete()
        await call.message.answer(f"Текущая дата: {months[today.month - 1]} {today.year} Года", reply_markup=markup)
    elif 'dtfr' in call.data:
        today = str(call.data)[4:]
        await call.message.delete()
        await call.message.answer(f'From {today}')
        today = date.today()
        markup = calender_buttons(today, typefr_to="to")
        await call.message.answer(f"Текущая дата: {months[today.month - 1]} {today.year} Года", reply_markup=markup)
    elif 'dtto' in call.data:
        today = str(call.data)[4:]
        await call.message.delete()
        await call.message.answer(f'To {today}')


if __name__ == '__main__':
    executor.start_polling(dp)
