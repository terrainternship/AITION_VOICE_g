import time

import speech_recognition as sr
from recognizer_pkg.recognizer import SpeechRecognizer
from transcription import Transcription


class GoogleRecognizer(SpeechRecognizer):
    def __init__(self, model: str = 'recognize_google', sample_rate: int = 16000, **kwargs):
        super().__init__(model, sample_rate, **kwargs)

    def recognize(self, filename) -> Transcription:
        """
        Функция для распознавания речи

        Args:
            filename - аудиофайл с записанной речью, wav
            offset - с какой секунды начать распознавание, int
            duration - длина распознаваемого фрагмента, int

        Returns:
            распознанный текст, str
        """

        self.start_at = time.time()
        # Создаем объект класса Recognizer
        recognizer = sr.Recognizer()

        # Считываем аудиофайл
        with sr.AudioFile(filename) as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source)

            # Recognize the speech
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio, language="ru")
                self.finished_at = time.time()

                return Transcription(
                    name='speech_recognition',
                    model='recognize_google',
                    transcribed_text=text,
                    run_time=self.finished_at - self.start_at
                )
            except sr.UnknownValueError:
                print("Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
