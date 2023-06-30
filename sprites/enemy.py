from datetime import datetime, timedelta
from typing import Optional

from PPlay.sprite import Sprite
from sprites.enemy_projectile import EnemyProjectile


class Enemy(Sprite):
    def __init__(self, space_invaders, velocity: int = 250, health=1, shoot_reload_time: int = 5):
        super().__init__("./assets/enemy.png")
        self.space_invaders = space_invaders
        self.velocity = velocity
        self.health = health
        self.last_shoot = datetime.now()
        self.shoot_reload_time = shoot_reload_time

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

    def shoot(self) -> Optional[EnemyProjectile]:
        now = datetime.now()
        elapsed_since_last_shoot = now - self.last_shoot

        minimum_timedelta = timedelta(seconds=self.shoot_reload_time)

        if not self.last_shoot or elapsed_since_last_shoot > minimum_timedelta:
            projectile = EnemyProjectile(self.space_invaders)
            projectile.x = self.x + self.width / 2 - projectile.width / 2
            projectile.y = self.y - 20
            self.last_shoot = now
            return projectile

    def action(self) -> Optional[EnemyProjectile]:
        self.move()
        enemy_projectile = self.shoot()
        return enemy_projectile
