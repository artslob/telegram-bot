class TelegramObject:
    def __init__(self, dct: dict, *args, **kwargs):
        self.dct = dct

    def to_dict(self):
        return self.dct

    @classmethod
    def from_dict(cls, dct: dict):
        return cls(dct, **dct)
