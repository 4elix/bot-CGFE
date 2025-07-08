from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.utils import ChangeDF
from bot.keyboards.reply import kb_type_graphic


call_router = Router()


@call_router.callback_query(F.data == 'y_groupby')
async def react_btn_y_groupby(callback: CallbackQuery, state: FSMContext):
    text = '''
    Как работает группировка:
    
1) Нужно ввести название первый колонки, это колонка, по значениям которой будут 
сформированы группы (например, "Регион", "Категория", "Дата").

2) Нужно ввести название второй колонки, это колонка, значения которой будут 
агрегироваться внутри каждой группы (например, "Продажи", "Количество", "Цена").

3) Нужно выбрать операцию агрегации, которая будет обрабатывать значения:
Сумма: для подсчёта общей суммы значений в каждой группе;
Среднее: для расчёта среднего значения;
Количество: для подсчёта числа записей в группе.
'''
    await callback.message.answer(text)
    await state.set_state(ChangeDF.column1)
    data = await state.get_data()
    columns = ', '.join(data['file'].columns)
    await callback.message.answer(f'Введите название первый колонки, список колонок:\n\n{columns}')


@call_router.callback_query(F.data == 'n_groupby')
async def react_btn_n_groupby(callback: CallbackQuery):
    text = 'Для создания графика выберите его тип. Ниже представлены кнопки с доступными вариантами'
    await callback.message.answer(text, reply_markup=kb_type_graphic)


@call_router.callback_query(F.data == 'y_save')
async def react_btn_y_save(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    result = data.pop('result', None)
    data.pop('file', None)
    data['file'] = result
    await state.set_data(data)
    await callback.answer("Результат сохранён.")
    text = 'Для создания графика выберите его тип. Ниже представлены кнопки с доступными вариантами'
    await callback.message.answer(text, reply_markup=kb_type_graphic)


@call_router.callback_query(F.data == 'n_save')
async def react_btn_n_save(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data.pop('result')
    data.pop('column1')
    data.pop('column2')
    text = 'Для создания графика выберите его тип. Ниже представлены кнопки с доступными вариантами'
    await callback.message.answer(text, reply_markup=kb_type_graphic)


