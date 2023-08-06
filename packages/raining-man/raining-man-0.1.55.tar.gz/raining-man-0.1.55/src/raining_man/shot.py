from FGAme import *
from .core import Physics, Media

class Shot(Circle):
    def __init__(self, pos=(400, 650)):
        super().__init__(radius=50,mass=10000, pos=pos, vel=(0, 100), 
                         color='brown')
        self.body = world.add(self)
        self.body_pygame = Media.change_image('images/stone.png')
        self.k = 1.05

    def update(self):
        drag_result = Physics.drag(self)
        self.vel, self.pos = drag_result
