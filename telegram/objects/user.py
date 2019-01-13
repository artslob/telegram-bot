from telegram.objects import TelegramObject, RequiredField, OptionalField


class User(TelegramObject):
    # required
    id = RequiredField(int)
    is_bot = RequiredField(bool)
    first_name = RequiredField(str)
    # optional
    last_name = OptionalField(str)
    username = OptionalField(str)
    language_code = OptionalField(str)

    def __init__(self,
                 id,
                 is_bot,
                 first_name,
                 last_name=None,
                 username=None,
                 language_code=None,
                 **kwargs):
        # required
        self.id = self.id(id)
        self.is_bot = self.is_bot(is_bot)
        # optional
        self.first_name = self.first_name(first_name)
        self.last_name = self.last_name(last_name)
        self.username = self.username(username)
        self.language_code = self.language_code(language_code)
