# Flappy Drake

Flappy Drake (“drake” means “kaczor” in polish) is a recreation
of the popular Flappy Bird.


# Dependencies

- Python
- poetry
- GNU make
- Inkscape


# Building and running

To build the project, execute
```sh
make
```

To run the game, execute
``` sh
poetry run flappy-drake
```
in the project's root directory.


# Assets

The assets used are either Arcade's builtins or handmade by the authors
of Flappy Drake and licensed under [Creative Commons Attribution 4.0
International](https://creativecommons.org/licenses/by/4.0), unless stated
otherwise for specific cases.


# Implementation details

Pyglet doesn't support loading SVG graphics yet[1]. Therefore, all SVG
graphics need to be converted to PNGs beforehand. After the issue is
solved, the removal of Inkscape, and possibly GNU Make, will
be possible.

Some methods implement Arcade's parent class interfaces, so they are not
documented as it would be too verbose. If a method does not contain a
docstring, try to refer to Arcade's documentation first.

[1]: https://github.com/pyglet/pyglet/issues/192
