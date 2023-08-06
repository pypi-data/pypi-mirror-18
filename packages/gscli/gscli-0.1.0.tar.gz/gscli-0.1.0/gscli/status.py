TEMPLATE = """{author_name} @{author_handle}{reply_block} {created_at}
id: {status_id}
{content}
"""


def _serialize_status(item: dict) -> dict:
    return {
        'status_id': int(item['id']),
        'content': item['text'],
        'author_name': item['user']['name'],
        'author_handle': item['user']['screen_name'],
        'created_at': item['created_at'],
        'conversation_id': item.get('statusnet_conversation_id'),
        'in_reply_to_status_id': item.get('in_reply_to_status_id'),
        'in_reply_to_screen_name': item.get('in_reply_to_screen_name')
    }


class Status:
    @classmethod
    def from_status_dict(cls, status_dict):
        instance = cls.__new__(cls)
        instance.__init__(**_serialize_status(status_dict))
        return instance

    def __init__(self, status_id: int, content: str, author_name: str,
                 author_handle: str, created_at: str,
                 conversation_id: int=None, in_reply_to_status_id: str=None,
                 in_reply_to_screen_name: str=None
                ) -> None:
        self.status_id = status_id
        self.content = content
        self.author_name = author_name
        self.author_handle = author_handle
        self.created_at = created_at
        self.in_reply_to_status_id = in_reply_to_status_id
        self.in_reply_to_screen_name = in_reply_to_screen_name
        self.conversation_id = conversation_id

    def __repr__(self) -> str:
        template = ('Status(status_id=%d, content="%s", ' +
                    'author_name="%s", author_handle="%s", ' +
                    'created_at="%s"')
        template %= (self.status_id, self.content, self.author_name,
                     self.author_handle, self.created_at)
        if self.conversation_id:
            template += ', conversation_id=%d' % self.conversation_id
        if self.in_reply_to_status_id and self.in_reply_to_screen_name:
            template += ((', in_reply_to_status_id=%s,' +
                          ' in_reply_to_screen_name=%s') %
                         (self.in_reply_to_status_id,
                          self.in_reply_to_screen_name))
        return template + ')'

    def __str__(self) -> str:
        reply_block = ''
        if self.in_reply_to_screen_name and self.in_reply_to_status_id:
            reply_block = ' > @%s (id: %s)' % (self.in_reply_to_screen_name,
                                               self.in_reply_to_status_id)
        return TEMPLATE.format(
            author_name=self.author_name, author_handle=self.author_handle,
            created_at=self.created_at, status_id=self.status_id,
            content=self.content, reply_block=reply_block
        )
