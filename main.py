import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from bot.handlers.texts import txt_router
from bot.handlers.commands import cmd_router
from bot.handlers.callback import call_router


async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_routers(
        txt_router,
        cmd_router,
        call_router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    print('work')
    try:
        asyncio.run(main())
    except Exception as error:
        print(error)
