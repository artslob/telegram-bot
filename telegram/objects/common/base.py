class TelegramObject:
    # TODO add saving of input dict and method to_dict

    @classmethod
    def from_dict(cls, dct: dict):
        return cls(**dct)
