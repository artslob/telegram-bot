class TelegramObject:
    @classmethod
    def from_dict(cls, dct: dict):
        return cls(**dct)
