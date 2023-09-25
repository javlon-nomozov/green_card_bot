from aiogram.dispatcher.filters.state import StatesGroup, State


class NewSubChat(StatesGroup):
    id_link = State()
    description = State()
