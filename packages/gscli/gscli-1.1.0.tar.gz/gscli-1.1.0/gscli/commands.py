# pylint: disable=unused-argument
from shlex import split
from functools import partial
from gnusocial import (timelines, favorites, friendships, users, blocks, media,
                       groups, search)
from gnusocial import statuses as s
from .group import Group
from .parsers import (timeline, help_command, user_timeline, post_command,
                      conversation_timeline, status_command, user_command,
                      group_timeline, group_command, upload_command,
                      search_command)
from .status import Status
from .user import User


def execute(input_string, config, no_split=False):
    if no_split is False:
        cmd, *args = split(input_string)
    else:
        cmd = input_string[0]
        args = input_string[1:]
    return commands[cmd](config, *args)


def _user_options(username: str, user_id: int):
    options = {}
    if username:
        options = {'screen_name': username}
    elif user_id:
        options = {'user_id': user_id}
    return options


def _print_users(user_dicts: list):
    for user_dict in user_dicts:
        print(User.from_user_dict(user_dict))


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
def home(config, count: int):
    statuses = timelines.home(
        server_url=config['server_url'], username=config['username'],
        password=config['password'], count=count
    )
    _print_statuses(statuses)


@timeline('public', 'Fetch public timeline.')
def public(config, count: int):
    statuses = timelines.public(
        server_url=config['server_url'], username=config['username'],
        password=config['password'], count=count
    )
    _print_statuses(statuses)


@timeline('friends', 'Fetch friends timeline.')
def friends(config, count: int):
    statuses = timelines.friends(
        server_url=config['server_url'], username=config['username'],
        password=config['password'], count=count
    )
    _print_statuses(statuses)


@user_timeline('user', 'Fetch user timeline.')
def user(config, count: int, username: str, user_id: int):
    statuses = timelines.user(
        server_url=config['server_url'], username=config['username'],
        password=config['password'], count=count,
        **_user_options(username, user_id)
    )
    _print_statuses(statuses)


@timeline('replies', 'Fetch replies timeline.')
def replies(config, count: int):
    statuses = timelines.replies(
        server_url=config['server_url'], username=config['username'],
        password=config['password'], count=count
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
def conversation(config, count: int, conversation_id: int):
    statuses = timelines.replies(
        server_url=config['server_url'], username=config['username'],
        password=config['password'], count=count,
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
def favorites_(config, count: int, username: str, user_id: int):
    statuses = favorites.favorites(
        server_url=config['server_url'], username=config['username'],
        password=config['password'], count=count,
        **_user_options(username, user_id)
    )
    _print_statuses(statuses)


@user_command('follow', 'Follow the user.')
def follow(config, username: str, user_id: int):
    user_dict = friendships.create(
        server_url=config['server_url'], username=config['username'],
        password=config['password'], **_user_options(username, user_id)
    )
    print('You have followed %s(@%s).' % (user_dict['name'],
                                          user_dict['screen_name']))


@user_command('unfollow', 'Unfollow the user.')
def unfollow(config, username: str, user_id: int):
    user_dict = friendships.destroy(
        server_url=config['server_url'], username=config['username'],
        password=config['password'], **_user_options(username, user_id)
    )
    print('You have unfollowed %s(@%s).' % (user_dict['name'],
                                            user_dict['screen_name']))


@user_timeline('followers', 'Show your or specified user\'s followers.')
def followers(config, username: str, user_id: int, count: int):
    user_dicts = users.followers(
        server_url=config['server_url'], username=config['username'],
        password=config['password'], count=count,
        **_user_options(username, user_id)
    )
    _print_users(user_dicts)


@user_timeline('following',
               'Show users who you or specified user are following.')
def following(config, username: str, user_id: int, count: int):
    user_dicts = users.followers(
        server_url=config['server_url'], username=config['username'],
        password=config['password'], count=count,
        **_user_options(username, user_id)
    )
    _print_users(user_dicts)


@user_command('block', 'Block a user.')
def block(config, username: str, user_id: int):
    user_dict = blocks.create(
        server_url=config['server_url'], username=config['username'],
        password=config['password'], **_user_options(username, user_id)
    )
    print('You have blocked %s(@%s).' % (user_dict['name'],
                                         user_dict['screen_name']))


@user_command('unblock', 'Unblock a user.')
def unblock(config, username: str, user_id: int):
    user_dict = blocks.destroy(
        server_url=config['server_url'], username=config['username'],
        password=config['password'], **_user_options(username, user_id)
    )
    print('You have unblocked %s(@%s).' % (user_dict['name'],
                                           user_dict['screen_name']))


def _print_groups(group_dicts: list):
    for group_dict in group_dicts:
        print(Group.from_group_dict(group_dict))


@user_command('groups',
              'Show groups which you or specified user are members of.')
def groups_(config, username: str, user_id: int):
    group_dicts = groups.user_groups(
        server_url=config['server_url'], username=config['username'],
        password=config['password'], **_user_options(username, user_id)
    )
    _print_groups(group_dicts)


def _group_options(group_name: str, group_id: int) -> dict:
    options = {}
    if group_name:
        options['nickname'] = group_name
    if group_id:
        options['id'] = group_id
    return options


@group_timeline('members', 'Show users who are the members of the group.')
def members(config, group_id: int, group_name: str, count: int):
    user_dicts = groups.members(
        server_url=config['server_url'], username=config['username'],
        password=config['password'], count=count,
        **_group_options(group_name, group_id)
    )
    _print_users(user_dicts)


@group_timeline('group', 'Fetch group timeline.')
def group(config, group_id: int, group_name: str, count: int):
    status_dicts = groups.timeline(
        server_url=config['server_url'], username=config['username'],
        password=config['password'], count=count,
        **_group_options(group_name, group_id)
    )
    _print_statuses(status_dicts)


@group_command('join', 'Join a group.')
def join(config, group_id: int, group_name: str):
    group_dict = groups.join(
        server_url=config['server_url'], username=config['username'],
        password=config['password'], **_group_options(group_name, group_id)
    )
    print('You have joined %s(@%s).' % (group_dict['fullname'],
                                        group_dict['nickname']))


@group_command('leave', 'Leave a group.')
def leave(config, group_id: int, group_name: str):
    group_dict = groups.leave(
        server_url=config['server_url'], username=config['username'],
        password=config['password'], **_group_options(group_name, group_id)
    )
    print('You have left %s(@%s).' % (group_dict['fullname'],
                                      group_dict['nickname']))


@upload_command
def upload(config, files: list):
    for f in files:
        _, link = media.upload(
            server_url=config['server_url'], username=config['username'],
            password=config['password'], filename=f
        )
        print('%s: %s' % (f, link))


@search_command
def search_(config, query: str, page: int, rpp: int):
    status_dicts = search.search(
        server_url=config['server_url'], username=config['username'],
        password=config['password'], query=query, page=page, rpp=rpp
    )
    _print_statuses(status_dicts)


commands = {
    'block': block,
    'conversation': conversation,
    'delete': delete,
    'favorite': favorite,
    'unfavorite': unfavorite,
    'favorites': favorites_,
    'follow': follow,
    'followers': followers,
    'following': following,
    'friends': friends,
    'group': group,
    'groups': groups_,
    'help': help_,
    'home': home,
    'join': join,
    'leave': leave,
    'members': members,
    'post': post,
    'public': public,
    'repeat': repeat,
    'replies': replies,
    'search': search_,
    'status': status_,
    'unblock': unblock,
    'unfollow': unfollow,
    'upload': upload,
    'user': user
}
