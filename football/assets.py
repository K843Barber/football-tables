"""Page to provide module details."""

from rich.text import Text

import football

small_logo = rf"""
    -   \O                                     ,  .-.___
  -     /\                                   O/  /xx\XXX\
 -   __/\ `                                  /\  |xx|XXX|
    `    \, ()                              ` << |xx|XXX|
^^^^^^^^^^^`^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Football version: {Text(football.__version__, style="magenta")}"""  # type: ignore
