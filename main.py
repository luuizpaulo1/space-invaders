from PPlay.keyboard import Keyboard
from PPlay.mouse import Mouse
from PPlay.window import Window
from db import DB
from loops.main_menu import MainMenu

window = Window(700, 700)
keyboard = Keyboard()
mouse = Mouse()

db = DB()
db.create_user_score_table()


main_menu = MainMenu(window, mouse, keyboard, db)

while True:
    main_menu.loop()
    if main_menu.finish:
        break
    window.update()
