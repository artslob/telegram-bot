from telegram.objects import TelegramObject, RequiredField, OptionalField, Chat
from telegram.objects.user import User


class Message(TelegramObject):
    # required
    message_id = RequiredField(int)
    date = RequiredField(int)
    chat = RequiredField(Chat)
    # optional
    from_user = OptionalField(User)  # TODO handle 'from' field
    text = OptionalField(str)

    # not complete list of fields!

    def __init__(self,
                 message_id,
                 date,
                 chat,
                 from_user=None,
                 text=None,
                 **kwargs):
        # required
        self.message_id = self.message_id(message_id)
        self.date = self.date(date)
        self.chat = self.chat(chat)
        # optional
        self.from_user = self.from_user(from_user)
        self.text = self.text(text)
