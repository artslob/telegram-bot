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
        self.id = field(int, id, required=True)
        self.is_bot = field(bool, is_bot, required=True)
        self.first_name = field(str, first_name, required=True)
        # optional
        self.last_name = field(str, last_name)
        self.username = field(str, username)
        self.language_code = field(str, language_code)
