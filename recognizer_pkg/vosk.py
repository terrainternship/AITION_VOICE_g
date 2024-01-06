import json
import time

import librosa
from pathlib import Path

from librosa import stream
from vosk import Model, KaldiRecognizer

from recognizer_pkg.recognizer import SpeechRecognizer
from transcription import Transcription


class VoskRecognizer(SpeechRecognizer):

    def __init__(self, model_name='vosk-model-ru-0.42', *,
                 lang='ru', sample_rate=16000, block_size=4000, name=None):
        name = name if name else model_name
        super().__init__(name, sample_rate)
        lang = model_name.split('-')[-2] if model_name else lang
        self.lang = lang
        self.block_size = block_size
        self.model_name = model_name
        self.model = Model(lang=lang, model_name=model_name)
        self.recognizer = KaldiRecognizer(self.model, self.sample_rate)
        self.recognizer.SetWords(True)

    def recognize(self, source: Path | str):
        if isinstance(source, Path) or isinstance(source, str):
            return self.recognize_from_file(source)
        else:
            raise TypeError('Source must be file path.')

    def recognize_from_stream(self, stream) -> Transcription:
        """
          Recognize words from bytes stream.
        """
        self.start_at = time.time()
        results = []
        data = stream.read()
        for i in range(0, len(data), self.block_size):
            data_block = data[i:i + self.block_size]
            if len(data) == 0:
                break
            if self.recognizer.AcceptWaveform(data_block):
                results.append(json.loads(self.recognizer.Result())["text"])

        text = json.loads(self.recognizer.FinalResult())["text"]
        if text:
            results.append(text)

        results = ' '.join(results)
        stream.close()
        self.finished_at = time.time()
        # return results
        return Transcription(
            name='vosk',
            model=self.model_name,
            transcribed_text=results,
            run_time=self.finished_at - self.start_at
        )

    def recognize_from_file(self, filename: Path | str):
        """
          Recognize words from WAV file.
        """
        if not Path(filename).exists():
            raise FileNotFoundError(f'File {filename} not found')
        audio, sr = librosa.load(filename, sr=self.sample_rate)
        audio = self.resample(audio, int(sr))
        stream = self.to_stream(audio)
        return self.recognize_from_stream(stream)
