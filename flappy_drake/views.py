#!/bin/python3

"""Views used in the game."""

# Local
from .constants import *
from .sprites import Player, Pipe

# Standard
from typing import Optional, List
import random
import webbrowser
import threading
import csv
from pathlib import Path

# Third party
import arcade
import arcade.gui as gui
import arcade.key as keys
import arcade.csscolor as colors



def open_url(url: str) -> None:
    """Wrapper around `webbrowser.open`, making it non-blocking.

    The purpose of this function is to make buttons in the main menu responsive, because the
    application isn't blocked by opening a page in the browser anymore.
    """
    thread = threading.Thread(
        group=None, target=lambda: webbrowser.open(url), daemon=True
    )
    thread.start()


def prep_scoreboard() -> Path:
    """Prepare directory for resources in accordance with XDG Base Directory."""
    SCOREBOARD_PATH.parent.mkdir(exist_ok=True)
    SCOREBOARD_PATH.touch()
    return SCOREBOARD_PATH


def read_scoreboard() -> List[int]:
    """Return the scores from the scoreboard in descending order."""
    prep_scoreboard()
    with SCOREBOARD_PATH.open() as scoreboard_file:
        scores = []
        for score in scoreboard_file:
            score = int(score)
            scores.append(score)

    scores.sort(reverse=True)
    return scores


def add_to_scoreboard(score: int) -> None:
    """Add the score to the scoreboard file.

    The `score` is added if it is at least as high as the lowest one. If the scoreboard is full
    (contains 5 scores), the `score` replaces the current lowest if it is smaller.
    """
    top_scores = read_scoreboard()
    # TODO: This is unsafe. Scoreboard structure doesn't guarantee that the
    # lowest score is at the end. A new type is needed.
    lowest_score = top_scores[-1] if top_scores else -1
    if score < lowest_score:
        return

    if len(top_scores) >= 5:
        top_scores.pop(-1)
    top_scores.append(score)

    with SCOREBOARD_PATH.open("w") as scoreboard_file:
        new_scoreboard = "\n".join(str(score) for score in top_scores)
        scoreboard_file.write(new_scoreboard)


class MainMenuView(arcade.View):
    def __init__(self, window=None):
        super().__init__(window)

        # Descendant views
        self.game = GameView(self)
        self.instructions_view = InstructionsView(self)
        self.scoreboard_view = ScoreboardView(self)

        # Prepare UI environment
        self.manager = gui.UIManager()
        self.box = gui.UIBoxLayout()

        # Buttons definitions
        self.start_button = gui.UIFlatButton(text="Start", width=WIDTH * 0.2)
        self.about_button = gui.UIFlatButton(text="About the Author", width=WIDTH * 0.2)
        self.quit_button = gui.UIFlatButton(text="Quit", width=WIDTH * 0.2)
        self.scoreboard_button = gui.UIFlatButton(text="Top Scores", width=WIDTH * 0.2)
        self.instructions_button = gui.UIFlatButton(
            text="Instructions", width=WIDTH * 0.2
        )

        # Button actions
        self.quit_button.on_click = lambda event: arcade.exit()
        self.instructions_button.on_click = lambda event: self.window.show_view(
            self.instructions_view
        )
        self.about_button.on_click = lambda event: open_url(ABOUT_URL)
        self.start_button.on_click = self.start_game
        self.scoreboard_button.on_click = lambda event: self.window.show_view(
            self.scoreboard_view
        )

        # Adding buttons to the box (order is important)
        self.box.add(self.start_button)
        self.box.add(self.scoreboard_button)
        self.box.add(self.instructions_button)
        self.box.add(self.about_button)
        self.box.add(self.quit_button)

        self.manager.add(gui.UIAnchorWidget(child=self.box))

    def start_game(self, event=None):
        self.game.setup()
        self.window.show_view(self.game)
        # TODO: Figure out how to make it into GameView
        arcade.schedule(self.game.spawn_enemy, interval=SPAWN_INTERVAL_LENGTH)

    def on_show(self):
        arcade.set_background_color(colors.AZURE)
        # TODO: Figure out how to make it into GameView
        arcade.unschedule(self.game.spawn_enemy)
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_key_press(self, symbol: int, modifiers: int):
        match symbol:
            case keys.S:
                self.start_game()
            case keys.Q:
                arcade.exit()
            case keys.I:
                self.window.show_view(self.instructions_view)
            case keys.A:
                open_url(ABOUT_URL)
            case keys.T:
                self.window.show_view(self.scoreboard_view)

    def on_draw(self):
        self.clear()
        self.manager.draw()


