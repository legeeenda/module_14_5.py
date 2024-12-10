from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from crud_functions import initiate_db, get_all_products, add_user, is_included
import asyncio

API_TOKEN = '7787493433:AAGBdEiUhUvCcydfXXxFbbS_F_T_Ca5Tfbk'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Рассчитать"), KeyboardButton(text="Информация")],
        [KeyboardButton(text="Купить"), KeyboardButton(text="Регистрация")]
    ],
    resize_keyboard=True
)


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Добро пожаловать! Выберите действие:", reply_markup=keyboard)


@dp.message(lambda message: message.text == "Регистрация")
async def sing_up(message: types.Message, state: FSMContext):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await state.set_state(RegistrationState.username)


@dp.message(RegistrationState.username)
async def set_username(message: types.Message, state: FSMContext):
    username = message.text
    if is_included(username):
        await message.answer("Пользователь существует, введите другое имя:")
    else:
        await state.update_data(username=username)
        await message.answer("Введите свой email:")
        await state.set_state(RegistrationState.email)

@dp.message(RegistrationState.email)
async def set_email(message: types.Message, state: FSMContext):
    email = message.text
    await state.update_data(email=email)
    await message.answer("Введите свой возраст:")
    await state.set_state(RegistrationState.age)


@dp.message(RegistrationState.age)
async def set_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        data = await state.get_data()
        add_user(data['username'], data['email'], age)
        await message.answer(f"Пользователь {data['username']} успешно зарегистрирован!")
        await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введите корректный возраст.")


@dp.message(lambda message: message.text == "Купить")
async def get_buying_list(message: types.Message):
    products = get_all_products()
    if not products:
        await message.answer("В базе данных нет продуктов.")
        return
    for product in products:
        product_id, title, description, price, image_url = product
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=image_url,
            caption=f"Название: {title} | Описание: {description} | Цена: {price} рублей."
        )
    await message.answer("Выберите продукт для покупки:")

async def main():

    initiate_db()
    print("Bot is running...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
