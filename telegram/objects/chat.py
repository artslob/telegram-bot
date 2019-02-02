from telegram.objects import TelegramObject, telegram_field as field


class Chat(TelegramObject):
    # not complete list of fields!

    def __init__(self,
                 dct,
                 id,
                 type,
                 title=None,
                 username=None,
                 first_name=None,
                 last_name=None,
                 all_members_are_administrators=None,
                 description=None,
                 invite_link=None,
                 pinned_message=None,
                 sticker_set_name=None,
                 can_set_sticker_set=None,
                 **kwargs):
        super().__init__(dct)
        # required
        self.id = field(int, id, required=True)
        self.type = field(str, type, required=True)
        # optional
        self.title = field(str, title)
        self.username = field(str, username)
        self.first_name = field(str, first_name)
        self.last_name = field(str, last_name)
        self.all_members_are_administrators = field(bool, all_members_are_administrators)
        self.description = field(str, description)
        self.invite_link = field(str, invite_link)
        from telegram.objects import Message
        self.pinned_message = field(Message, pinned_message)
        self.sticker_set_name = field(str, sticker_set_name)
        self.can_set_sticker_set = field(bool, can_set_sticker_set)
