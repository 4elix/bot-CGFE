import pandas as pd
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from tabulate import tabulate

from bot.support import manager_groupby
from bot.keyboards.reply import kb_type_graphic, kb_type_groupby, list_type_graphic
from bot.keyboards.inline import kb_option_groupby, kb_option_save_groupby, change_settings_graphic
from bot.utils import GetFile, ChangeDF, HistoryGroupby, CreateGraphic, ChangeGraphic

from bot.ghostwriter import text_start, text_send_xlsx, text_need_group_by, text_enter_name_column, text_error, \
    text_error_enter_column_name, text_save_result_groupby, get_column_name_for_axis, get_axis_name, text_color_options, \
    show_settings_graphic

txt_router = Router()


@txt_router.message(F.text == 'Начать')
async def react_btn_startwork(message: Message, state: FSMContext):
    await state.set_state(GetFile.file)
    await message.answer(text_start, reply_markup=ReplyKeyboardRemove())


@txt_router.message(F.document, GetFile.file)
async def get_file_excel(message: Message, state: FSMContext):
    document = message.document
    if not document.file_name.endswith(('.xlsx', '.xls')):
        await message.answer(text_send_xlsx)
        return

    file_id = document.file_id
    file = await message.bot.get_file(file_id)
    file_path = file.file_path
    file_data = await message.bot.download_file(file_path)

    df = pd.read_excel(file_data)
    await state.update_data(file=df)
    await message.answer(text_need_group_by, reply_markup=kb_option_groupby)


@txt_router.message(ChangeDF.column1)
async def get_name_column1(message: Message, state: FSMContext):
    await state.update_data(column1=message.text)
    await state.set_state(ChangeDF.column2)

    data = await state.get_data()
    columns = ', '.join(data['file'].columns)
    await message.answer(text_enter_name_column(columns, 1))


@txt_router.message(ChangeDF.column2)
async def get_name_column2(message: Message, state: FSMContext):
    await state.update_data(column2=message.text)
    await state.set_state(ChangeDF.operation)
    await message.answer('Выберите операцию', reply_markup=kb_type_groupby)


@txt_router.message(ChangeDF.operation)
async def react_btn_sub_settings(message: Message, state: FSMContext):
    data = await state.get_data()
    if data.get('file') is None:
        await message.answer(text_error)
        return

    df, col1, col2 = data.values()
    result = await manager_groupby(df, col1, col2, message.text)
    if result is None:
        columns = ', '.join(df.columns)
        await message.answer(text_error_enter_column_name(columns))
        await state.set_state(ChangeDF.column1)
        return
    else:
        await state.set_state(HistoryGroupby.result)
        await state.update_data(result=result)
        text = tabulate(result, headers='keys', tablefmt='github', showindex=False)
        await message.answer(f'Вот такой результат:\n <pre>{text}</pre>', parse_mode="HTML")
        await message.answer(text_save_result_groupby, reply_markup=kb_option_save_groupby)


@txt_router.message(F.text.in_(list_type_graphic))
async def react_btn_type_graphic(message: Message, state: FSMContext):
    data = await state.get_data()
    if data.get('file') is None:
        await message.answer(text_error)
        return

    data = await state.get_data()
    columns = ', '.join(data['file'].columns)
    await state.update_data(type_graphic=message.text)
    await state.set_state(CreateGraphic.x)
    await message.answer(get_column_name_for_axis('x', columns))


@txt_router.message(CreateGraphic.x)
async def get_axis_x(message: Message, state: FSMContext):
    await state.update_data(x=message.text)
    data = await state.get_data()
    if data['type_graphic'] == 'Гистограмма':
        await state.set_state(CreateGraphic.x_label)
        await message.answer(get_axis_name('x'))
        return

    await state.set_state(CreateGraphic.y)
    columns = ', '.join(data['file'].columns)
    await message.answer(get_column_name_for_axis('', columns))


@txt_router.message(CreateGraphic.y)
async def get_axis_y(message: Message, state: FSMContext):
    await state.update_data(y=message.text)
    await state.set_state(CreateGraphic.x_label)
    await message.answer(get_axis_name('x'))


@txt_router.message(CreateGraphic.x_label)
async def get_label_x(message: Message, state: FSMContext):
    await state.update_data(x_label=message.text)
    data = await state.get_data()
    if data['type_graphic'] == 'Гистограмма':
        await state.set_state(CreateGraphic.title)
        text = 'Введите заголовок для графика'
        await message.answer(text)
        return

    await state.set_state(CreateGraphic.y_label)
    await message.answer(get_axis_name(''))


@txt_router.message(CreateGraphic.y_label)
async def get_label_y(message: Message, state: FSMContext):
    await state.update_data(y_label=message.text)
    await state.set_state(CreateGraphic.title)
    text = 'Введите заголовок для графика'
    await message.answer(text)


@txt_router.message(CreateGraphic.title)
async def get_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(CreateGraphic.color)
    await message.answer(text_color_options)


@txt_router.message(CreateGraphic.color)
async def get_color(message: Message, state: FSMContext):
    index_color = int(message.text)
    color = ['red', 'blue'][index_color - 1]
    await state.update_data(color=color)
    data = await state.get_data()
    await message.answer(show_settings_graphic(data), reply_markup=change_settings_graphic(data))


@txt_router.message(ChangeGraphic.g_type_graphic)
async def react_g_type_graphic(message: Message, state: FSMContext):
    await state.update_data(type_graphic=message.text)
    data = await state.get_data()
    await message.answer(show_settings_graphic(data), reply_markup=change_settings_graphic(data))


@txt_router.message(ChangeGraphic.g_x)
async def react_g_x(message: Message, state: FSMContext):
    await state.update_data(x=message.text)
    data = await state.get_data()
    await message.answer(show_settings_graphic(data), reply_markup=change_settings_graphic(data))


@txt_router.message(ChangeGraphic.g_y)
async def react_g_y(message: Message, state: FSMContext):
    await state.update_data(y=message.text)
    data = await state.get_data()
    await message.answer(show_settings_graphic(data), reply_markup=change_settings_graphic(data))


@txt_router.message(ChangeGraphic.g_title)
async def react_g_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    data = await state.get_data()
    await message.answer(show_settings_graphic(data), reply_markup=change_settings_graphic(data))


@txt_router.message(ChangeGraphic.g_x_label)
async def react_g_x_label(message: Message, state: FSMContext):
    await state.update_data(x_label=message.text)
    data = await state.get_data()
    await message.answer(show_settings_graphic(data), reply_markup=change_settings_graphic(data))


@txt_router.message(ChangeGraphic.g_y_label)
async def react_g_y_label(message: Message, state: FSMContext):
    await state.update_data(y_label=message.text)
    data = await state.get_data()
    await message.answer(show_settings_graphic(data), reply_markup=change_settings_graphic(data))


@txt_router.message(ChangeGraphic.g_color)
async def react_g_color(message: Message, state: FSMContext):
    await state.update_data(color=message.text)
    data = await state.get_data()
    await message.answer(show_settings_graphic(data), reply_markup=change_settings_graphic(data))
