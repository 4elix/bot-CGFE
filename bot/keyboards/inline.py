from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


kb_option_groupby = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Да', callback_data='y_groupby'),
        InlineKeyboardButton(text='Нет', callback_data='n_groupby')
    ]
])

kb_option_save_groupby = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Да', callback_data='y_save'),
        InlineKeyboardButton(text='Нет', callback_data='n_save')
    ]
])
