#!/bin/python3

"""Sprites used in the game."""

# Local
from .constants import *

# Standard
from typing import Tuple, Sequence
import random

# Third party
import arcade
from PIL import Image


class Player(arcade.Sprite):
    """Player's sprite."""

    def __init__(self) -> None:
        super().__init__(
            ASSETS_PATH / "drake.png",
            hit_box_algorithm="Detailed",
            scale=0.1 * SCALE,
            center_y=HEIGHT / 2,
            center_x=100,
        )
        self.flapped: bool = False
        self.alive: bool = True

    @property
    def in_screen(self):
        """True if the sprite is in the screen, false otherwise."""
        # As the most of the time, player is in screen, it is better to check negated “or”s, as
        # usually only the first condition is checked.
        return not (
            self.right <= 0
            or self.left >= WIDTH
            or self.top <= 0
            or self.bottom >= HEIGHT
        )


class Pipe(arcade.Sprite):
    """Enemy sprite.

    Instance of the class is a sprite represented by a pipe.
    """

    def __init__(self, flipped: bool = False):
        image_path = ASSETS_PATH / "pipe.png"
        image = Image.open(image_path)
        super().__init__(
            # TODO: Contribute to Python Arcade with pathlib support
            image_path,
            scale=SCALE * 0.3,
            image_height=image.height,
            image_width=image.width,
            flipped_vertically=flipped,
        )
        self.left = WIDTH
        self.top = WIDTH // 2

    @classmethod
    def create_pipe_pair(
        cls, center_height: float, gap: float
    ) -> Tuple["Pipe", "Pipe"]:
        """Return a tuple of `Pipe`s, one above the other, being symmetric with respect to midpoint.

        The difficulty of overcoming each pipe pair is determined by its gap and height of the gap
        relative to the preceding pipe pairs. The distance between pipe pairs is determined by
        timers. Therefore, `center_height` and `gap` were chosen as constructor's parameters.
        """
        gap_half = gap / 2
        lower = Pipe()
        upper = Pipe(flipped=True)
        lower.top = center_height - gap_half
        upper.bottom = center_height + gap_half
        return (lower, upper)

    @classmethod
    def create_random_pipe_pair(
        cls,
        height_range: Sequence[float],
        gap: float,
        random_generator: random.Random,
    ):
        """Return a pair of pipes with randomly (uniformly) chosen height of a center (midpoint)."""
        height = random_generator.uniform(*height_range)
        return cls.create_pipe_pair(height, gap)
