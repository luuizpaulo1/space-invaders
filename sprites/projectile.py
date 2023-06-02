from PPlay.sprite import Sprite
from PPlay.window import Window


class Projectile(Sprite):
    def __init__(self, window: Window, velocity: int = 500):
        super().__init__("./assets/projectile.png")
        self.velocity = velocity
        self.window = window

    def update(self):
        self.y -= self.velocity * self.window.delta_time()
