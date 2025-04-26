import asyncio
from aiogram import Bot, Dispatcher
from handlers.start_cmd import router
from config import TOKEN


async def main():
    """Функция запуска работы бота"""
    bot = Bot(TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    print('Бот запущен...')
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот остановлен...')
