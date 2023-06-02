from datetime import datetime, timedelta

from PPlay.keyboard import Keyboard
from PPlay.sprite import Sprite
from PPlay.window import Window
from sprites.projectile import Projectile


class Ship(Sprite):
    def __init__(self, window: Window, keyboard: Keyboard, shoot_cadence: int = 60):
        super().__init__("./assets/ship.png")
        self.velocity = 500
        self.window = window
        self.keyboard = keyboard
        self.last_shoot = None
        self.shoot_cadence = shoot_cadence  # shoots per minute

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
            projectile = Projectile(window=self.window)
            projectile.x = self.x + self.width / 2 - projectile.width / 2
            projectile.y = self.y - 20
            self.last_shoot = now
            return projectile

    def action(self):
        if self.keyboard.key_pressed("LEFT") and self.x > 0:
            self.x -= self.velocity * self.window.delta_time()
        elif self.keyboard.key_pressed("RIGHT") and self.x < (self.window.width - self.width):
            self.x += self.velocity * self.window.delta_time()
        if self.keyboard.key_pressed("SPACE"):
            return self.shoot()

    def draw(self):
        super().draw()
