from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_menu = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton(text='Начать')]
])

kb_type_groupby = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton(text='Сумма'), KeyboardButton(text='Среднее')],
    [KeyboardButton(text='Количество')]
])

type_graphic = [
    'Гистограмма',
    'Коробчатая диаграмма',
    'Столбчатая диаграмма',
    'Линейный график',
    'Диаграмма рассеяния (точечная диаграмма)',
]

kb_type_graphic = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton(text=tg)] for tg in type_graphic
])

