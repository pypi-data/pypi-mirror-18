from FGAme import *
from raining_man.images import *
from .core import Media

class Boy(AABB):
    def __init__(self):
        super().__init__(shape=(30, 30), pos=(400, 100), mass=500)
        self.body_pygame = Media.change_image('images/1.png')
        self.rectangle = [0, 0, 60, 60]
        self.position = [400, 100]
        self.k = 1.05

    def update(self):
        pass

    def move_p1(self, dx):
        self.position = [self.position[0] + dx, 100]
        self.pos = self.position
