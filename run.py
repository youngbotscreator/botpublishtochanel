import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, html
from aiogram.enums import ParseMode
from app.handlers import router


async def main():
    bot = Bot(token='TOKEN', parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())