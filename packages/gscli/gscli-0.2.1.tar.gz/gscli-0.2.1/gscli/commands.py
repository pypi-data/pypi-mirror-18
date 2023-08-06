# pylint: disable=unused-argument
from shlex import split
from functools import partial
from gnusocial import timelines, favorites
from gnusocial import statuses as s
from .parsers import (timeline, help_command, user_timeline, post_command,
                      conversation_timeline, status_command)
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


@conversation_timeline
def conversation(config, posts_number: int, conversation_id: int):
    statuses = timelines.replies(
        server_url=config['server_url'], username=config['username'],
        password=config['password'], count=posts_number,
        conversation_id=conversation_id
    )
    _print_statuses(statuses)


@status_command('delete', 'Delete a status.')
def delete(config, status_id: int):
    status = s.destroy(
        server_url=config['server_url'], username=config['username'],
        password=config['password'], status_id=status_id
    )
    print(Status.from_status_dict(status))


@status_command('status', 'Show the status details.')
def status_(config, status_id: int):
    status = s.show(
        server_url=config['server_url'], username=config['username'],
        password=config['password'], status_id=status_id
    )
    print(Status.from_status_dict(status).detailed)


@status_command('status', 'Repeat a status.')
def repeat(config, status_id: int):
    status = s.repeat(
        server_url=config['server_url'], username=config['username'],
        password=config['password'], status_id=status_id
    )
    print(Status.from_status_dict(status))


@status_command('favorite', 'Favorite a status.')
def favorite(config, status_id: int):
    status = favorites.create(
        server_url=config['server_url'], username=config['username'],
        password=config['password'], status_id=status_id
    )
    print(Status.from_status_dict(status))


@status_command('favorite', 'Favorite a status.')
def unfavorite(config, status_id: int):
    status = favorites.destroy(
        server_url=config['server_url'], username=config['username'],
        password=config['password'], status_id=status_id
    )
    print(Status.from_status_dict(status))


@user_timeline('favorites', 'Fetch favorites timeline.')
def favorites_(config, posts_number: int, username: str, user_id: int):
    options = {}
    if username:
        options = {'screen_name': username}
    elif user_id:
        options = {'user_id': user_id}
    statuses = favorites.favorites(
        server_url=config['server_url'], username=config['username'],
        password=config['password'], count=posts_number, **options
    )
    _print_statuses(statuses)

help_strings = {
    'block': '''block <username>|-i <user_id>
    Block a user.''',

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

    'search': '''search <query>
    Search statuses matching the query.''',

    'unblock': '''unblock <username>|-i <user_id>
    Unblock a user.''',

    'unfollow': '''unfollow <username>|-i <user_id>
    Unfollow the user.''',

    'upload': '''upload <file> [files]
    Upload files to the server.''',

}

commands = {
    # 'block': '',
    'conversation': conversation,
    'delete': delete,
    'favorite': favorite,
    'unfavorite': unfavorite,
    'favorites': favorites_,
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
    'repeat': repeat,
    'replies': replies,
    # 'search': '',
    'status': status_,
    # 'unblock': '',
    # 'unfollow': '',
    # 'upload': '',
    'user': user
}
