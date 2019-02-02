from telegram.objects import TelegramObject, telegram_field as field, Chat
from telegram.objects.user import User


class Message(TelegramObject):
    # not complete list of fields!

    def __init__(self,
                 dct,
                 message_id,
                 date,
                 chat,
                 from_user=None,
                 text=None,
                 **kwargs):
        super().__init__(dct)
        # required
        self.message_id = field(int, message_id, required=True)
        self.date = field(int, date, required=True)
        self.chat = field(Chat, chat, required=True)
        # optional
        self.from_user = field(User, from_user)
        self.text = field(str, text)

    @classmethod
    def from_dict(cls, dct: dict):
        if 'from' in dct:
            dct['from_user'] = dct.pop('from')
        return super().from_dict(dct)
