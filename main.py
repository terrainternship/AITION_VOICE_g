import json

from pathlib import Path

from dataset import Dataset
from recognizer_pkg.google import GoogleRecognizer
from recognizer_pkg.vosk import VoskRecognizer
from recognizer_pkg.whisper import WhisperRecognizer
from transcription import Transcription, AudioTrack
from utils import ogg_to_wav

DATASET_DIR = Path().absolute().joinpath(Path().absolute().parent, 'data_set')
AUDIO_NAME_BEGIN = 'audio_2023-12-25_20-48-37.ogg'
AUDIO_NAME_END = 'audio_2023-12-25_20-49-02.ogg'

data_set = Dataset(DATASET_DIR, AUDIO_NAME_BEGIN, AUDIO_NAME_END)


google_rec = GoogleRecognizer()
vosk_rec = VoskRecognizer()
# acceptable_whisper_models = ['tiny', 'base', 'small', 'medium', 'large', 'large-v2', 'large-v3']
whisper_rec = WhisperRecognizer('medium')
audio_list = []

targets_file: type(open) = None
try:
    targets_file = open(Path(DATASET_DIR, 'targets.json'), 'r')
    targets = json.loads(targets_file.read())
    print('Targets: ', targets)
except:
    raise Exception('Cannot get targets_text')
finally:
    if targets_file:
        targets_file.close()

for f in data_set:
    source_file = Path(DATASET_DIR, f)
    wav_file = Path(DATASET_DIR, 'output.wav')
    ogg_to_wav(source_file, wav_file)
    print(source_file)
    google_transcription: Transcription = google_rec(str(wav_file))
    vosk_transcription: Transcription = vosk_rec(str(wav_file))
    whisper_transcription: Transcription = whisper_rec(str(wav_file))

    audio_track = AudioTrack(
        filename=f,
        target_text=targets[f],
        transcriptions=[google_transcription, vosk_transcription, whisper_transcription]
    )
    audio_track_dict = audio_track.__dict__()
    audio_list.append(audio_track_dict)
    print(audio_track_dict)

with open(Path(DATASET_DIR, 'transcriptions.json'), 'w') as file:
    json.dump(audio_list, file, indent=4, ensure_ascii=False)
