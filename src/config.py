# Путь к видео
_VIDEO_PATH = None

# Функция для получения пути к файлу
def get_file_path():
    return _VIDEO_PATH

# Функция для изменения пути к файлу
def set_file_path(new_path):
    global _VIDEO_PATH
    _VIDEO_PATH = new_path