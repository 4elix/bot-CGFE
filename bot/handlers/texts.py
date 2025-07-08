import pandas as pd
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from tabulate import tabulate

from bot.support import manager_groupby
from bot.keyboards.reply import kb_type_graphic, kb_type_groupby, type_graphic
from bot.keyboards.inline import kb_option_groupby, kb_option_save_groupby
from bot.utils import GetFile, ChangeDF, HistoryGroupby, CreateGraphic

txt_router = Router()


@txt_router.message(F.text == 'Начать')
async def react_btn_startwork(message: Message, state: FSMContext):
    text = 'Для работы мне нужен файл формата excel, можете отправить.'
    text += '\n\nТак же на обработку файла может занять несколько минут'
    await state.set_state(GetFile.file)
    await message.answer(text, reply_markup=ReplyKeyboardRemove())


@txt_router.message(F.document, GetFile.file)
async def get_file_excel(message: Message, state: FSMContext):
    document = message.document
    if not document.file_name.endswith(('.xlsx', '.xls')):
        await message.answer("Пожалуйста, отправьте Excel-файл (.xlsx или .xls).")
        return

    file_id = document.file_id
    file = await message.bot.get_file(file_id)
    file_path = file.file_path
    file_data = await message.bot.download_file(file_path)

    df = pd.read_excel(file_data)
    await state.update_data(file=df)
    text = 'Требуется ли сгруппировать данные в полученном файле?'
    await message.answer(text, reply_markup=kb_option_groupby)


@txt_router.message(ChangeDF.column1)
async def get_name_column1(message: Message, state: FSMContext):
    await state.update_data(column1=message.text)
    await state.set_state(ChangeDF.column2)

    data = await state.get_data()
    columns = ', '.join(data['file'].columns)
    await message.answer(f'Введите название второй колонки, список колонок:\n\n{columns}')


@txt_router.message(ChangeDF.column2)
async def get_name_column2(message: Message, state: FSMContext):
    await state.update_data(column2=message.text)
    await state.set_state(ChangeDF.operation)
    await message.answer('Выберите операцию', reply_markup=kb_type_groupby)


@txt_router.message(ChangeDF.operation)
async def react_btn_sub_settings(message: Message, state: FSMContext):
    data = await state.get_data()
    if data.get('file') is None:
        await message.answer('Произошла ошибка, нажмите или напишите /start')
        return

    df, col1, col2 = data.values()
    result = await manager_groupby(df, col1, col2, message.text)
    if result is None:
        columns = ', '.join(df.columns)
        text = f'Вы указали несуществующие поля.\nПожалуйста, введите повторно c первого поля:\n\n{columns}'
        await message.answer(text)
        await state.set_state(ChangeDF.column1)
        return
    else:
        await state.set_state(HistoryGroupby.result)
        await state.update_data(result=result)
        text = tabulate(result, headers='keys', tablefmt='github', showindex=False)
        await message.answer(f'Вот такой результат:\n <pre>{text}</pre>', parse_mode="HTML")
        text = 'Нажав "Да", вы удалите отправленный Excel-файл и сохраните группировку.'
        text += '\n\nНажав "Нет", файл останется, но группировка не будет сохранена.'
        await message.answer(text, reply_markup=kb_option_save_groupby)


@txt_router.message(F.text.in_(type_graphic))
async def react_btn_type_graphic(message: Message, state: FSMContext):
    data = await state.get_data()
    if data.get('file') is None:
        await message.answer('Произошла ошибка, нажмите или напишите /start')
        return

    data = await state.get_data()
    columns = ', '.join(data['file'].columns)
    await state.update_data(type_graphic=message.text)
    await state.set_state(CreateGraphic.x)
    text = f'Пожалуйста, введите имя столбца, который будет отображён по оси X, список колонок:\n\n{columns}'
    await message.answer(text)


@txt_router.message(CreateGraphic.x)
async def get_axis_x(message: Message, state: FSMContext):
    await state.update_data(x=message.text)
    data = await state.get_data()
    if data['type_graphic'] == 'Гистограмма':
        await state.set_state(CreateGraphic.x_label)
        text = 'Введите подпись для оси x'
        await message.answer(text)
        return

    await state.set_state(CreateGraphic.y)
    columns = ', '.join(data['file'].columns)
    text = f'Пожалуйста, введите имя столбца, который будет отображён по оси У, список колонок:\n\n{columns}'
    await message.answer(text)


@txt_router.message(CreateGraphic.y)
async def get_axis_y(message: Message, state: FSMContext):
    await state.update_data(y=message.text)
    await state.set_state(CreateGraphic.x_label)
    data = await state.get_data()
    text = 'Введите подпись для оси x'
    await message.answer(text)


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
    text = 'Введите подпись для оси y'
    await message.answer(text)


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
    text = 'Выберете цвет для графика.\n1) Красный\n2) Синей'
    await message.answer(text)


@txt_router.message(CreateGraphic.color)
async def get_color(message: Message, state: FSMContext):
    index_color = int(message.text)
    color = ['red', 'blue'][index_color-1]
    await state.update_data(color=color)
    data = await state.get_data()
    text = f'''
Заголовок: {data.get('title', 'Не указанно')}.
Тип графика: {data.get('type_graphic', 'Не указанно')}.
Оси-x: {data.get('x', 'Не указанно')}.
Оси-y: {data.get('y', 'Не указанно')}.
Подпись для оси-x: {data.get('x_label', 'Не указанно')}.
Подпись для оси-y: {data.get('y_label', 'Не указанно')}.
Цвета графика: {data.get('color', 'Не указанно')}.
'''
    await message.answer(text)