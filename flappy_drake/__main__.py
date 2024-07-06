#!/bin/python

# Third party
import arcade

# Local
from .constants import *
from .views import MainMenuView

def main():
    window = arcade.Window(width=WIDTH, height=HEIGHT, title=TITLE)
    main_menu = MainMenuView()
    window.show_view(main_menu)
    arcade.run()


if __name__ == "__main__":
    main()
