from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.utils import ChangeDF, ChangeGraphic
from bot.keyboards.reply import kb_type_graphic
from bot.ghostwriter import text_help_work_groupby, text_enter_name_column, text_create_graphic, \
    get_column_name_for_axis, get_axis_name

call_router = Router()


@call_router.callback_query(F.data == 'y_groupby')
async def react_btn_y_groupby(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text_help_work_groupby)
    await state.set_state(ChangeDF.column1)
    data = await state.get_data()
    columns = ', '.join(data['file'].columns)
    await callback.message.answer(text_enter_name_column(columns, 1))


@call_router.callback_query(F.data == 'n_groupby')
async def react_btn_n_groupby(callback: CallbackQuery):
    await callback.message.answer(text_create_graphic, reply_markup=kb_type_graphic)


@call_router.callback_query(F.data == 'y_save')
async def react_btn_y_save(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    result = data.pop('result', None)
    data.pop('file', None)
    data['file'] = result
    await state.set_data(data)
    await callback.answer("Результат сохранён.")
    await callback.message.answer(text_create_graphic, reply_markup=kb_type_graphic)


@call_router.callback_query(F.data == 'n_save')
async def react_btn_n_save(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data.pop('result')
    data.pop('column1')
    data.pop('column2')
    await callback.message.answer(text_create_graphic, reply_markup=kb_type_graphic)


@call_router.callback_query(F.data.startswith('change-settings'))
async def react_btn_change_settings(callback: CallbackQuery, state: FSMContext):
    _, option = callback.data.split(':')
    data = await state.get_data()
    columns = ', '.join(data['file'].columns)
    if option == 'type_graphic':
        await state.set_state(ChangeGraphic.g_type_graphic)
        await callback.message.answer('Внизу указаны типы графиков', reply_markup=kb_type_graphic)
    elif option == 'x':
        await state.set_state(ChangeGraphic.g_x)
        await callback.message.answer(get_column_name_for_axis('x', columns))
    elif option == 'y':
        await state.set_state(ChangeGraphic.g_y)
        await callback.message.answer(get_column_name_for_axis('y', columns))
    elif option == 'x_label':
        await state.set_state(ChangeGraphic.g_x_label)
        await callback.message.answer(get_axis_name('x'))
    elif option == 'y_label':
        await state.set_state(ChangeGraphic.g_y_label)
        await callback.message.answer(get_axis_name('y'))
    elif option == 'title':
        await state.set_state(ChangeGraphic.g_title)
        await callback.message.answer('Введите заголовок для графика')


@call_router.callback_query(F.data.startswith('create_graphic'))
async def create_graphic(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
