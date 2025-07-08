from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from bot.keyboards.reply import kb_menu

cmd_router = Router()


@cmd_router.message(Command('start'))
async def react_cmd_start(message: Message):
    await message.answer('Добрый день, я могу создать выбранный вами график', reply_markup=kb_menu)
