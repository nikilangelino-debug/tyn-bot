import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# Вставь сюда токен, который тебе дал @BotFather
TOKEN = "8942425687:AAGaQTpFaW-kRWzOS2llrZoSFM70s7JMTHs"

# Твой личный Telegram ID (чтобы бот знал, кому присылать готовые анкеты)
# Можешь узнать свой ID у бота @userinfobot в Telegram
ADMIN_ID = 5099881393

# Настройка состояний анкеты
class Form(StatesGroup):
    name = State()
    age = State()
    occupation = State()
    motivation = State()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Старт / Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Привет! Это официальный бот Tashkent Youth Network (TYN).\n\n"
        "Давай заполним короткую анкету для вступления в комьюнити.\n"
        "Как тебя зовут? (Напиши Имя и Фамилию)"
    )
    await state.set_state(Form.name)

# Шаг 1: Имя
@dp.message(Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Form.age)

# Шаг 2: Возраст
@dp.message(Form.age)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Чем занимаешься / где учишься или работаешь?")
    await state.set_state(Form.occupation)

# Шаг 3: Деятельность
@dp.message(Form.occupation)
async def process_occupation(message: types.Message, state: FSMContext):
    await state.update_data(occupation=message.text)
    await message.answer("Почему ты хочешь присоединиться к TYN? Какая у тебя цель?")
    await state.set_state(Form.motivation)

# Шаг 4: Мотивация и завершение
@dp.message(Form.motivation)
async def process_motivation(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data.get("name")
    age = data.get("age")
    occupation = data.get("occupation")
    motivation = message.text
    
    username = message.from_user.username
    user_link = f"@{username}" if username else f"ID: {message.from_user.id}"

    # Текст заявки для тебя (Администратора)
    admin_text = (
        f"🚨 Новая заявка в TYN!\n\n"
        f"👤 Имя: {name}\n"
        f"📅 Возраст: {age}\n"
        f"💼 Деятельность: {occupation}\n"
        f"🎯 Цель/Мотивация: {motivation}\n"
        f"🔗 Контакт: {user_link}"
    )

    # Отправляем готовую заявку тебе в ЛС
    try:
        await bot.send_message(ADMIN_ID, admin_text, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Не удалось отправить заявку админу: {e}")

    # Сообщение кандидату
    await message.answer(
        "Спасибо! Твоя анкета успешно отправлена организатору.\n"
        "Мы изучим её и свяжемся с тобой в ближайшее время! 🚀"
    )
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
