import itertools
from datetime import datetime

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

        self.ship.set_position((self.background.width / 2) - (self.ship.width / 2), self.background.height * 7 / 8)

        self.finish = False
        self.game_over = False
        self.win = False

        self.projectiles = []

        self.n_rows_enemies = 3
        self.n_columns_enemies = 5
        self.enemies = self.create_enemies(self.n_rows_enemies, self.n_columns_enemies)

        self.fps_counter = 0
        self.fps_display = 0
        self.fps_last_count = datetime.now()

    @property
    def enemies_1d(self):
        return itertools.chain.from_iterable(self.enemies)

    def expire_projectiles(self):
        for index in range(len(self.projectiles) - 1, -1, -1):
            next_projectile = False
            for enemy in self.enemies_1d:
                if self.projectiles[index].collided(enemy):
                    self.projectiles.pop(index)
                    enemy.health -= 1
                    next_projectile = True
                    break

            if next_projectile:
                continue

            if self.projectiles[index].y < 0:
                self.projectiles.pop(index)

    def expire_enemies(self):
        for i in range(len(self.enemies) - 1, -1, -1):
            for j in range(len(self.enemies[i]) - 1, -1, -1):
                if self.enemies[i][j].health <= 0:
                    self.enemies[i].pop(j)
            if not self.enemies[i]:
                self.enemies.pop(i)

    def create_enemies(self, n_rows: int, n_columns: int):
        dummy = Enemy(self)
        enemy_width = dummy.width
        enemy_height = dummy.height
        del dummy

        spacing_width = enemy_width * 1.5
        spacing_height = enemy_height * 1.5

        enemies = []
        enemy_y = 0
        for i in range(n_rows):
            enemy_x = 1
            row = []
            for j in range(n_columns):
                new_enemy = Enemy(self)
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

    def loop(self):
        if self.game_over or self.win:
            return

        self.count_fps()

        projectile = self.ship.action()
        if projectile:
            self.projectiles.append(projectile)

        self.expire_projectiles()
        self.expire_enemies()

        self.background.draw()
        self.ship.draw()

        for projectile in self.projectiles:
            projectile.move()
            projectile.draw()

        for enemy in self.enemies_1d:
            enemy.move()
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

        if not self.enemies:
            self.win = True

        if self.keyboard.key_pressed("ESC"):
            self.finish = True

        self.show_fps()
