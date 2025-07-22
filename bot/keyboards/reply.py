from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.support import list_type_graphic
kb_menu = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton(text='Начать')]
])

kb_type_groupby = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton(text='Сумма'), KeyboardButton(text='Среднее')],
    [KeyboardButton(text='Количество')]
])


kb_type_graphic = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton(text=tg)] for tg in list_type_graphic
])

