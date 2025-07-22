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


class ChangeGraphic(StatesGroup):
    g_type_graphic = State()
    g_x = State()
    g_y = State()
    g_title = State()
    g_x_label = State()
    g_y_label = State()
    g_color = State()
