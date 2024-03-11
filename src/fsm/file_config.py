from aiogram.fsm.state import StatesGroup, State


class FileConfig(StatesGroup):
    count_files = State()