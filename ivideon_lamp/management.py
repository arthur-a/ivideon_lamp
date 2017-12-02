derived_classes = []


def get_commands():
    return derived_classes


class CommandMeta(type):
    def __init__(cls, name, bases, vars):
        if name != 'BaseCommand':
            derived_classes.append(cls)
        super(CommandMeta, cls).__init__(name, bases, vars)


class BaseCommand(metaclass=CommandMeta):
    type = None

    def __init__(self, value=None):
        self.value = value

    def run(self):
        raise NotImplementedError


# Import here after BaseCommand was initalized
from . import commands