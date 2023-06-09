from PPlay.gameimage import GameImage
from PPlay.keyboard import Keyboard
from PPlay.mouse import Mouse
from PPlay.sprite import Sprite
from PPlay.window import Window


class DifficultyMenu:
    def __init__(self, window: Window, mouse: Mouse, keyboard: Keyboard):
        self.window = window
        self.mouse = mouse
        self.keyboard = keyboard
        self.background = GameImage("./assets/background.png")
        self.easy_button = Sprite("./assets/easy_button.png")
        self.intermediate_button = Sprite("./assets/intermediate_button.png")
        self.hard_button = Sprite("./assets/hard_button.png")
        self.finish = False

        self.easy_button.set_position((self.background.width / 2) - (self.easy_button.width / 2), 100)
        self.intermediate_button.set_position((self.background.width / 2) - (self.intermediate_button.width / 2), 250)
        self.hard_button.set_position((self.background.width / 2) - (self.hard_button.width / 2), 400)

    def loop(self):
        if self.mouse.is_over_object(self.easy_button) and self.mouse.is_button_pressed(1):
            ...
        if self.mouse.is_over_object(self.intermediate_button) and self.mouse.is_button_pressed(1):
            ...
        if self.mouse.is_over_object(self.hard_button) and self.mouse.is_button_pressed(1):
            ...

        if self.keyboard.key_pressed("ESC"):
            self.finish = True

        self.background.draw()
        self.easy_button.draw()
        self.intermediate_button.draw()
        self.hard_button.draw()
