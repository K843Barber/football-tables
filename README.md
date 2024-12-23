# football-tables :soccer:

A way to extract football tables and see them right in your command line!

## Usage

Best to create venv with `python3 -m venv .venv` and activate with `source .venv/bin/activate`
Run `pip install -e .`
Only tested in `src/football/`, but in here, run something like: `football get --league --Premier_League --season 2023 24`, followed by `football show --league Premier_League --season 2023 24`

## Features

Includes
    - autocompletion from `argcomplete` for the top 5 leagues

## TODO

    - Add functionality to new format to be able to get all time table and H2H
    - Figure out tagging
