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


def change_settings_graphic(data: dict):
    name_parameters = list(data.items())[1:]
    list_btn = []

    for name, value in name_parameters:
        row = [
            InlineKeyboardButton(
                text=f'Изменить {name}',
                callback_data=f'change-settings:{name}'
            ),
            InlineKeyboardButton(
                text=str(data[name]),
                callback_data=f'---'
            )
        ]
        list_btn.append(row)

    list_btn.append([InlineKeyboardButton(text='🔙 Назад', callback_data='back_change_settings')])

    return InlineKeyboardMarkup(inline_keyboard=list_btn)
