"""File generated by TLObjects' generator. All changes will be ERASED"""
from ...tl.tlobject import TLObject
from ...tl.tlobject import TLRequest
from typing import Optional, List, Union, TYPE_CHECKING
import os
import struct
from datetime import datetime
if TYPE_CHECKING:
    from ...tl.types import TypeInputMedia, TypeInputPrivacyRule, TypeInputUser, TypeMediaArea, TypeMessageEntity, TypeReaction, TypeReportReason



class ActivateStealthModeRequest(TLRequest):
    CONSTRUCTOR_ID = 0x57bbd166
    SUBCLASS_OF_ID = 0x8af52aac

    def __init__(self, past: Optional[bool]=None, future: Optional[bool]=None):
        """
        :returns Updates: Instance of either UpdatesTooLong, UpdateShortMessage, UpdateShortChatMessage, UpdateShort, UpdatesCombined, Updates, UpdateShortSentMessage.
        """
        self.past = past
        self.future = future

    def to_dict(self):
        return {
            '_': 'ActivateStealthModeRequest',
            'past': self.past,
            'future': self.future
        }

    def _bytes(self):
        return b''.join((
            b'f\xd1\xbbW',
            struct.pack('<I', (0 if self.past is None or self.past is False else 1) | (0 if self.future is None or self.future is False else 2)),
        ))

    @classmethod
    def from_reader(cls, reader):
        flags = reader.read_int()

        _past = bool(flags & 1)
        _future = bool(flags & 2)
        return cls(past=_past, future=_future)


