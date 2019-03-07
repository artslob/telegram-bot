from telegram.objects import telegram_field as field, TelegramMethodObject


class SendMessageObject(TelegramMethodObject):
    # not complete list of fields!

    def __init__(self,
                 chat_id,
                 text,
                 parse_mode=None,
                 disable_web_page_preview=None,
                 disable_notification=None,
                 reply_to_message_id=None,
                 **kwargs):
        # required
        self.chat_id = chat_id
        self.text = field(str, text, required=True)
        # optional
        self.parse_mode = field(str, parse_mode)
        self.disable_web_page_preview = field(bool, disable_web_page_preview)
        self.disable_notification = field(bool, disable_notification)
        self.reply_to_message_id = field(int, reply_to_message_id)
