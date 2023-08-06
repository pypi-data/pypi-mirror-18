# pylint: disable=unused-argument
from shlex import split
from functools import partial
from gnusocial import timelines
from gnusocial import statuses as s
from .parsers import timeline, help_command, user_timeline, post_command
from .status import Status


def execute(input_string, config):
    cmd, *args = split(input_string)
    return commands[cmd](config, *args)


@help_command
def help_(config, command_names):
    if command_names:
        for command in command_names:
            commands[command](config, show_help=True)
    else:
        for command in sorted(commands):
            print(command)


def _print_statuses(statuses):
    for status in statuses:
        print(Status.from_status_dict(status))


@timeline('home', 'Fetch home timeline.')
def home(config, posts_number: int):
    statuses = timelines.home(
        server_url=config['server_url'], username=config['username'],
        password=config['password'], count=posts_number
    )
    _print_statuses(statuses)


@timeline('public', 'Fetch public timeline.')
def public(config, posts_number: int):
    statuses = timelines.public(
        server_url=config['server_url'], username=config['username'],
        password=config['password'], count=posts_number
    )
    _print_statuses(statuses)


@timeline('friends', 'Fetch friends timeline.')
def friends(config, posts_number: int):
    statuses = timelines.friends(
        server_url=config['server_url'], username=config['username'],
        password=config['password'], count=posts_number
    )
    _print_statuses(statuses)


@user_timeline('user', 'Fetch user timeline.')
def user(config, posts_number: int, username: str, user_id: int):
    options = {}
    if username:
        options = {'screen_name': username}
    elif user_id:
        options = {'user_id': user_id}
    statuses = timelines.user(
        server_url=config['server_url'], username=config['username'],
        password=config['password'], count=posts_number,
        **options
    )
    _print_statuses(statuses)


@timeline('replies', 'Fetch replies timeline.')
def replies(config, posts_number: int):
    statuses = timelines.replies(
        server_url=config['server_url'], username=config['username'],
        password=config['password'], count=posts_number
    )
    _print_statuses(statuses)


@post_command
def post(config, status_text, attachment, reply_to_status):
    _post = partial(
        s.update, server_url=config['server_url'], username=config['username'],
        password=config['password'], status=status_text, source='gscli',
    )
    args = {}
    if attachment:
        args['media'] = attachment
    if reply_to_status:
        args['in_reply_to_status_id'] = reply_to_status
    status = _post(**args)
    print(Status.from_status_dict(status))

help_strings = {
    'block': '''block <username>|-i <user_id>
    Block a user.''',

    'conversation': '''conversation <conversation_id>
    Show a conversation.''',

    'delete': '''delete <status_id>
    Delete a status.''',

    'favorite': '''favorite <status_id>
    Favorite a status.''',

    'favorites': '''favorites [-n posts_number]
    Fetch favorites timeline.''',

    'follow': '''follow <username>|-i <user_id>
    Follow the user.''',

    'followers': '''followers [username|-i user_id]
    Show your or another user's followers.''',

    'following': '''following [username|-i user_id]
    Show users who you or another user are following.''',

    'group': '''group <groupname>|-i <group_id>\
    Fetch group timeline.''',

    'groups': '''groups [username|-i user_id]
    Show groups which you or another user are members of.''',

    'join': '''join <groupname>|-i <group_id>
    Join a group.''',

    'leave': '''leave <groupname>|-i <group_id>
    Leave a group.''',

    'members': '''members <groupname>|-i <group_id>
    Show users who are the members of the group.''',

    'post': '''post <status_text> [-a file] [-r status_id]
    Post status.
    Optional arguments:
        -a file \t attach a file
        -r status_id \t status to reply to''',

    'repeat': '''repeat <status_id>
    Repeat a status.''',

    'search': '''search <query>
    Search statuses matching the query.''',

    'status': '''status <status_id>
    Show the status details.''',

    'unblock': '''unblock <username>|-i <user_id>
    Unblock a user.''',

    'unfollow': '''unfollow <username>|-i <user_id>
    Unfollow the user.''',

    'upload': '''upload <file> [files]
    Upload files to the server.''',

}

commands = {
    # 'block': '',
    # 'conversation': '',
    # 'delete': '',
    # 'favorite': '',
    # 'favorites': '',
    # 'follow': '',
    # 'followers': '',
    # 'following': '',
    'friends': friends,
    # 'group': '',
    # 'groups': '',
    'help': help_,
    'home': home,
    # 'join': '',
    # 'leave': '',
    # 'members': '',
    'post': post,
    'public': public,
    # 'repeat': '',
    'replies': replies,
    # 'search': '',
    # 'status': '',
    # 'unblock': '',
    # 'unfollow': '',
    # 'upload': '',
    'user': user
}
