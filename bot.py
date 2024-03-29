import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from src.handlers import sort_file

load_dotenv()

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()


async def main():

    dp.include_routers(sort_file.router)
    # await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())




