import zipfile
from pathlib import Path


def create_dir_if_not_exists(directory_path):
    path = Path(directory_path)
    if not path.exists():
        path.mkdir(parents=True)
        print(f"Папка '{directory_path}' была создана.")
        return directory_path
    else:
        directory_path = directory_path + '1'
        return create_dir_if_not_exists(directory_path)



def open_file(file_path):
    a = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f]
    for i in lines:
        if i not in a:
            a.append(i)

    return (sorted(a), len(lines), len(a))


def divide_array(chunks, dir_path):
    data = open_file(dir_path)
    input_array = data[0]
    chunks = int(chunks)
    # Если число частей больше, чем длина массива, возвращаем ошибку
    if chunks > len(input_array):
        return False

    chunk_size = len(input_array) // chunks

    # Вычисляем количество элементов, которые останутся после первоначального деления
    remainder = len(input_array) % chunks

    # Инициализируем массив для хранения подмассивов
    divided = []

    # Начальный индекс для следующего подмассива
    start_index = 0

    for i in range(chunks):
        # Для каждого подмассива добавляем 1 к размеру подмассива, если остаток еще не распределен
        end_index = start_index + chunk_size + (1 if i < remainder else 0)
        # Добавляем срез исходного массива в список подмассивов
        divided.append(input_array[start_index:end_index])
        # Обновляем начальный индекс для следующего подмассива
        start_index = end_index

    return (divided, data[1], data[2])




def write_files(dir_path, chunks):
    data = divide_array(chunks=chunks, dir_path=dir_path)
    arr = data[0]
    print(Path(dir_path).resolve())
    file_paths = []

    # Записываем каждый подмассив в отдельный файл
    for i, chunk in enumerate(arr, 1):
        file_path = Path(dir_path).resolve().parent / f"База {i}.txt"
        with file_path.open(mode='w', encoding='utf-8') as file:
            for element in chunk:
                file.write(f"{element}\n")
        file_paths.append(file_path)

    return (file_paths, data[1], data[2])



# def create_zip_archive(dir_path, chunks):
#     files = write_files(chunks=chunks, dir_path=dir_path)
#     archive_path = Path(dir_path).resolve().parent / 'sort.zip'
#     with zipfile.ZipFile(archive_path, 'w') as zipf:
#         for file_path in files:
#             # Добавляем файл в архив
#             zipf.write(file_path, arcname=file_path.name)
#     return archive_path