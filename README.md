# football-tables :soccer:

A way to extract football tables and see them right in your command line!

## Usage

Best to create venv with `python3 -m venv .venv` and activate with `source .venv/bin/activate`
Run `pip install -e .`
Only tested in `src/football/`, but in here, run something like: `football get --league --Premier_League --season 2023 24`, followed by `football show --league Premier_League --season 2023 24`

## Features

Includes - autocompletion from `argcomplete` for the top 5 leagues

## TODO

- Tables and stats
  - add goal against distribution
  - reformat page
  - add clean sheets, seasonal stats
- H2H
  - add emblems
  - back button in header or footer to fit into single page
  - Add clean sheets
- Seasonal stats table
  - Something including goals, clean sheets, top scorers (golden boot)
