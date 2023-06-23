from PPlay.sprite import Sprite


class Enemy(Sprite):
    def __init__(self, space_invaders, velocity: int = 50, health=5):
        super().__init__("./assets/enemy.png")
        self.space_invaders = space_invaders
        self.velocity = velocity
        self.health = health

    @property
    def is_touching_the_left_wall(self):
        return self.x < 0

    @property
    def is_touching_the_right_wall(self):
        return self.x > (self.space_invaders.window.width - self.width)

    @property
    def is_touching_the_ship(self):
        return self.y + self.height >= self.space_invaders.ship.y

    def move(self):
        self.x += self.velocity * self.space_invaders.window.delta_time()
