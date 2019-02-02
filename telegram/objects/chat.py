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
        self.id = field(int, id, required=True)  # type: int
        self.type = field(str, type, required=True)  # type: str
        # optional
        self.title = field(str, title)  # type: str
        self.username = field(str, username)  # type: str
        self.first_name = field(str, first_name)  # type: str
        self.last_name = field(str, last_name)  # type: str
        self.all_members_are_administrators = field(bool, all_members_are_administrators)  # type: bool
        self.description = field(str, description)  # type: str
        self.invite_link = field(str, invite_link)  # type: str
        from telegram.objects import Message
        self.pinned_message = field(Message, pinned_message)  # type: Message
        self.sticker_set_name = field(str, sticker_set_name)  # type: str
        self.can_set_sticker_set = field(bool, can_set_sticker_set)  # type: bool
