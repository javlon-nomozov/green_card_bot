from aiogram.dispatcher.filters.state import StatesGroup, State


class NewSubChat(StatesGroup):
    id_link = State()
    description = State()

class Anketa(StatesGroup):
    phone = State()
    fname = State()
    lname = State()
    gender = State()
    birth_year = State()
    birth_month = State()
    birth_day = State()
    birth_city = State()
    birth_country = State()
    photo = State()
    living_city = State()
    living_country = State()
    edu_grade = State()
    marriage_state = State()
    child_count = State()
    session_count = State()
    ch_fname = State()
    ch_lname = State()
    ch_gender = State()
    ch_birth_year = State()
    ch_birth_month = State()
    ch_birth_day = State()
    ch_city = State()
    ch_country = State()
    ch_photo = State()
    bill = State()