class SubMenuView(arcade.View):
    """Base class for submenus."""

    def __init__(self, top_menu: arcade.View, window: Optional[arcade.Window] = None):
        super().__init__(window)
        self.top_menu = top_menu
        self.manager = gui.UIManager()
        # self.manager.enable()
        self.back_button = gui.UIFlatButton(text="Back", x=WIDTH / 2 - 50, y=25)
        self.back_button.on_click = lambda event: self.window.show_view(self.top_menu)
        self.manager.add(self.back_button)

    def on_show(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_key_press(self, symbol: int, _modifiers: int):
        if symbol in {keys.Q, keys.B, keys.ESCAPE}:
            self.window.show_view(self.top_menu)


class ScoreboardView(SubMenuView):
    def __init__(self, top_menu, window: Optional[arcade.Window] = None):
        super().__init__(top_menu, window)

    def on_show(self):
        super().on_show()
        top_scores = read_scoreboard()
        if top_scores:
            top_scores_text = "The best 5 scores are\n"
            top_scores_text += "\n".join(str(score) for score in top_scores)

        else:
            top_scores_text = "Be the first one to score!"

        self.scoreboard = arcade.Text(
            top_scores_text,
            align="center",
            multiline=True,
            font_size=16,
            start_x=WIDTH / 2,
            start_y=HEIGHT / 2,
            anchor_x="center",
            anchor_y="center",
            width=WIDTH // 2,
            color=colors.BLACK,
        )

    def on_draw(self):
        super().on_draw()
        self.scoreboard.draw()


class InstructionsView(SubMenuView):
    def __init__(self, top_menu: arcade.View, window: Optional[arcade.Window] = None):
        super().__init__(top_menu, window)

    def on_draw(self):
        super().on_draw()
        arcade.draw_text(
            INSTRUCTIONS,
            WIDTH / 2,
            HEIGHT / 2,
            anchor_x="center",
            anchor_y="center",
            color=colors.BLACK,
            multiline=True,
            align="center",
            font_size=16,
            width=5 / 8 * WIDTH,
        )


class GameView(arcade.View):
    def __init__(self, main_menu=Optional[arcade.View]) -> None:
        super().__init__()
        self.random_generator = random.Random()
        self.score_sound = arcade.load_sound(":resources:sounds/coin5.wav")
        self.lose_sound = arcade.load_sound(":resources:sounds/hurt1.wav")
        self.main_menu = main_menu

    def setup(self) -> None:
        arcade.set_background_color(colors.AZURE)
        self.score = 0
        self.player = Player()
        # Separating enemy and scored is for optimizing checking if a pipe is out of the screen.
        self.enemy_list = arcade.SpriteList()
        self.scored_list = arcade.SpriteList()
        self.physics_engine = arcade.PymunkPhysicsEngine(gravity=(0, -GRAVITY * 100))
        self.physics_engine.add_sprite(self.player)

    def spawn_enemy(self, delta_time: float):
        enemy_pair = Pipe.create_random_pipe_pair(
            PIPE_PAIR_HEIGHT_RANGE, PIPE_PAIR_GAP, self.random_generator
        )
        # TODO: Contribute to Python Arcade with ”+=”.
        self.enemy_list.extend(list(enemy_pair))
        for enemy in enemy_pair:
            self.physics_engine.add_sprite(
                enemy, mass=PIPE_MASS, gravity=(0, 0), friction=1
            )
            self.physics_engine.set_horizontal_velocity(enemy, -SPEED)

    def on_key_press(self, symbol: int, modifiers: int):
        match symbol:
            case keys.UP | keys.K | keys.SPACE:
                if not self.player.flapped and self.player.alive:
                    self.physics_engine.set_velocity(self.player, (0, JUMP_SPEED))
                    self.player.flapped = True

            case keys.R:
                self.setup()

            case keys.Q | keys.ESCAPE:
                self.window.show_view(self.main_menu)

    def on_key_release(self, symbol: int, modifiers: int):
        match symbol:
            case keys.UP | keys.K | keys.SPACE:
                self.player.flapped = False

    def on_update(self, delta_time: float):
        self.physics_engine.step()

        collisions = arcade.check_for_collision_with_lists(
            self.player, (self.scored_list, self.enemy_list)
        )

        if collisions or not self.player.in_screen:
            if self.player.alive:
                self.lose_sound.play()
                add_to_scoreboard(self.score)
                game_over_view = GameOverView(self)
                self.window.show_view(game_over_view)
            self.player.alive = False

        # OPTIMIZE: the check. Is `kill` costly? No need to call it after death—it is already dead.
        if not self.player.in_screen:
            self.player.kill()

        if self.enemy_list and self.enemy_list[0].center_x < self.player.center_x:
            # Each one of a pipe pair is a separate sprite.
            self.scored_list.append(self.enemy_list.pop(0))
            self.scored_list.append(self.enemy_list.pop(0))
            if self.player.alive:
                self.score += 1
                self.score_sound.play()

        if scored := self.scored_list:
            while scored and scored[0].right <= 0:
                scored[0].remove_from_sprite_lists()

    def on_draw(self):
        self.clear()
        self.enemy_list.draw()
        self.scored_list.draw()
        self.player.draw()

        self.score_text = arcade.Text(
            str(self.score),
            WIDTH // 2,
            0.9 * HEIGHT,
            color=colors.BLACK,
            font_size=24,
            anchor_x="center",
        )
        self.score_text.draw()


class GameOverView(arcade.View):
    def __init__(self, game_view: arcade.View, window: Optional[arcade.Window] = None):
        super().__init__(window)
        self.game_view = game_view

    def on_update(self, delta_time: float):
        self.game_view.on_update(delta_time)

    def on_draw(self):
        self.clear()
        self.game_view.on_draw()
        arcade.draw_text(
            "Game over!",
            WIDTH / 2,
            HEIGHT / 2,
            color=colors.BLACK,
            anchor_x="center",
            font_size=32,
        )
        arcade.draw_text(
            "Press R to restart, or Q to quit.",
            WIDTH / 2,
            HEIGHT / 3,
            color=colors.BLACK,
            anchor_x="center",
            font_size=16,
        )

    def on_key_press(self, symbol: int, modifiers: int):
        match symbol:
            case keys.R:
                self.game_view.setup()
                self.window.show_view(self.game_view)

            case keys.Q | keys.ESCAPE:
                if self.game_view.main_menu:
                    self.window.show_view(self.game_view.main_menu)