class CanSendStoryRequest(TLRequest):
    CONSTRUCTOR_ID = 0xb100d45d
    SUBCLASS_OF_ID = 0xf5b399ac

    def to_dict(self):
        return {
            '_': 'CanSendStoryRequest'
        }

    def _bytes(self):
        return b''.join((
            b']\xd4\x00\xb1',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class DeleteStoriesRequest(TLRequest):
    CONSTRUCTOR_ID = 0xb5d501d7
    SUBCLASS_OF_ID = 0x5026710f

    def __init__(self, id: List[int]):
        """
        :returns Vector<int>: This type has no constructors.
        """
        self.id = id

    def to_dict(self):
        return {
            '_': 'DeleteStoriesRequest',
            'id': [] if self.id is None else self.id[:]
        }

    def _bytes(self):
        return b''.join((
            b'\xd7\x01\xd5\xb5',
            b'\x15\xc4\xb5\x1c',struct.pack('<i', len(self.id)),b''.join(struct.pack('<i', x) for x in self.id),
        ))

    @classmethod
    def from_reader(cls, reader):
        reader.read_int()
        _id = []
        for _ in range(reader.read_int()):
            _x = reader.read_int()
            _id.append(_x)

        return cls(id=_id)

    @staticmethod
    def read_result(reader):
        reader.read_int()  # Vector ID
        return [reader.read_int() for _ in range(reader.read_int())]


class EditStoryRequest(TLRequest):
    CONSTRUCTOR_ID = 0xa9b91ae4
    SUBCLASS_OF_ID = 0x8af52aac

    def __init__(self, id: int, media: Optional['TypeInputMedia']=None, media_areas: Optional[List['TypeMediaArea']]=None, caption: Optional[str]=None, entities: Optional[List['TypeMessageEntity']]=None, privacy_rules: Optional[List['TypeInputPrivacyRule']]=None):
        """
        :returns Updates: Instance of either UpdatesTooLong, UpdateShortMessage, UpdateShortChatMessage, UpdateShort, UpdatesCombined, Updates, UpdateShortSentMessage.
        """
        self.id = id
        self.media = media
        self.media_areas = media_areas
        self.caption = caption
        self.entities = entities
        self.privacy_rules = privacy_rules

    async def resolve(self, client, utils):
        if self.media:
            self.media = utils.get_input_media(self.media)

    def to_dict(self):
        return {
            '_': 'EditStoryRequest',
            'id': self.id,
            'media': self.media.to_dict() if isinstance(self.media, TLObject) else self.media,
            'media_areas': [] if self.media_areas is None else [x.to_dict() if isinstance(x, TLObject) else x for x in self.media_areas],
            'caption': self.caption,
            'entities': [] if self.entities is None else [x.to_dict() if isinstance(x, TLObject) else x for x in self.entities],
            'privacy_rules': [] if self.privacy_rules is None else [x.to_dict() if isinstance(x, TLObject) else x for x in self.privacy_rules]
        }

    def _bytes(self):
        assert ((self.caption or self.caption is not None) and (self.entities or self.entities is not None)) or ((self.caption is None or self.caption is False) and (self.entities is None or self.entities is False)), 'caption, entities parameters must all be False-y (like None) or all me True-y'
        return b''.join((
            b'\xe4\x1a\xb9\xa9',
            struct.pack('<I', (0 if self.media is None or self.media is False else 1) | (0 if self.media_areas is None or self.media_areas is False else 8) | (0 if self.caption is None or self.caption is False else 2) | (0 if self.entities is None or self.entities is False else 2) | (0 if self.privacy_rules is None or self.privacy_rules is False else 4)),
            struct.pack('<i', self.id),
            b'' if self.media is None or self.media is False else (self.media._bytes()),
            b'' if self.media_areas is None or self.media_areas is False else b''.join((b'\x15\xc4\xb5\x1c',struct.pack('<i', len(self.media_areas)),b''.join(x._bytes() for x in self.media_areas))),
            b'' if self.caption is None or self.caption is False else (self.serialize_bytes(self.caption)),
            b'' if self.entities is None or self.entities is False else b''.join((b'\x15\xc4\xb5\x1c',struct.pack('<i', len(self.entities)),b''.join(x._bytes() for x in self.entities))),
            b'' if self.privacy_rules is None or self.privacy_rules is False else b''.join((b'\x15\xc4\xb5\x1c',struct.pack('<i', len(self.privacy_rules)),b''.join(x._bytes() for x in self.privacy_rules))),
        ))

    @classmethod
    def from_reader(cls, reader):
        flags = reader.read_int()

        _id = reader.read_int()
        if flags & 1:
            _media = reader.tgread_object()
        else:
            _media = None
        if flags & 8:
            reader.read_int()
            _media_areas = []
            for _ in range(reader.read_int()):
                _x = reader.tgread_object()
                _media_areas.append(_x)

        else:
            _media_areas = None
        if flags & 2:
            _caption = reader.tgread_string()
        else:
            _caption = None
        if flags & 2:
            reader.read_int()
            _entities = []
            for _ in range(reader.read_int()):
                _x = reader.tgread_object()
                _entities.append(_x)

        else:
            _entities = None
        if flags & 4:
            reader.read_int()
            _privacy_rules = []
            for _ in range(reader.read_int()):
                _x = reader.tgread_object()
                _privacy_rules.append(_x)

        else:
            _privacy_rules = None
        return cls(id=_id, media=_media, media_areas=_media_areas, caption=_caption, entities=_entities, privacy_rules=_privacy_rules)


class ExportStoryLinkRequest(TLRequest):
    CONSTRUCTOR_ID = 0x16e443ce
    SUBCLASS_OF_ID = 0xfc541a6

    def __init__(self, user_id: 'TypeInputUser', id: int):
        """
        :returns ExportedStoryLink: Instance of ExportedStoryLink.
        """
        self.user_id = user_id
        self.id = id

    async def resolve(self, client, utils):
        self.user_id = utils.get_input_user(await client.get_input_entity(self.user_id))

    def to_dict(self):
        return {
            '_': 'ExportStoryLinkRequest',
            'user_id': self.user_id.to_dict() if isinstance(self.user_id, TLObject) else self.user_id,
            'id': self.id
        }

    def _bytes(self):
        return b''.join((
            b'\xceC\xe4\x16',
            self.user_id._bytes(),
            struct.pack('<i', self.id),
        ))

    @classmethod
    def from_reader(cls, reader):
        _user_id = reader.tgread_object()
        _id = reader.read_int()
        return cls(user_id=_user_id, id=_id)


class GetAllReadUserStoriesRequest(TLRequest):
    CONSTRUCTOR_ID = 0x729c562c
    SUBCLASS_OF_ID = 0x8af52aac

    def to_dict(self):
        return {
            '_': 'GetAllReadUserStoriesRequest'
        }

    def _bytes(self):
        return b''.join((
            b',V\x9cr',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class GetAllStoriesRequest(TLRequest):
    CONSTRUCTOR_ID = 0xeeb0d625
    SUBCLASS_OF_ID = 0x7e60d0cd

    def __init__(self, next: Optional[bool]=None, hidden: Optional[bool]=None, state: Optional[str]=None):
        """
        :returns stories.AllStories: Instance of either AllStoriesNotModified, AllStories.
        """
        self.next = next
        self.hidden = hidden
        self.state = state

    def to_dict(self):
        return {
            '_': 'GetAllStoriesRequest',
            'next': self.next,
            'hidden': self.hidden,
            'state': self.state
        }

    def _bytes(self):
        return b''.join((
            b'%\xd6\xb0\xee',
            struct.pack('<I', (0 if self.next is None or self.next is False else 2) | (0 if self.hidden is None or self.hidden is False else 4) | (0 if self.state is None or self.state is False else 1)),
            b'' if self.state is None or self.state is False else (self.serialize_bytes(self.state)),
        ))

    @classmethod
    def from_reader(cls, reader):
        flags = reader.read_int()

        _next = bool(flags & 2)
        _hidden = bool(flags & 4)
        if flags & 1:
            _state = reader.tgread_string()
        else:
            _state = None
        return cls(next=_next, hidden=_hidden, state=_state)


class GetPinnedStoriesRequest(TLRequest):
    CONSTRUCTOR_ID = 0xb471137
    SUBCLASS_OF_ID = 0x251c0c2c

    def __init__(self, user_id: 'TypeInputUser', offset_id: int, limit: int):
        """
        :returns stories.Stories: Instance of Stories.
        """
        self.user_id = user_id
        self.offset_id = offset_id
        self.limit = limit

    async def resolve(self, client, utils):
        self.user_id = utils.get_input_user(await client.get_input_entity(self.user_id))

    def to_dict(self):
        return {
            '_': 'GetPinnedStoriesRequest',
            'user_id': self.user_id.to_dict() if isinstance(self.user_id, TLObject) else self.user_id,
            'offset_id': self.offset_id,
            'limit': self.limit
        }

    def _bytes(self):
        return b''.join((
            b'7\x11G\x0b',
            self.user_id._bytes(),
            struct.pack('<i', self.offset_id),
            struct.pack('<i', self.limit),
        ))

    @classmethod
    def from_reader(cls, reader):
        _user_id = reader.tgread_object()
        _offset_id = reader.read_int()
        _limit = reader.read_int()
        return cls(user_id=_user_id, offset_id=_offset_id, limit=_limit)


class GetStoriesArchiveRequest(TLRequest):
    CONSTRUCTOR_ID = 0x1f5bc5d2
    SUBCLASS_OF_ID = 0x251c0c2c

    def __init__(self, offset_id: int, limit: int):
        """
        :returns stories.Stories: Instance of Stories.
        """
        self.offset_id = offset_id
        self.limit = limit

    def to_dict(self):
        return {
            '_': 'GetStoriesArchiveRequest',
            'offset_id': self.offset_id,
            'limit': self.limit
        }

    def _bytes(self):
        return b''.join((
            b'\xd2\xc5[\x1f',
            struct.pack('<i', self.offset_id),
            struct.pack('<i', self.limit),
        ))

    @classmethod
    def from_reader(cls, reader):
        _offset_id = reader.read_int()
        _limit = reader.read_int()
        return cls(offset_id=_offset_id, limit=_limit)


class GetStoriesByIDRequest(TLRequest):
    CONSTRUCTOR_ID = 0x6a15cf46
    SUBCLASS_OF_ID = 0x251c0c2c

    def __init__(self, user_id: 'TypeInputUser', id: List[int]):
        """
        :returns stories.Stories: Instance of Stories.
        """
        self.user_id = user_id
        self.id = id

    async def resolve(self, client, utils):
        self.user_id = utils.get_input_user(await client.get_input_entity(self.user_id))

    def to_dict(self):
        return {
            '_': 'GetStoriesByIDRequest',
            'user_id': self.user_id.to_dict() if isinstance(self.user_id, TLObject) else self.user_id,
            'id': [] if self.id is None else self.id[:]
        }

    def _bytes(self):
        return b''.join((
            b'F\xcf\x15j',
            self.user_id._bytes(),
            b'\x15\xc4\xb5\x1c',struct.pack('<i', len(self.id)),b''.join(struct.pack('<i', x) for x in self.id),
        ))

    @classmethod
    def from_reader(cls, reader):
        _user_id = reader.tgread_object()
        reader.read_int()
        _id = []
        for _ in range(reader.read_int()):
            _x = reader.read_int()
            _id.append(_x)

        return cls(user_id=_user_id, id=_id)


class GetStoriesViewsRequest(TLRequest):
    CONSTRUCTOR_ID = 0x9a75d6a6
    SUBCLASS_OF_ID = 0x4b3fc4ba

    def __init__(self, id: List[int]):
        """
        :returns stories.StoryViews: Instance of StoryViews.
        """
        self.id = id

    def to_dict(self):
        return {
            '_': 'GetStoriesViewsRequest',
            'id': [] if self.id is None else self.id[:]
        }

    def _bytes(self):
        return b''.join((
            b'\xa6\xd6u\x9a',
            b'\x15\xc4\xb5\x1c',struct.pack('<i', len(self.id)),b''.join(struct.pack('<i', x) for x in self.id),
        ))

    @classmethod
    def from_reader(cls, reader):
        reader.read_int()
        _id = []
        for _ in range(reader.read_int()):
            _x = reader.read_int()
            _id.append(_x)

        return cls(id=_id)


class GetStoryViewsListRequest(TLRequest):
    CONSTRUCTOR_ID = 0xf95f61a4
    SUBCLASS_OF_ID = 0xb9437560

    def __init__(self, id: int, offset: str, limit: int, just_contacts: Optional[bool]=None, reactions_first: Optional[bool]=None, q: Optional[str]=None):
        """
        :returns stories.StoryViewsList: Instance of StoryViewsList.
        """
        self.id = id
        self.offset = offset
        self.limit = limit
        self.just_contacts = just_contacts
        self.reactions_first = reactions_first
        self.q = q

    def to_dict(self):
        return {
            '_': 'GetStoryViewsListRequest',
            'id': self.id,
            'offset': self.offset,
            'limit': self.limit,
            'just_contacts': self.just_contacts,
            'reactions_first': self.reactions_first,
            'q': self.q
        }

    def _bytes(self):
        return b''.join((
            b'\xa4a_\xf9',
            struct.pack('<I', (0 if self.just_contacts is None or self.just_contacts is False else 1) | (0 if self.reactions_first is None or self.reactions_first is False else 4) | (0 if self.q is None or self.q is False else 2)),
            b'' if self.q is None or self.q is False else (self.serialize_bytes(self.q)),
            struct.pack('<i', self.id),
            self.serialize_bytes(self.offset),
            struct.pack('<i', self.limit),
        ))

    @classmethod
    def from_reader(cls, reader):
        flags = reader.read_int()

        _just_contacts = bool(flags & 1)
        _reactions_first = bool(flags & 4)
        if flags & 2:
            _q = reader.tgread_string()
        else:
            _q = None
        _id = reader.read_int()
        _offset = reader.tgread_string()
        _limit = reader.read_int()
        return cls(id=_id, offset=_offset, limit=_limit, just_contacts=_just_contacts, reactions_first=_reactions_first, q=_q)


class GetUserStoriesRequest(TLRequest):
    CONSTRUCTOR_ID = 0x96d528e0
    SUBCLASS_OF_ID = 0xc6b1923d

    def __init__(self, user_id: 'TypeInputUser'):
        """
        :returns stories.UserStories: Instance of UserStories.
        """
        self.user_id = user_id

    async def resolve(self, client, utils):
        self.user_id = utils.get_input_user(await client.get_input_entity(self.user_id))

    def to_dict(self):
        return {
            '_': 'GetUserStoriesRequest',
            'user_id': self.user_id.to_dict() if isinstance(self.user_id, TLObject) else self.user_id
        }

    def _bytes(self):
        return b''.join((
            b'\xe0(\xd5\x96',
            self.user_id._bytes(),
        ))

    @classmethod
    def from_reader(cls, reader):
        _user_id = reader.tgread_object()
        return cls(user_id=_user_id)


class IncrementStoryViewsRequest(TLRequest):
    CONSTRUCTOR_ID = 0x22126127
    SUBCLASS_OF_ID = 0xf5b399ac

    def __init__(self, user_id: 'TypeInputUser', id: List[int]):
        """
        :returns Bool: This type has no constructors.
        """
        self.user_id = user_id
        self.id = id

    async def resolve(self, client, utils):
        self.user_id = utils.get_input_user(await client.get_input_entity(self.user_id))

    def to_dict(self):
        return {
            '_': 'IncrementStoryViewsRequest',
            'user_id': self.user_id.to_dict() if isinstance(self.user_id, TLObject) else self.user_id,
            'id': [] if self.id is None else self.id[:]
        }

    def _bytes(self):
        return b''.join((
            b'\'a\x12"',
            self.user_id._bytes(),
            b'\x15\xc4\xb5\x1c',struct.pack('<i', len(self.id)),b''.join(struct.pack('<i', x) for x in self.id),
        ))

    @classmethod
    def from_reader(cls, reader):
        _user_id = reader.tgread_object()
        reader.read_int()
        _id = []
        for _ in range(reader.read_int()):
            _x = reader.read_int()
            _id.append(_x)

        return cls(user_id=_user_id, id=_id)


class ReadStoriesRequest(TLRequest):
    CONSTRUCTOR_ID = 0xedc5105b
    SUBCLASS_OF_ID = 0x5026710f

    def __init__(self, user_id: 'TypeInputUser', max_id: int):
        """
        :returns Vector<int>: This type has no constructors.
        """
        self.user_id = user_id
        self.max_id = max_id

    async def resolve(self, client, utils):
        self.user_id = utils.get_input_user(await client.get_input_entity(self.user_id))

    def to_dict(self):
        return {
            '_': 'ReadStoriesRequest',
            'user_id': self.user_id.to_dict() if isinstance(self.user_id, TLObject) else self.user_id,
            'max_id': self.max_id
        }

    def _bytes(self):
        return b''.join((
            b'[\x10\xc5\xed',
            self.user_id._bytes(),
            struct.pack('<i', self.max_id),
        ))

    @classmethod
    def from_reader(cls, reader):
        _user_id = reader.tgread_object()
        _max_id = reader.read_int()
        return cls(user_id=_user_id, max_id=_max_id)

    @staticmethod
    def read_result(reader):
        reader.read_int()  # Vector ID
        return [reader.read_int() for _ in range(reader.read_int())]


class ReportRequest(TLRequest):
    CONSTRUCTOR_ID = 0xc95be06a
    SUBCLASS_OF_ID = 0xf5b399ac

    def __init__(self, user_id: 'TypeInputUser', id: List[int], reason: 'TypeReportReason', message: str):
        """
        :returns Bool: This type has no constructors.
        """
        self.user_id = user_id
        self.id = id
        self.reason = reason
        self.message = message

    async def resolve(self, client, utils):
        self.user_id = utils.get_input_user(await client.get_input_entity(self.user_id))

    def to_dict(self):
        return {
            '_': 'ReportRequest',
            'user_id': self.user_id.to_dict() if isinstance(self.user_id, TLObject) else self.user_id,
            'id': [] if self.id is None else self.id[:],
            'reason': self.reason.to_dict() if isinstance(self.reason, TLObject) else self.reason,
            'message': self.message
        }

    def _bytes(self):
        return b''.join((
            b'j\xe0[\xc9',
            self.user_id._bytes(),
            b'\x15\xc4\xb5\x1c',struct.pack('<i', len(self.id)),b''.join(struct.pack('<i', x) for x in self.id),
            self.reason._bytes(),
            self.serialize_bytes(self.message),
        ))

    @classmethod
    def from_reader(cls, reader):
        _user_id = reader.tgread_object()
        reader.read_int()
        _id = []
        for _ in range(reader.read_int()):
            _x = reader.read_int()
            _id.append(_x)

        _reason = reader.tgread_object()
        _message = reader.tgread_string()
        return cls(user_id=_user_id, id=_id, reason=_reason, message=_message)


class SendReactionRequest(TLRequest):
    CONSTRUCTOR_ID = 0x49aaa9b3
    SUBCLASS_OF_ID = 0x8af52aac

    def __init__(self, user_id: 'TypeInputUser', story_id: int, reaction: 'TypeReaction', add_to_recent: Optional[bool]=None):
        """
        :returns Updates: Instance of either UpdatesTooLong, UpdateShortMessage, UpdateShortChatMessage, UpdateShort, UpdatesCombined, Updates, UpdateShortSentMessage.
        """
        self.user_id = user_id
        self.story_id = story_id
        self.reaction = reaction
        self.add_to_recent = add_to_recent

    async def resolve(self, client, utils):
        self.user_id = utils.get_input_user(await client.get_input_entity(self.user_id))

    def to_dict(self):
        return {
            '_': 'SendReactionRequest',
            'user_id': self.user_id.to_dict() if isinstance(self.user_id, TLObject) else self.user_id,
            'story_id': self.story_id,
            'reaction': self.reaction.to_dict() if isinstance(self.reaction, TLObject) else self.reaction,
            'add_to_recent': self.add_to_recent
        }

    def _bytes(self):
        return b''.join((
            b'\xb3\xa9\xaaI',
            struct.pack('<I', (0 if self.add_to_recent is None or self.add_to_recent is False else 1)),
            self.user_id._bytes(),
            struct.pack('<i', self.story_id),
            self.reaction._bytes(),
        ))

    @classmethod
    def from_reader(cls, reader):
        flags = reader.read_int()

        _add_to_recent = bool(flags & 1)
        _user_id = reader.tgread_object()
        _story_id = reader.read_int()
        _reaction = reader.tgread_object()
        return cls(user_id=_user_id, story_id=_story_id, reaction=_reaction, add_to_recent=_add_to_recent)


class SendStoryRequest(TLRequest):
    CONSTRUCTOR_ID = 0xd455fcec
    SUBCLASS_OF_ID = 0x8af52aac

    def __init__(self, media: 'TypeInputMedia', privacy_rules: List['TypeInputPrivacyRule'], pinned: Optional[bool]=None, noforwards: Optional[bool]=None, media_areas: Optional[List['TypeMediaArea']]=None, caption: Optional[str]=None, entities: Optional[List['TypeMessageEntity']]=None, random_id: int=None, period: Optional[int]=None):
        """
        :returns Updates: Instance of either UpdatesTooLong, UpdateShortMessage, UpdateShortChatMessage, UpdateShort, UpdatesCombined, Updates, UpdateShortSentMessage.
        """
        self.media = media
        self.privacy_rules = privacy_rules
        self.pinned = pinned
        self.noforwards = noforwards
        self.media_areas = media_areas
        self.caption = caption
        self.entities = entities
        self.random_id = random_id if random_id is not None else int.from_bytes(os.urandom(8), 'big', signed=True)
        self.period = period

    async def resolve(self, client, utils):
        self.media = utils.get_input_media(self.media)

    def to_dict(self):
        return {
            '_': 'SendStoryRequest',
            'media': self.media.to_dict() if isinstance(self.media, TLObject) else self.media,
            'privacy_rules': [] if self.privacy_rules is None else [x.to_dict() if isinstance(x, TLObject) else x for x in self.privacy_rules],
            'pinned': self.pinned,
            'noforwards': self.noforwards,
            'media_areas': [] if self.media_areas is None else [x.to_dict() if isinstance(x, TLObject) else x for x in self.media_areas],
            'caption': self.caption,
            'entities': [] if self.entities is None else [x.to_dict() if isinstance(x, TLObject) else x for x in self.entities],
            'random_id': self.random_id,
            'period': self.period
        }

    def _bytes(self):
        return b''.join((
            b'\xec\xfcU\xd4',
            struct.pack('<I', (0 if self.pinned is None or self.pinned is False else 4) | (0 if self.noforwards is None or self.noforwards is False else 16) | (0 if self.media_areas is None or self.media_areas is False else 32) | (0 if self.caption is None or self.caption is False else 1) | (0 if self.entities is None or self.entities is False else 2) | (0 if self.period is None or self.period is False else 8)),
            self.media._bytes(),
            b'' if self.media_areas is None or self.media_areas is False else b''.join((b'\x15\xc4\xb5\x1c',struct.pack('<i', len(self.media_areas)),b''.join(x._bytes() for x in self.media_areas))),
            b'' if self.caption is None or self.caption is False else (self.serialize_bytes(self.caption)),
            b'' if self.entities is None or self.entities is False else b''.join((b'\x15\xc4\xb5\x1c',struct.pack('<i', len(self.entities)),b''.join(x._bytes() for x in self.entities))),
            b'\x15\xc4\xb5\x1c',struct.pack('<i', len(self.privacy_rules)),b''.join(x._bytes() for x in self.privacy_rules),
            struct.pack('<q', self.random_id),
            b'' if self.period is None or self.period is False else (struct.pack('<i', self.period)),
        ))

    @classmethod
    def from_reader(cls, reader):
        flags = reader.read_int()

        _pinned = bool(flags & 4)
        _noforwards = bool(flags & 16)
        _media = reader.tgread_object()
        if flags & 32:
            reader.read_int()
            _media_areas = []
            for _ in range(reader.read_int()):
                _x = reader.tgread_object()
                _media_areas.append(_x)

        else:
            _media_areas = None
        if flags & 1:
            _caption = reader.tgread_string()
        else:
            _caption = None
        if flags & 2:
            reader.read_int()
            _entities = []
            for _ in range(reader.read_int()):
                _x = reader.tgread_object()
                _entities.append(_x)

        else:
            _entities = None
        reader.read_int()
        _privacy_rules = []
        for _ in range(reader.read_int()):
            _x = reader.tgread_object()
            _privacy_rules.append(_x)

        _random_id = reader.read_long()
        if flags & 8:
            _period = reader.read_int()
        else:
            _period = None
        return cls(media=_media, privacy_rules=_privacy_rules, pinned=_pinned, noforwards=_noforwards, media_areas=_media_areas, caption=_caption, entities=_entities, random_id=_random_id, period=_period)


class ToggleAllStoriesHiddenRequest(TLRequest):
    CONSTRUCTOR_ID = 0x7c2557c4
    SUBCLASS_OF_ID = 0xf5b399ac

    def __init__(self, hidden: bool):
        """
        :returns Bool: This type has no constructors.
        """
        self.hidden = hidden

    def to_dict(self):
        return {
            '_': 'ToggleAllStoriesHiddenRequest',
            'hidden': self.hidden
        }

    def _bytes(self):
        return b''.join((
            b'\xc4W%|',
            b'\xb5ur\x99' if self.hidden else b'7\x97y\xbc',
        ))

    @classmethod
    def from_reader(cls, reader):
        _hidden = reader.tgread_bool()
        return cls(hidden=_hidden)


class TogglePinnedRequest(TLRequest):
    CONSTRUCTOR_ID = 0x51602944
    SUBCLASS_OF_ID = 0x5026710f

    def __init__(self, id: List[int], pinned: bool):
        """
        :returns Vector<int>: This type has no constructors.
        """
        self.id = id
        self.pinned = pinned

    def to_dict(self):
        return {
            '_': 'TogglePinnedRequest',
            'id': [] if self.id is None else self.id[:],
            'pinned': self.pinned
        }

    def _bytes(self):
        return b''.join((
            b'D)`Q',
            b'\x15\xc4\xb5\x1c',struct.pack('<i', len(self.id)),b''.join(struct.pack('<i', x) for x in self.id),
            b'\xb5ur\x99' if self.pinned else b'7\x97y\xbc',
        ))

    @classmethod
    def from_reader(cls, reader):
        reader.read_int()
        _id = []
        for _ in range(reader.read_int()):
            _x = reader.read_int()
            _id.append(_x)

        _pinned = reader.tgread_bool()
        return cls(id=_id, pinned=_pinned)

    @staticmethod
    def read_result(reader):
        reader.read_int()  # Vector ID
        return [reader.read_int() for _ in range(reader.read_int())]

