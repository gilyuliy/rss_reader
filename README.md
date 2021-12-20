# rss_reader

Pure python rss reader
## [Iteration 1]

Installation: per requirements.txt
```
python -m pip install argparse feedparser logging pandas
```
###### Most common usage example:
```
python rss_reader.py https://www.yahoo.com/news/rss
```

###### Usage doc:

rss_reader.py [-h] [--limit LIMIT] [--version] [--json] [--verbose] source

positional arguments:
  source         URL of RSS source

optional arguments:
  -h, --help     show this help message and exit
  --limit LIMIT  Limit news topics if this parameter provided
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status message
  
Run unit tests:
```
python -m unittest test_rss_reader.WholeTestCase
```
Good output should be as
```
C:\python3\rss_reader\test>python -m unittest test_rss_reader.WholeTestCase
Ran 4 tests in 3.082s
OK
```

Do self-check (aleady implemented as Github action in main channel)
```
python -m pycodestyle test\test_rss_reader.py --max-line=120
python -m pycodestyle package\rss_reader.py --max-line=120
```
Good output should now have any output

## [Iteration 2]
###### Packaging:
1. Execute
```
python -m build
```
Output should be 
```
Successfully built rss_reader-0.0.4.tar.gz and rss_reader-0.0.4-py3-none-any.whl
```

2. Upload  rss_reader-x.x.x.tar.gz and rss_reader-x.x.x-py3-none-any.whl to clean machine with python 3.9
3. Execute 
```
python3 -m pip install rss_reader-0.0.4.tar.gz
```
4. Output should be 
```
Successfully installed rss-reader-0.0.4
```
6. Execute
```
rss_reader -h
```
8. Output should be same as in python script:
rss_reader [-h] [--limit LIMIT] [--version] [--json] [--verbose] source

Pure Python command-line RSS reader by gilyuliy

positional arguments:
  source         URL of RSS source

optional arguments:
  -h, --help     show this help message and exit
  --limit LIMIT  Limit news topics if this parameter provided
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status message
  --date DATE    Date in Ymd format to read cache

## [Iteration 3]
Utility does caching in file rss_storage.h5
Format of storage is described at hdfgroup.org
Basically, we store DataFrame with following columns
- title
- published
- link
- published_Ymd

This is used for offline access when called with --date key
--date key can work with any other keys above
