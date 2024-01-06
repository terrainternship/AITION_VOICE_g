import json


class Transcription:
    def __init__(self, name: str, model: str, transcribed_text: str = None, run_time: float = 0):
        self.name = name
        self.model = model
        self.transcribed_text = transcribed_text
        self.run_time = run_time


class AudioTrack:

    def __init__(self, filename: str, target_text: str = None, transcriptions: list[Transcription] = None):
        self.filename = filename
        self.target_text = target_text
        self.transcriptions = transcriptions

    def __dict__(self):
        return dict(filename=self.filename, target_text=self.target_text,
                    transcriptions=[tr.__dict__ for tr in self.transcriptions])

    # @property
    # def target_text(self):
    #     return self.target_text
    #
    # @target_text.setter
    # def target_text(self, value):
    #     self.target_text = value


if __name__ == '__main__':
    t = Transcription(name='speech_recognizer', model='recognize_google', transcribed_text='text', run_time=12345)
    a = AudioTrack(filename='output.ogg', target_text='target_text', transcriptions=[t])

    print('t:', t.__dict__)
    print('a', a.__dict__())
    json_str = json.dumps(a.__dict__())
    print('json a', json_str)
