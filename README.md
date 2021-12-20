# rss_reader

Pure python rss reader

Installation: per requirements.txt
python -m pip install argparse feedparser logging pandas

usage example
python rss_reader.py https://www.yahoo.com/news/rss

Usage doc:

 rss_reader.py [-h] [--limit LIMIT] [--version] [--json] [--verbose] source

positional arguments:
  source         URL of RSS source

optional arguments:
  -h, --help     show this help message and exit
  --limit LIMIT  Limit news topics if this parameter provided
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status message
  
Run unit tests::
python -m unittest test_rss_reader.WholeTestCase

Good output should be as 
C:\python3\rss_reader>python -m unittest test_rss_reader.WholeTestCase
....
----------------------------------------------------------------------
Ran 4 tests in 3.082s

OK

Do self-check (aleady implemented as Github action in main channel)
python -m pycodestyle test_rss_reader.py --max-line=120

Good output should now have any output
