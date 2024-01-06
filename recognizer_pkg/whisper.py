import time
from pathlib import Path

import whisper

from recognizer_pkg.recognizer import SpeechRecognizer
from transcription import Transcription


class WhisperRecognizer(SpeechRecognizer):
    # acceptable_whisper_models = ['tiny', 'base', 'small', 'medium', 'large', 'large-v2', 'large-v3']
    def recognize(self, filename) -> Transcription:
        if not Path(filename).exists():
            raise FileNotFoundError(f'File {filename} not fount.')
        self.start_at = time.time()
        model = whisper.load_model(self.model)
        transcription = model.transcribe(filename, fp16=False)
        self.finished_at = time.time()
        return Transcription(
            name='whisper',
            model=self.model,
            transcribed_text=transcription['text'],
            run_time=self.finished_at-self.start_at
        )

