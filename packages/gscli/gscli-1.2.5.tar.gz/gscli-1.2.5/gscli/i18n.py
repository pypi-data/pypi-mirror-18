from gettext import bindtextdomain, textdomain, gettext, ngettext
import os
from locale import setlocale, LC_ALL
from datetime import datetime
from tzlocal import get_localzone
_domain = 'messages'
_localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
bindtextdomain(_domain, _localedir)
textdomain(_domain)
_ = gettext


def translate_created_at(created_at):
    locale = setlocale(LC_ALL)
    fmt = '%a %b %d %H:%M:%S %z %Y'
    setlocale(LC_ALL, 'C')
    created_at = datetime.strptime(created_at, fmt)
    setlocale(LC_ALL, locale)
    tz = get_localzone()
    created_at = created_at.astimezone(tz)
    return created_at.strftime('%c')


def __translate_standard_messages():
    """Argparse strings"""
    _('%(prog)s: error: %(message)s\n')
    _('expected one argument')
    _('invalid choice: %(value)r (choose from %(choices)s)')
    _('not allowed with argument %s')
    _('optional arguments')
    _('positional arguments')
    _('show this help message and exit')
    _('usage: ')
