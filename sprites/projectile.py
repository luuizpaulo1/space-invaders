from PPlay.sprite import Sprite
from PPlay.window import Window


class Projectile(Sprite):
    def __init__(self, space_invaders, velocity: int = 500):
        super().__init__("./assets/projectile.png")
        self.velocity = velocity
        self.window = space_invaders.window

    def action(self):
        self.y -= self.velocity * self.window.delta_time()
