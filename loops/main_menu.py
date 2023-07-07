from PPlay.gameimage import GameImage
from PPlay.keyboard import Keyboard
from PPlay.mouse import Mouse
from PPlay.sprite import Sprite
from PPlay.window import Window
from db import DB, UserScore
from loops.difficulty_menu import DifficultyMenu
from loops.ranking_menu import RankingMenu
from loops.space_invaders import SpaceInvaders


class MainMenu:
    def __init__(self, window: Window, mouse: Mouse, keyboard: Keyboard, database: DB):
        self.window = window
        self.mouse = mouse
        self.keyboard = keyboard
        self.database = database

        self.background = GameImage("./assets/background.png")
        self.start = Sprite("./assets/start.png")
        self.difficulty_button = Sprite("./assets/difficulty.png")
        self.ranking_button = Sprite("./assets/ranking.png")
        self.exit_button = Sprite("./assets/exit.png")
        self.finish = False

        self.start.set_position((self.background.width / 2) - (self.start.width / 2), 100)
        self.difficulty_button.set_position((self.background.width / 2) - (self.difficulty_button.width / 2), 250)
        self.ranking_button.set_position((self.background.width / 2) - (self.ranking_button.width / 2), 400)
        self.exit_button.set_position((self.background.width / 2) - (self.exit_button.width / 2), 550)

        self.diff_menu = DifficultyMenu(self.window, self.mouse, self.keyboard)
        self.ranking_menu = RankingMenu(self.window, self.mouse, self.keyboard, self.database)
        self.space_invaders = SpaceInvaders(self.window, self.mouse, self.keyboard)

    def draw_game_over(self):
        font_size_header = 50
        font_size_body = 30
        self.window.draw_text(
            "GAME OVER!",
            size=font_size_header,
            color="red",
            x=(self.window.width / 2) - 150,
            y=self.window.height / 2 - font_size_header / 2
        )
        self.window.draw_text(
            "type your name in the terminal",
            size=font_size_body,
            color="red",
            x=170,
            y=self.window.height / 2 - font_size_body / 2 + font_size_body * 2
        )

    def loop(self):
        if self.mouse.is_over_object(self.start) and self.mouse.is_button_pressed(1):
            while True:
                self.space_invaders.finish = False
                self.space_invaders.loop()
                if self.space_invaders.finish:
                    break
                elif self.space_invaders.game_over:
                    self.draw_game_over()
                    self.window.update()
                    score = UserScore(input("name: "), score=self.space_invaders.score)
                    self.database.save_user_score(score)
                    self.space_invaders = SpaceInvaders(self.window, self.mouse, self.keyboard)
                    break

                elif self.space_invaders.win:
                    font_size = 50
                    text = "YOU WON!"
                    self.window.draw_text(
                        text,
                        size=font_size,
                        color="blue",
                        x=(self.window.width / 2) - 140,
                        y=self.window.height / 2 - font_size / 2
                    )
                self.window.update()

        if self.mouse.is_over_object(self.difficulty_button) and self.mouse.is_button_pressed(1):
            while True:
                self.diff_menu.finish = False
                self.diff_menu.loop()
                if self.diff_menu.finish:
                    break
                self.window.update()

        if self.mouse.is_over_object(self.ranking_button) and self.mouse.is_button_pressed(1):
            while True:
                self.ranking_menu.finish = False
                self.ranking_menu.loop()
                if self.ranking_menu.finish:
                    break
                self.window.update()

        if self.mouse.is_over_object(self.exit_button) and self.mouse.is_button_pressed(1):
            self.finish = True

        self.background.draw()
        self.start.draw()
        self.difficulty_button.draw()
        self.ranking_button.draw()
        self.exit_button.draw()
