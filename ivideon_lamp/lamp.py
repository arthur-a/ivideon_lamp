from ivideon_lamp import ascii_art


class Lamp:
    color = 0xFFFFFF  # RGB

    def __init__(self):
        self.is_on = False

    def on(self):
        if self.is_on:
            print('The lamp already is on')
        else:
            self.is_on = True
            print('Switch on the lamp')
            print(ascii_art.ON)

    def off(self):
        if self.is_on:
            self.is_on = False
            print('Switch off the lamp')
            print(ascii_art.OFF)
        else:
            print('The lamp already is off')


    def set_color(self, color):
        self.color = color
        print('New color of the lamp is %s' % (color,))


_lamp = None
def get_lamp():
    global _lamp
    if _lamp is None:
        _lamp = Lamp()
    return _lamp
