# rss_reader

Python rss reader
## [Iteration 1]

Installation: per requirements.txt
main script is rss_reader.py located in package/ folder.
Actually, it's the only thing you need+requirements, if you don't package the solution.
```
python -m pip install argparse build fpdf feedparser logging pandas scikit-image
```
###### Most common usage example:
```
python rss_reader.py https://www.yahoo.com/news/rss
```

###### Usage doc:
```
rss_reader.py [-h] [--limit LIMIT] [--version] [--json] [--verbose] [--date DATE] [--to-pdf TO_PDF]
                     [--to-html TO_HTML]
                     [source ...]

Pure Python command-line RSS reader by gilyuliy

positional arguments:
  source             URL of RSS source

optional arguments:
  -h, --help         show this help message and exit
  --limit LIMIT      Limit news topics if this parameter provided
  --version          Print version info
  --json             Print result as JSON in stdout
  --verbose          Outputs verbose status message
  --date DATE        Date in Ymd format to read cache
  --to-pdf TO_PDF    Path where to export PDF
  --to-html TO_HTML  Path where to export HTML
  
```
Run unit tests:
```
python -m unittest test\test_rss_reader.WholeTestCase

Good output should be as
```
C:\python3\rss_reader\test>python -m unittest test_rss_reader.WholeTestCase
Ran 8 tests in 9.082s
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
python -m pip install build
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
````
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
````
## [Iteration 3]
Utility does caching in file rss_storage.h5
Format of storage is described at hdfgroup.org
Basically, we store DataFrame with following columns
- title
- published
- link
- published_Ymd
- mediaLink
- mediaContent

This is used for offline access when called with --date key
--date key can work with any other keys above

## [Iteration 4]
Utility is able to export data with images to PDF
To use that add --to-pdf path, for example:
```
python rss_reader.py https://news.yahoo.com/rss --to-pdf .
```
Utility accepts and understands all keys above and 
any combinations of them

When executed with source positional argument source,
utility stores all data, including images to DataFrame H5 storage,
so when used later with --date YYYMMDD, --to-pdf can be created offline

with --to-html utility will export data to html
```
python rss_reader.py https://news.yahoo.com/rss --to-html .
```

This also works with all possible combinations of keys above.
