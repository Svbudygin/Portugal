from utils import *


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("🏠 Выбрать жильё 🏠", callback_data="quiz")
    markup.add(button1)
    await message.answer(f"Здравствуйте!👋\nДобро пожаловать в бота по поиску квартир и апартоментов в Португалии 🇵🇹",
                         reply_markup=markup)


@dp.callback_query_handler(lambda query: query.data == 'quiz')
async def callback_giveaway(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    message = await bot.send_message(chat_id=callback_query.message.chat.id, text="🌇 Введите город 🌇")
    await add_del_message(message)
    await Form.city_state.set()


@dp.message_handler(state=Form.city_state)
async def city(message: types.Message, state: FSMContext):
    await add_del_message(message)
    city = message.text
    async with state.proxy() as data:
        data['city'] = city
    message = await message.answer("🏘 Введите район 🏘")
    await add_del_message(message)
    await Form.area_state.set()


@dp.message_handler(state=Form.area_state)
async def area(message: types.Message, state: FSMContext):
    await add_del_message(message)
    area = message.text
    async with state.proxy() as data:
        data['area'] = area
    message = await message.answer(f"💶 Напишите минимальную цену в € в месяц 💶")
    await add_del_message(message)
    await Form.price_min_state.set()


@dp.message_handler(state=Form.price_min_state)
async def min_price(message: types.Message, state: FSMContext):
    await add_del_message(message)
    try:
        price = int(message.text)
    except ValueError:
        price = '-'
    async with state.proxy() as data:
        data['min_price'] = price
    message = await message.answer(f"💶 Напишите максимальную цену в € в месяц 💶")
    await add_del_message(message)
    await Form.price_max_state.set()


@dp.message_handler(state=Form.price_max_state)
async def max_price(message: types.Message, state: FSMContext):
    await add_del_message(message)
    async with state.proxy() as data:
        try:
            price = int(message.text)
        except ValueError:
            price = '-'
        price = price if price != '-' and data['min_price'] != '-' and price > data['min_price'] else '-'
        data['max_price'] = price
    today = date.today()
    markup = calender_buttons(today, typefr_to="fr")
    message = await message.answer(
        f"🕒 Выберите дату заезда 🕒\nТекущая дата: {months[today.month - 1]} {today.year} Года",
        reply_markup=markup)
    await add_del_message(message)
    await Form.from_date_state.set()


@dp.callback_query_handler(
    lambda c: c.data.startswith('pr') or c.data.startswith('ne') or c.data.startswith('dtfr'),
    state=Form.from_date_state)
async def callback_calendar_from(call, state: FSMContext):
    if call.data.startswith('ne') or call.data.startswith('pr'):
        today = str(call.data)[4:14]  # '2023-12-25'
        today = change_date_by_months(today, 1 if call.data.startswith('ne') else -1)
        markup = calender_buttons(today, typefr_to='fr')
        await call.message.delete()
        await call.message.answer(
            f"🕒 Выберита дату заезда 🕒\nТекущая дата: {months[today.month - 1]} {today.year} Года",
            reply_markup=markup)
        await Form.from_date_state.set()
    elif call.data.startswith('dtfr'):
        today = str(call.data)[4:]
        await call.message.delete()
        from_date = call.data[4:]
        async with state.proxy() as data:
            data['from_date'] = from_date
        message = await call.message.answer(f'From {today}')
        await add_del_message(message)
        today = date.today()
        markup = calender_buttons(today, typefr_to="to")
        await call.message.answer(
            f"⏱️ Выберита дату выезда ⏱️\nТекущая дата: {months[today.month - 1]} {today.year} Года",
            reply_markup=markup)
        await Form.to_date_state.set()


@dp.callback_query_handler(lambda c: c.data.startswith('pr') or c.data.startswith('ne') or c.data.startswith('dtto'),
                           state=Form.to_date_state)
async def callback_calendar_to(call, state: FSMContext):
    if call.data.startswith('ne') or call.data.startswith('pr'):
        today = str(call.data)[4:14]  # '2023-12-25'
        today = change_date_by_months(today, 1 if call.data.startswith('ne') else -1)
        markup = calender_buttons(today, typefr_to='to')
        await call.message.delete()
        await call.message.answer(
            f"🕒 Выберита дату заезда 🕒\nТекущая дата: {months[today.month - 1]} {today.year} Года",
            reply_markup=markup)
        await Form.to_date_state.set()
    elif call.data.startswith('dtto'):
        today = str(call.data)[4:]
        await call.message.delete()
        message = await call.message.answer(f'To {today}')
        await add_del_message(message)
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
        print(from_date, to_date, city, area, min_price, max_price)
        # pars(from_date, to_date, city, area, min_price, max_price)
        await del_messages(call.message.chat.id)
        await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp)
