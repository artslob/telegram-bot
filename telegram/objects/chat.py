from telegram.objects import TelegramObject, RequiredField, OptionalField


class Chat(TelegramObject):
    # required
    id = RequiredField(int)
    type = RequiredField(str)
    # optional
    title = OptionalField(str)
    username = OptionalField(str)
    first_name = OptionalField(str)
    last_name = OptionalField(str)
    all_members_are_administrators = OptionalField(bool)
    description = OptionalField(str)
    invite_link = OptionalField(str)
    # pinned_message = OptionalField(Message)
    sticker_set_name = OptionalField(str)
    can_set_sticker_set = OptionalField(bool)

    # not complete list of fields!

    def __init__(self,
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
        # required
        self.id = self.id(id)
        self.type = self.type(type)
        # optional
        self.title = self.title(title)
        self.username = self.username(username)
        self.first_name = self.first_name(first_name)
        self.last_name = self.last_name(last_name)
        self.all_members_are_administrators = self.all_members_are_administrators(all_members_are_administrators)
        self.description = self.description(description)
        self.invite_link = self.invite_link(invite_link)
        from telegram.objects import Message
        self.pinned_message = OptionalField(Message)(pinned_message)
        self.sticker_set_name = self.sticker_set_name(sticker_set_name)
        self.can_set_sticker_set = self.can_set_sticker_set(can_set_sticker_set)
