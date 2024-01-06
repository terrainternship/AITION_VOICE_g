import io
import time
import librosa
import soundfile as sf

from abc import ABC, abstractmethod


class SpeechRecognizer(ABC):
    """
      Abstract class to handle speach recognition.

      Args:
          model (str): recogniser's model name
          sample_rate (int): sample rate of the recognisable audio
    """

    def __init__(self, model: str, sample_rate: int = 16000, **kwargs):
        self.model = model
        self.sample_rate = sample_rate
        self.start_at = None
        self.finished_at = None
        self.stream = None
        self.__dict__.update(kwargs)

    def __call__(self, filename):
        return self.recognize(filename)

    def __enter__(self):
        self.start_at = time.time()
        return self

    def __exit__(self, type, value, traceback):
        self.finished_at = time.time()
        if self.stream:
            self.stream.close()

    @abstractmethod
    def recognize(self, filename):
        raise NotImplementedError()

    def resample(self, audio, sample_rate: int):
        audio = librosa.resample(audio, orig_sr=sample_rate, target_sr=self.sample_rate)
        return audio

    def to_stream(self, audio):
        self.stream = io.BytesIO()
        sf.write(self.stream, audio, self.sample_rate, format='WAV', subtype='PCM_16')
        self.stream.seek(0)
        return self.stream

    def run_time(self) -> float:
        if not self.finished_at:
            self.finished_at = time.time()
        return round(self.finished_at - self.start_at, 4)
