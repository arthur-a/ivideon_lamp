from .management import BaseCommand
from .lamp import get_lamp


class CommandOn(BaseCommand):
    type = 0x12

    def run(self):
        lamp = get_lamp()
        lamp.on()


class CommandOff(BaseCommand):
    type = 0x13

    def run(self):
        lamp = get_lamp()
        lamp.off()


class CommandColor(BaseCommand):
    type = 0x20

    def run(self):
        if self.value is not None:
            lamp = get_lamp()
            lamp.set_color(self.value)


# Add your commands here just subclass from BaseCommand class, set 'type' value 
# and override 'run' method.


if __name__ == '__main__':
    cmd_on = CommandOn()
    cmd_on.run()

    cmd_off = CommandOff()
    cmd_off.run()

    cmd_color = CommandColor((0,0,0,),)
    cmd_color.run()
