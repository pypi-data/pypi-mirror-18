from gettext import bindtextdomain, textdomain, gettext, ngettext
import os
_domain = 'messages'
_localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
bindtextdomain(_domain, _localedir)
textdomain(_domain)
_ = gettext


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
