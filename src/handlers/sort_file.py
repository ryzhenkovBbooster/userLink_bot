import os
from pathlib import Path
from dotenv import load_dotenv
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from src.fsm.file_config import FileConfig
from src.service.crud_file import create_dir_if_not_exists, open_file, divide_array, write_files
load_dotenv()
router = Router()


@router.message(F.document)
async def sort_file(message: Message, state: FSMContext):
    if int(os.getenv('USER')) == message.from_user.id:

        document_id = message.document.file_id
        file = await message.bot.get_file(document_id)
        script_path = Path(__file__).resolve()
        file_path = file.file_path

        lib_path = os.path.join(script_path.parent.parent.parent, 'lib_files', message.document.file_name.split('.')[0])
        dir_path = create_dir_if_not_exists(lib_path)
        dir_path = f'{dir_path}/{message.document.file_name}'


        await message.bot.download_file(file_path, dir_path )

        await state.update_data(path=dir_path)
        await state.set_state(FileConfig.count_files)
        await message.answer('Введите кол-во файлов, которое хотите получить')



@router.message(FileConfig.count_files)
async def count_files(message: Message, state: FSMContext):
    data = await state.get_data()
    dir_path = data['path']
    files = write_files(dir_path=dir_path, chunks=message.text)
    await message.answer(f'Всего ссылок {files[1]}\n'
                         f'Удалено ссылок {files[1] - files[2]}\n'
                         f'Уникальных ссылок {files[2]}')
    for i in files[0]:
        await message.answer_document(FSInputFile(i))


