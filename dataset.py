import os


class Dataset:
    __files = []

    @classmethod
    def __extract_files_range(cls, path, first_file, last_file):
        if not os.path.exists(path):
            print(f'Directory {path} does not exist.')
            return None
        audio_files = sorted([file for file in os.listdir(path) if file.endswith('.ogg')])

        try:
            start_index = audio_files.index(first_file)
            if not start_index:
                print(f'File {first_file} not found.')
                return None
            end_index = audio_files.index(last_file) + 1
            if not end_index:
                print(f'File {last_file} not found.')
                return None
            selected_files = audio_files[start_index:end_index]

            cls.__files = selected_files
        except ValueError:
            return None

    def __init__(self, dir_path, first_file, last_file):
        self.__extract_files_range(dir_path, first_file, last_file)
        self.__current_index = 0
        self.__number = len(self.__files)

    def __iter__(self):
        self.__current_index = 0
        return self

    def __next__(self):
        if self.__current_index == self.__number:
            raise StopIteration()
        file = self.__files[self.__current_index]
        self.__current_index += 1
        return file
