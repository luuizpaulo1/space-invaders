from PPlay.gameimage import GameImage
from PPlay.keyboard import Keyboard
from PPlay.mouse import Mouse
from PPlay.window import Window
from sprites.ship import Ship


class SpaceInvaders:
    def __init__(self, window: Window, mouse: Mouse, keyboard: Keyboard):
        self.window = window
        self.mouse = mouse
        self.keyboard = keyboard
        self.background = GameImage("./assets/background.png")
        self.ship = Ship(window=self.window, keyboard=self.keyboard, shoot_cadence=1000)

        self.ship.set_position((self.background.width / 2) - (self.ship.width / 2), self.background.height * 7 / 8)

        self.finish = False

        self.projectiles = []

    def expire_projectiles(self):
        for index in range(len(self.projectiles) - 1, -1, -1):
            if self.projectiles[index].y < 0:
                self.projectiles.pop(index)

    def loop(self):
        self.background.draw()
        self.ship.draw()
        projectile = self.ship.action()
        if projectile:
            self.projectiles.append(projectile)

        self.expire_projectiles()
        for projectile in self.projectiles:
            projectile.update()
            projectile.draw()

        if self.keyboard.key_pressed("ESC"):
            self.finish = True
