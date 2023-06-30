import itertools
from datetime import datetime
from random import randint

from PPlay.gameimage import GameImage
from PPlay.keyboard import Keyboard
from PPlay.mouse import Mouse
from PPlay.window import Window
from sprites.enemy import Enemy
from sprites.ship import Ship


class SpaceInvaders:
    def __init__(self, window: Window, mouse: Mouse, keyboard: Keyboard):
        self.window = window
        self.mouse = mouse
        self.keyboard = keyboard
        self.background = GameImage("./assets/background.png")
        self.ship = Ship(self, shoot_cadence=1000)

        self.ship.centralize()

        self.finish = False
        self.game_over = False
        self.win = False

        self.projectiles = []
        self.enemy_projectiles = []

        self.n_rows_enemies = 3
        self.n_columns_enemies = 5
        self.enemy_dummy = Enemy(self)
        self.enemies = self.create_enemies(self.n_rows_enemies, self.n_columns_enemies)

        self.fps_counter = 0
        self.fps_display = 0
        self.fps_last_count = datetime.now()

        self.score = 0

    @property
    def enemies_1d(self):
        return list(itertools.chain.from_iterable(self.enemies))

    def expire_projectiles(self):
        x_limits = (
            min(enemy.x for enemy in self.enemies_1d),
            max(enemy.x for enemy in self.enemies_1d) + self.enemy_dummy.width
        )
        y_limits = (
            min(enemy.y for enemy in self.enemies_1d),
            max(enemy.y for enemy in self.enemies_1d) + self.enemy_dummy.height
        )

        for index_projectile in range(len(self.projectiles) - 1, -1, -1):
            projectile = self.projectiles[index_projectile]
            if x_limits[0] < projectile.x < x_limits[1] and y_limits[0] < projectile.y < y_limits[1]:
                next_projectile = False
                for index_enemy in range(len(list(self.enemies_1d)) - 1, -1, -1):
                    enemy = self.enemies_1d[index_enemy]
                    if projectile.collided(enemy):
                        self.projectiles.pop(index_projectile)
                        enemy.health -= 1
                        next_projectile = True
                        break

                if next_projectile:
                    continue

            if self.projectiles[index_projectile].y < 0:
                self.projectiles.pop(index_projectile)

    def expire_enemy_projectiles(self):
        for index_projectile in range(len(self.enemy_projectiles) - 1, -1, -1):
            enemy_projectile = self.enemy_projectiles[index_projectile]
            next_projectile = False
            if not self.ship.is_invincible:
                for index_enemy in range(len(list(self.enemies_1d)) - 1, -1, -1):
                    if enemy_projectile.collided(self.ship):
                        self.enemy_projectiles.pop(index_projectile)
                        self.ship.lives -= 1
                        self.ship.set_invincible()
                        self.ship.centralize()
                        next_projectile = True
                        break

            if next_projectile:
                continue

            if self.enemy_projectiles[index_projectile].y > self.window.height:
                self.enemy_projectiles.pop(index_projectile)

    def expire_enemies(self):
        for i in range(len(self.enemies) - 1, -1, -1):
            for j in range(len(self.enemies[i]) - 1, -1, -1):
                if self.enemies[i][j].health <= 0:
                    self.enemies[i].pop(j)
                    self.score += 50 * (self.n_rows_enemies - i)
            if not self.enemies[i]:
                self.enemies.pop(i)

    def create_enemies(self, n_rows: int, n_columns: int):
        enemy_width = self.enemy_dummy.width
        enemy_height = self.enemy_dummy.height

        spacing_width = enemy_width * 1.5
        spacing_height = enemy_height * 1.5

        enemies = []
        enemy_y = 0
        for i in range(n_rows):
            enemy_x = 1
            row = []
            for j in range(n_columns):
                shoot_reload_time = randint(2, 5)
                new_enemy = Enemy(self, shoot_reload_time=shoot_reload_time)
                new_enemy.set_position(enemy_x, enemy_y)
                row.append(new_enemy)
                enemy_x += spacing_width
            enemies.append(row)
            enemy_y += spacing_height
        return enemies

    def count_fps(self):
        self.fps_counter += 1

        if (datetime.now() - self.fps_last_count).microseconds >= 500*1000:
            self.fps_display = self.fps_counter * 2
            self.fps_counter = 0
            self.fps_last_count = datetime.now()

    def show_fps(self):
        self.window.draw_text(str(self.fps_display), size=20, x=0, y=0)

    def show_score(self):
        self.window.draw_text(f"SCORE: {str(self.score)}", color="red", size=20, x=self.window.width - 130, y=0)

    def show_lives(self):
        self.window.draw_text(f"LIVES: {str(self.ship.lives)}", color="red", size=20, x=self.window.width - 100, y=self.window.height - 40)

    def loop(self):
        if self.win or self.game_over:
            return

        self.count_fps()

        projectile = self.ship.action()
        if projectile:
            self.projectiles.append(projectile)

        self.expire_projectiles()
        self.expire_enemy_projectiles()
        self.expire_enemies()

        self.background.draw()
        if self.ship.show:
            self.ship.draw()

        for projectile in self.projectiles:
            projectile.action()
            projectile.draw()

        for enemy_projectile in self.enemy_projectiles:
            enemy_projectile.action()
            enemy_projectile.draw()

        for enemy in self.enemies_1d:
            enemy_projectile = enemy.action()
            if enemy_projectile:
                self.enemy_projectiles.append(enemy_projectile)
            enemy.draw()

        if any([enemy.is_touching_the_left_wall for enemy in self.enemies_1d]):
            for enemy in self.enemies_1d:
                enemy.y += enemy.height
                enemy.velocity = abs(enemy.velocity)

        if any([enemy.is_touching_the_right_wall for enemy in self.enemies_1d]):
            for enemy in self.enemies_1d:
                enemy.y += enemy.height
                enemy.velocity = -abs(enemy.velocity)

        if any([enemy.is_touching_the_ship for enemy in self.enemies_1d]):
            self.game_over = True

        if not self.ship.lives:
            self.game_over = True

        if not self.enemies:
            self.win = True

        if self.keyboard.key_pressed("ESC"):
            self.finish = True

        self.show_fps()
        self.show_score()
        self.show_lives()
