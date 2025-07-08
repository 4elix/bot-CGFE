from aiogram.fsm.state import StatesGroup, State


class GetFile(StatesGroup):
    file = State()


class ChangeDF(StatesGroup):
    column1 = State()
    column2 = State()
    operation = State()


class HistoryGroupby(StatesGroup):
    result = State()


class CreateGraphic(StatesGroup):
    type_graphic = State()
    x = State()
    y = State()
    title = State()
    x_label = State()
    y_label = State()
    color = State()
