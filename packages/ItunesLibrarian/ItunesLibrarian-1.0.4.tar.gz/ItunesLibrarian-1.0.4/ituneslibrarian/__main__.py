"""ItunesLibrarian.

Usage:
  ituneslibrarian.py parse [-i <input>] [-o <output>] [-c]
  ituneslibrarian.py search -f <name> [-s] [-c] [-p | -n] [--no-album | --album=<album>] [--no-artist | --artist=<artist>] [--no-title | --title=<title>]
  ituneslibrarian.py modify split [-b <symbol>] [-i <input>] [-s]

Options:
  -i, --input <input>     [default: Library.xml]
  -o, --output <output>     [default: Library.csv]
  -b, --symbol <symbol> [default: -]
  -s, --save            [default: false]
  -p, --print           [default: true]
  -n, --no-print        [default: true]
  -c, --check           [default: false]

"""

import ituneslibrarian.modify
import ituneslibrarian.parse
from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(__doc__, version='ItunesLibrary 1.0')

    if arguments["parse"]:
        ituneslibrarian.parse.to_csv(
            arguments["--input"], arguments["--output"])

    if arguments["search"]:
        print("Not implemented yet")

    if arguments["modify"]:
        library = ituneslibrarian.parse.to_dict(
            arguments["--input"])

        ituneslibrarian.modify.library(library)
