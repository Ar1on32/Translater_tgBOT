import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, Message, CallbackQuery
from aiogram.filters import Command
from deep_translator import GoogleTranslator
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Замените на ваш токен бота, полученный от BotFather
TOKEN = 'Сюда ВАШ токен'  # Обязательно замените на ваш токен

# Создание экземпляра бота
bot = Bot(token=TOKEN)

# Создание экземпляра диспетчера
dp = Dispatcher()

# Начальное состояние перевода
current_language = 'ru-en'  # Направление перевода: 'ru-en' (Русский → Английский) или 'en-ru' (Английский → Русский)

# Функция для создания инлайн-клавиатуры
def get_inline_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Русский → Английский", callback_data='ru_en')],
        [InlineKeyboardButton(text="Английский → Русский", callback_data='en_ru')]
    ])
    return keyboard

# Функция для создания обычной клавиатуры
def get_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="Меню")]
    ])
    return keyboard

async def start(message: Message):
    await message.reply("Привет! Я бот-переводчик. Нажмите 'Меню' для выбора направления перевода.", reply_markup=get_keyboard())

async def show_menu(message: Message):
    await message.reply("Выберите направление перевода:", reply_markup=get_inline_keyboard())

async def set_language(callback: CallbackQuery):
    global current_language
    if callback.data == 'ru_en':
        current_language = 'ru-en'
        await callback.answer("Режим переключен: Русский → Английский")
    elif callback.data == 'en_ru':
        current_language = 'en-ru'
        await callback.answer("Режим переключен: Английский → Русский")

async def translate(message: Message):
    global current_language
    if message.text:
        try:
            text = message.text
            if text == 'Меню':
                await show_menu(message)
                return
            if current_language == 'ru-en':
                translator = GoogleTranslator(source='auto', target='en')
                translation = translator.translate(text)
            else:
                translator = GoogleTranslator(source='auto', target='ru')
                translation = translator.translate(text)

            await message.reply(f"Перевод: {translation}")
        except Exception as e:
            logger.error(f"Ошибка перевода: {e}")  # Логируем ошибку
            await message.reply("Произошла ошибка при переводе. Пожалуйста, попробуйте позже.")

# Регистрация обработчиков сообщений и колбеков
dp.message.register(start, Command('start'))
dp.message.register(translate)
dp.callback_query.register(set_language)

async def main():
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка запуска бота: {e}")  # Логируем ошибку при запуске

if __name__ == '__main__':
    asyncio.run(main())
