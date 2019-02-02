from telegram.objects import TelegramObject, telegram_field as field, Message


class Update(TelegramObject):
    # not complete list of fields!

    def __init__(self,
                 dct,
                 update_id,
                 message=None,
                 edited_message=None,
                 channel_post=None,
                 edited_channel_post=None,
                 **kwargs):
        super().__init__(dct)
        # required
        self.update_id = field(int, update_id, required=True)
        # optional
        self.message = field(Message, message)
        self.edited_message = field(Message, edited_message)
        self.channel_post = field(Message, channel_post)
        self.edited_channel_post = field(Message, edited_channel_post)
