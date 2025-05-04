from aiogram.fsm.state import StatesGroup, State


class AddOrder(StatesGroup):
    customer = State()
    products = State()
    count_products = State()
