import json


class TelegramObject:
    def __init__(self, dct: dict, *args, **kwargs):
        self.dct = dct

    def to_dict(self):
        return self.dct

    @classmethod
    def from_dict(cls, dct: dict):
        return cls(dct, **dct)

    def to_str(self):
        return json.dumps(self.to_dict(), indent=4)
