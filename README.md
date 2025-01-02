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
  - add clean sheets, seasonal stats
- H2H
  - add emblems
  - back button in header or footer to fit into single page
- Seasonal stats table
  - Something including goals, clean sheets, top scorers (golden boot)
- Tidy up
  - helper_functions (combine them since alot do similar stuff)
  - format_tables (might need to take stuff from show_table)
  - Need to correct data before querying it really.
    - Although the list is nice in H2H, the queried stats are wrong, at least for la liga and serie a. PL seems to in line with data online. Unsure of Bundesliga, Ligue 1 yet, or Allsvenskan

## Status

### Leagues

| _Page_       | _Sub-item_    | _Allsvenskan_                     | _Bundesliga_                      | _La Liga_                         | _Ligue 1_                         | _Premier League_                                       | _Serie A_                         |
| :----------- | :------------ | :-------------------------------- | :-------------------------------- | :-------------------------------- | :-------------------------------- | :----------------------------------------------------- | :-------------------------------- |
| League Table | Tables        | <input type="checkbox" unchecked> | <input type="checkbox" unchecked> | <input type="checkbox" unchecked> | <input type="checkbox" unchecked> | <input type="checkbox" checked>                        | <input type="checkbox" unchecked> |
|              | Seasons       | <input type="checkbox" unchecked> | <input type="checkbox" unchecked> | <input type="checkbox" unchecked> | <input type="checkbox" unchecked> | <input type="checkbox" checked>                        | <input type="checkbox" unchecked> |
|              | Goal dists    | <input type="checkbox" unchecked> | <input type="checkbox" unchecked> | <input type="checkbox" unchecked> | <input type="checkbox" unchecked> | <input type="checkbox" checked>                        | <input type="checkbox" unchecked> |
|              | General stats | <input type="checkbox" unchecked> | <input type="checkbox" unchecked> | <input type="checkbox" unchecked> | <input type="checkbox" unchecked> | <input type="checkbox" unchecked> Clean Sheets         | <input type="checkbox" unchecked> |
| H2H          | Stats         | <input type="checkbox" unchecked> | <input type="checkbox" unchecked> | <input type="checkbox" unchecked> | <input type="checkbox" unchecked> | <input type="checkbox" unchecked> Wins                 | <input type="checkbox" unchecked> |
|              | Stats         | <input type="checkbox" unchecked> | <input type="checkbox" unchecked> | <input type="checkbox" unchecked> | <input type="checkbox" unchecked> | <input type="checkbox" unchecked> Logo                 | <input type="checkbox" unchecked> |
| All Time     | New Feature   | <input type="checkbox" unchecked> | <input type="checkbox" unchecked> | <input type="checkbox" unchecked> | <input type="checkbox" unchecked> | <input type="checkbox" unchecked> No. of league titles | <input type="checkbox" unchecked> |
