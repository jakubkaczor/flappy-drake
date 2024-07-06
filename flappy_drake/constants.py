#!/bin/python

"""Constants used in the game."""

from pathlib import Path

ASSETS_PATH = Path(__file__).resolve().parent.parent / "assets"

WIDTH = 800
HEIGHT = 600
TITLE = "Flappy Drake"
SCALE = 1.0
JUMP_SPEED = 1000
SPEED = 500
GRAVITY = 9.81 * 5
PLAYER_MASS = 1.0
PIPE_MASS = PLAYER_MASS * 100
PIPE_PAIR_GAP = HEIGHT // 3
PIPE_PAIR_HEIGHT_RANGE = (PIPE_PAIR_GAP * 0.8, HEIGHT - PIPE_PAIR_GAP * 0.8)
SPAWN_INTERVAL_LENGTH = 1  # seconds
ABOUT_URL = "https://jakubkaczor.com"
SCOREBOARD_PATH = Path.home() / ".local/share/flappy-drake/scoreboard.csv"
MUSIC = False

INSTRUCTIONS = " ".join((
    "Keep the bird in the screen without touching the pipes. You get the point",
    "if you move past the half of a pipe, without touching it. To make the",
    "bird flap, press K, UP or SPACE. Anytime, you can go back to main menu with",
    "Q. Typing Q in the main menu will quit the application. To restart the game,",
    "press R.",
))
