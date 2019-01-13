from telegram.objects import TelegramObject, RequiredField, OptionalField, Message


class Update(TelegramObject):
    # required
    update_id = RequiredField(int)
    # optional
    message = OptionalField(Message)
    edited_message = OptionalField(Message)
    channel_post = OptionalField(Message)
    edited_channel_post = OptionalField(Message)

    # not complete list of fields!

    def __init__(self,
                 update_id,
                 message=None,
                 edited_message=None,
                 channel_post=None,
                 edited_channel_post=None,
                 **kwargs):
        # required
        self.update_id = self.update_id(update_id)
        # optional
        self.message = self.message(message)
        self.edited_message = self.edited_message(edited_message)
        self.channel_post = self.channel_post(channel_post)
        self.edited_channel_post = self.edited_channel_post(edited_channel_post)
