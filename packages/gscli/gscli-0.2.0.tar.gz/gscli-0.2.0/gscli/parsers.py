from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from functools import wraps


def timeline(command_name: str, description: str):
    def decorator(f):
        @wraps(f)
        def wrapper(config, *args, **kwargs):
            parser = _make_timeline_parser(command_name, description)
            if 'show_help' in kwargs and kwargs.pop('show_help'):
                parser.print_help()
            else:
                f_args = parser.parse_args(args)
                f(config, posts_number=f_args.posts_number)
        return wrapper
    return decorator


def help_command(f):
    desc = 'Show all available commands or info about specified commands.'

    @wraps(f)
    def wrapper(config, *args, **kwargs):
        parser = ArgumentParser('help', description=desc, add_help=False)
        parser.add_argument('commands', nargs='*')
        if 'show_help' in kwargs and kwargs.pop('show_help'):
            parser.print_help()
        else:
            f_args = parser.parse_args(args)
            f(config, f_args.commands)
    return wrapper


def post_command(f):
    desc = 'Post a status.'

    @wraps(f)
    def wrapper(config, *args, **kwargs):
        parser = ArgumentParser('post', description=desc, add_help=False)
        parser.add_argument('status_text', help='text of the status to post')
        parser.add_argument('-a', '--attachment', help='a file to attach',
                            metavar='FILE')
        parser.add_argument('-r', '--reply-to-status', type=int,
                            metavar='STATUS_ID',
                            help='ID of the status to reply to')
        if 'show_help' in kwargs and kwargs.pop('show_help'):
            parser.print_help()
        else:
            f_args = parser.parse_args(args)
            f(config, f_args.status_text, f_args.attachment, f_args.reply_to_status)
    return wrapper


def user_timeline(command_name: str, description: str):
    def decorator(f):
        @wraps(f)
        def wrapper(config, *args, **kwargs):
            parser = _make_user_timeline_parser(command_name, description)
            if 'show_help' in kwargs and kwargs.pop('show_help'):
                parser.print_help()
            else:
                f_args = parser.parse_args(args)
                f(config, posts_number=f_args.posts_number,
                  username=f_args.username, user_id=f_args.user_id)
        return wrapper
    return decorator


def conversation_timeline(f):
    @wraps(f)
    def wrapper(config, *args, **kwargs):
        parser = _make_conversation_timeline_parser(
            'conversation', 'Show a conversation.'
        )
        if 'show_help' in kwargs and kwargs.pop('show_help'):
            parser.print_help()
        else:
            f_args = parser.parse_args(args)
            f(config, posts_number=f_args.posts_number,
              conversation_id=f_args.conversation_id)
    return wrapper


def status_command(command_name: str, description: str):
    def decorator(f):
        @wraps(f)
        def wrapper(config, *args, **kwargs):
            parser = _make_status_parser(command_name, description)
            if 'show_help' in kwargs and kwargs.pop('show_help'):
                parser.print_help()
            else:
                f_args = parser.parse_args(args)
                f(config, status_id=f_args.status_id)
        return wrapper
    return decorator


def _add_username_and_id(parser: ArgumentParser, username_description: str,
                         user_id_description):
    parser.add_argument('-u', '--username', help=username_description)
    parser.add_argument('-i', '--user-id', help=user_id_description, type=int)


def _add_conversation_id(parser: ArgumentParser, description: str):
    parser.add_argument('conversation_id', help=description, type=int)


def _make_timeline_parser(command_name: str, description: str):
    parser = ArgumentParser(prog=command_name, description=description,
                            formatter_class=ArgumentDefaultsHelpFormatter,
                            add_help=False)
    parser.add_argument(
        '-n', '--posts_number', default=20, type=int,
        help='Number of posts to fetch'
    )
    return parser


def _make_user_timeline_parser(command_name: str, description: str):
    parser = _make_timeline_parser(command_name, description)
    _add_username_and_id(
        parser, username_description='Name of the target user',
        user_id_description='ID of the target user'
    )
    return parser


def _make_conversation_timeline_parser(command_name: str, description: str):
    parser = _make_timeline_parser(command_name, description)
    _add_conversation_id(parser, description='ID of the conversation to show')
    return parser


def _make_status_parser(command_name, description: str):
    parser = ArgumentParser(prog=command_name, description=description,
                            formatter_class=ArgumentDefaultsHelpFormatter,
                            add_help=False)
    parser.add_argument('status_id', type=int, help='ID of the target status')
    return parser
