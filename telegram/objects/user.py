from telegram.objects import TelegramObject, telegram_field as field


class User(TelegramObject):
    def __init__(self,
                 dct,
                 id,
                 is_bot,
                 first_name,
                 last_name=None,
                 username=None,
                 language_code=None,
                 **kwargs):
        super().__init__(dct)
        # required
        self.id = field(int, id, required=True)  # type: int
        self.is_bot = field(bool, is_bot, required=True)  # type: bool
        self.first_name = field(str, first_name, required=True)  # type: str
        # optional
        self.last_name = field(str, last_name)  # type: str
        self.username = field(str, username)  # type: str
        self.language_code = field(str, language_code)  # type: str
