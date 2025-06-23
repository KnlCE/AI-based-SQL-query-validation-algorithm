from aiogram.filters.command import Command
from aiogram import Router, types, F, Bot
from aiogram.types import ReplyKeyboardRemove
from keyboards.subscribe_btn import subscribe_btn
from config import TOKEN, BOT_ID
from ai.generate_explanation import explain_sql_error

router = Router()
bot = Bot(TOKEN)


@router.message(Command('start'))
async def start_cmd(message: types.Message):
    result = await bot.get_chat_member(chat_id=BOT_ID, user_id=message.from_user.id)
    if message.chat.type == 'private':
        if result.status != 'left':
            await message.answer('🔎Проверка SQL запроса на правильность с помощью ИИ📝\n\nОтправьте свой SQL запрос:',
                                 reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer(f'Для бесплатного использования бота подпишитесь на наш канал с интересными новостями из мира IT: {BOT_ID}', reply_markup=subscribe_btn)


@router.message(F.text == 'Я подписан')
async def cmd_subscribe(message: types.Message):
    result = await bot.get_chat_member(chat_id=BOT_ID, user_id=message.from_user.id)
    if message.chat.type == 'private':
        if result.status != 'left':
            await message.answer('Вы подписаны на канал! Теперь вы можете проверить свой SQL запрос:', reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer(f'Вы все еще не подписались на наш канал(\n{BOT_ID}', reply_markup=subscribe_btn)


@router.message()
async def handle_sql_query(message: types.Message):
    result = await bot.get_chat_member(chat_id=BOT_ID, user_id=message.from_user.id)
    if message.chat.type == 'private':
        if result.status != 'left':
            try:
                explanation = explain_sql_error(message.text)
                await message.answer(f"Анализ вашего SQL-запроса:\n\n{explanation}")
            except Exception as e:
                await message.answer("Произошла ошибка при анализе запроса. Пожалуйста, попробуйте еще раз.")
        else:
            await message.answer(f'Для использования бота подпишитесь на наш канал: {BOT_ID}', reply_markup=subscribe_btn)


