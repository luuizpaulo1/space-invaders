from PPlay.gameimage import GameImage
from PPlay.keyboard import Keyboard
from PPlay.mouse import Mouse
from PPlay.window import Window
from db import DB


class RankingMenu:
    def __init__(self, window: Window, mouse: Mouse, keyboard: Keyboard, database: DB):
        self.window = window
        self.mouse = mouse
        self.keyboard = keyboard
        self.background = GameImage("./assets/background.png")

        self.finish = False

        self.database = database

    def show_scores(self):
        user_scores = self.database.get_top_5()
        self.window.draw_text(
            "Name",
            size=30,
            color="red",
            x=200,
            y=100
        )
        self.window.draw_text(
            "Score",
            size=30,
            color="red",
            x=400,
            y=100
        )
        for index, user_score in enumerate(user_scores):
            self.window.draw_text(
                user_score.username,
                size=30,
                color="red",
                x=200,
                y=100 + (index + 1) * 100
            )
            self.window.draw_text(
                str(user_score.score),
                size=30,
                color="red",
                x=400,
                y=100 + (index + 1) * 100
            )

    def loop(self):
        if self.keyboard.key_pressed("ESC"):
            self.finish = True
        self.background.draw()
        self.show_scores()
