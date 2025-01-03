from rich.console import Console  # noqa: D100

import football

console = Console()

small_logo = console.print(rf"""
    -   \O                                     ,  .-.___
  -     /\                                   O/  /xx\XXX\
 -   __/\ `                                  /\  |xx|XXX|
    `    \, ()                              ` << |xx|XXX|
^^^^^^^^^^^`^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[bold cyan]Football version: {football.__version__}[/bold cyan]""")  # type: ignore
