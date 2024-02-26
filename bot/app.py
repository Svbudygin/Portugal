from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import date
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import MessageToDeleteNotFound

from buttons import calender_buttons, change_date_by_months
from config import TG_token
from main import pars

months = ['Январь', "Февраль", "Март", "Апрель", "Май", "Июнь",
          "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
bot = Bot(TG_token)
dp = Dispatcher(bot, storage=MemoryStorage())


class Form(StatesGroup):
    city_state = State()
    area_state = State()
    price_state = State()
    from_date_state = State()
    to_date_state = State()


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("🏠 Выбрать жильё 🏠", callback_data="quiz")
    markup.add(button1)
    await message.answer(f"Здравствуйте!👋\nДобро пожаловать в бота по поиску квартир и апартоментов в Португалии 🇵🇹",
                         reply_markup=markup)


@dp.callback_query_handler(lambda query: query.data == 'quiz')
async def callback_giveaway(callback_query: types.CallbackQuery):
    await bot.send_message(chat_id=callback_query.message.chat.id, text="🧭 Введите город 🧭")
    await Form.city_state.set()


@dp.message_handler(state=Form.city_state)
async def process_name(message: types.Message, state: FSMContext):
    city = message.text
    async with state.proxy() as data:
        data['city'] = city
    await message.answer("🏘 Введите район 🏘")
    await Form.area_state.set()


@dp.message_handler(state=Form.area_state)
async def process_name1(message: types.Message, state: FSMContext):
    area = message.text
    async with state.proxy() as data:
        data['area'] = area
    # await state.finish()
    await message.answer(f"💶 Напишите диапозон цен в € в формате \"min-max\" 💶")
    await Form.price_state.set()


@dp.message_handler(state=Form.price_state)
async def process_name1(message: types.Message, state: FSMContext):
    price = message.text
    if '-' in price and price.count('-') == 1:
        price = price.split('-')
        try:
            min_price = int(price[0])
            max_price = int(price[1])
            if max_price >= min_price:
                async with state.proxy() as data:
                    data['min_price'] = min_price
                    data['max_price'] = max_price
                today = date.today()
                markup = calender_buttons(today, typefr_to="fr")
                await message.answer(f"🕒 Выберите дату заезда 🕒\nТекущая дата: {months[today.month - 1]} {today.year} Года",
                                     reply_markup=markup)
                await Form.from_date_state.set()
            else:
                await message.answer(f"Ваш диапозон не верен. Диапозон цен в € в формате \"min-max\"")
        except ValueError:
            await message.answer(f"Введите числа! Диапозон цен в € в формате \"min-max\"")
    else:
        await message.answer(f"Введите в правильном формате! Диапозон цен в € в формате \"min-max\"")
    # await state.finish()


@dp.callback_query_handler(
    lambda c: c.data.startswith('pr') or c.data.startswith('ne') or c.data.startswith('dtfr'),
    state=Form.from_date_state)
async def callback(call, state: FSMContext):
    if call.data.startswith('ne') or call.data.startswith('pr'):
        today = str(call.data)[4:14]  # '2023-12-25'
        today = change_date_by_months(today, 1 if call.data.startswith('ne') else -1)
        markup = calender_buttons(today, typefr_to='fr')
        await call.message.delete()
        await call.message.answer(f"🕒 Выберита дату заезда 🕒\nТекущая дата: {months[today.month - 1]} {today.year} Года",
                                  reply_markup=markup)
        await Form.from_date_state.set()
    elif call.data.startswith('dtfr'):
        today = str(call.data)[4:]
        await call.message.delete()
        from_date = call.data[4:]
        async with state.proxy() as data:
            data['from_date'] = from_date
        await call.message.answer(f'From {today}')
        today = date.today()
        markup = calender_buttons(today, typefr_to="to")
        await call.message.answer(f"🕒 Выберита дату выезда 🕒\nТекущая дата: {months[today.month - 1]} {today.year} Года",
                                  reply_markup=markup)
        await Form.to_date_state.set()


@dp.callback_query_handler(lambda c: c.data.startswith('pr') or c.data.startswith('ne') or c.data.startswith('dtto'),
                           state=Form.to_date_state)
async def callback(call, state: FSMContext):
    if call.data.startswith('ne') or call.data.startswith('pr'):
        today = str(call.data)[4:14]  # '2023-12-25'
        today = change_date_by_months(today, 1 if call.data.startswith('ne') else -1)
        markup = calender_buttons(today, typefr_to='to')
        await call.message.delete()
        await call.message.answer(f"🕒 Выберита дату заезда 🕒\nТекущая дата: {months[today.month - 1]} {today.year} Года",
                                  reply_markup=markup)
        # await Form.to_date_state.set()
    elif call.data.startswith('dtto'):
        today = str(call.data)[4:]
        await call.message.delete()
        await call.message.answer(f'To {today}')
        await call.message.answer(f'⏳ Подождите пару минут, скоро отправим вам новые объявления ... ⏳')
        to_date = call.data[4:]
        async with state.proxy() as data:
            data['to_date'] = to_date
        async with state.proxy() as data:
            from_date = data['from_date']
            to_date = data['to_date']
            city = data['city']
            area = data['area']
            min_price = data['min_price']
            max_price = data['max_price']

        pars(from_date, to_date, city, area, min_price, max_price)
        await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp)
