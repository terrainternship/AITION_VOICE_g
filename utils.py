# Библиотека для воспроизведения звуковых файлов
import json
from pathlib import Path

import IPython.display as ipd
from pydub import AudioSegment


def ogg_to_wav(source: Path | str, destination: Path | str):
    # Load the .ogg file
    audio = AudioSegment.from_ogg(source)

    # Convert the audio to WAV format
    audio.export(format='wav', out_f=destination)


def display_audio(filename: Path | str):
    print(filename)
    ipd.display(ipd.Audio(filename))


def plain_text_to_dict(source_file: Path | str, target_file: Path | str):
    """
    Конвертирует данные из файла source_file в формате: audio_2023-11-20_18-04-29.ogg Таргетный текст аудио записи
    в формат python dict и сохраняет данные в файл target_file

    :param source_file: Path | str
    :param target_file: Path | str
    :return: None
    """
    source = open(source_file, 'r')
    data = source.read()
    source.close()

    lines = data.split('\n')
    # print('Data', data)
    print('Lines: ', lines)
    targets = {}
    for line in lines:
        file_text = line.split('\t')
        if len(file_text) == 2:
            targets.update({file_text[0]: file_text[1]})
        else:
            print('file_text', file_text)

    target = open(target_file, 'w')
    target.write(json.dumps(targets, ensure_ascii=False, indent=4))
    target.close()


if __name__ == '__main__':
    DATASET_DIR = Path().absolute().joinpath(Path().absolute().parent, 'data_set')
    plain_text_to_dict(Path(DATASET_DIR, 'targets.txt'), Path(DATASET_DIR, 'targets.json'))
