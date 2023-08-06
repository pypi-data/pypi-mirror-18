from prompt_toolkit.validation import ValidationError, Validator
from gnusocial.utils import DOMAIN_REGEX
from . import commands


class CommandValidator(Validator):
    def validate(self, document):
        cmd, *args = commands.split(document.text)
        if cmd not in commands.commands:
            raise ValidationError(message='Unknown command: \'%s\'' % cmd)
        else:
            if hasattr(self, cmd):
                self.__getattribute__(cmd)(args, document)

    @staticmethod
    def help(args, document):
        for arg in args:
            if arg not in commands.commands:
                i = document.text.find(arg)
                raise ValidationError(i, 'help: Unknown command: \'%s\'' % arg)


class URLValidator(Validator):
    def validate(self, document):
        if not DOMAIN_REGEX.match(document.text):
            raise ValidationError(message='Invalid server URL')
