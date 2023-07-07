from datetime import datetime, timedelta

from PPlay.keyboard import Keyboard
from PPlay.sprite import Sprite
from PPlay.window import Window
from sprites.projectile import Projectile


class Ship(Sprite):
    def __init__(self, space_invaders, shoot_cadence: int = 60):
        super().__init__("./assets/ship.png")
        self.velocity = 500
        self.window = space_invaders.window
        self.keyboard = space_invaders.keyboard
        self.last_shoot = None
        self.shoot_cadence = shoot_cadence  # shoots per minute
        self.lives = 3
        self.is_invincible = False
        self.last_invincible_time = None
        self.invincible_time = 2
        self.blink_duration = 10**5
        self.last_blink = None
        self.show = True

    def centralize(self):
        self.set_position((self.window.width / 2) - (self.width / 2), self.window.height * 7 / 8)

    def shoot(self):
        now = datetime.now()
        elapsed_since_last_shoot = None
        if self.last_shoot:
            elapsed_since_last_shoot = now - self.last_shoot

        minimum_timedelta = timedelta(
            seconds=int(60 / self.shoot_cadence),
            microseconds=60 / self.shoot_cadence % 1 * 10 ** 6
        )

        if not self.last_shoot or elapsed_since_last_shoot > minimum_timedelta:
            projectile = Projectile(self)
            projectile.x = self.x + self.width / 2 - projectile.width / 2
            projectile.y = self.y - 20
            self.last_shoot = now
            return projectile

    def set_invincible(self):
        now = datetime.now()
        self.is_invincible = True
        self.last_invincible_time = now
        self.last_blink = now
        self.show = False

    def expire_invincibility(self):
        if self.last_invincible_time:
            self.is_invincible = not (datetime.now() - self.last_invincible_time).seconds > self.invincible_time
        if not self.is_invincible:
            self.show = True

    def blink(self):
        now = datetime.now()
        if (now - self.last_blink).microseconds >= self.blink_duration:
            self.show = not self.show
            self.last_blink = now

    def action(self):
        if self.keyboard.key_pressed("LEFT") and self.x > 0:
            self.x -= self.velocity * self.window.delta_time()
        elif self.keyboard.key_pressed("RIGHT") and self.x < (self.window.width - self.width):
            self.x += self.velocity * self.window.delta_time()
        if self.keyboard.key_pressed("SPACE"):
            return self.shoot()
        self.expire_invincibility()
        if self.is_invincible:
            self.blink()


