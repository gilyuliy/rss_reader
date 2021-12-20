import argparse
import dateutil.parser as dateparser
import feedparser
import logging
import pandas as pd
import re
import sys


def run_rss_reader():
    """
    Main funciton
    """
    __version__ = "0.0.5"
    STORAGE = "rss_storage.h5"

    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader by gilyuliy')
    parser.add_argument("source", type=str, help="URL of RSS source", nargs='*')
#    parser.add_argument("source", type=str, help="URL of RSS source")
    parser.add_argument("--limit", type=int,
                        help="Limit news topics if this parameter provided")
    parser.add_argument('--version', action='version', version='%(prog)s '+__version__, help="Print version info")
    parser.add_argument('--json', action='store_true', help="Print result as JSON in stdout")
    parser.add_argument('--verbose', action='store_true', help="Outputs verbose status message")
    parser.add_argument("--date", type=int,
                        help='Date in Ymd format to read cache')

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s ',
                            datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s ',
                            datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

    logging.debug("Program started")

    if args.limit:
        limit = args.limit
    else:
        limit = int(sys.maxsize)
    logging.debug("Limit is " + str(limit))

    if args.source:
        logging.debug("Source specified, online mode")
        source = str(args.source[0])
        print(source)
        logging.debug("Parsing RSS: " + str(source))
        feed = feedparser.parse(source)
        posts = []
        for index, key in zip(range(limit), feed.entries):
            entry = feed.entries[index]
            posts.append((entry.title, entry.published, entry.link,
                          (dateparser.parse(entry.published)).strftime('%Y%m%d')))
        logging.debug("Data: " + str(posts))
        logging.debug("Converting to DataFrame for future better processing")
        df = pd.DataFrame(posts, columns=['title', 'published', 'link', 'published_Ymd'])
        df.to_pickle(STORAGE)
        logging.debug(df)
    else:
        logging.debug("Source NOT specified, OFFLINE mode")
        if args.date:
            argsdate = str(args.date)
            p = re.compile('\\d{8}')
            if None is p.match(argsdate):
                logging.error("Date should be in format YYYYMMDD, e.g. 20211220")
                sys.exit(-1)
            logging.debug("Looking for news for date: " + str(argsdate))
            df = pd.read_pickle(STORAGE)
            df = df.head(limit + 1)
            df = df.loc[df['published_Ymd'] == argsdate]
            if df.shape[0] == 0:
                logging.error("No news found for date "+argsdate)
                sys.exit(-1)
            logging.debug(df)
        else:
            print("--date in %Y%m%d format is required if source is not specificed")
            sys.exit(-1)

    if args.json:
        logging.debug("Output is JSON")
        output = df.to_json(orient="split")
        print(output)
    else:
        logging.debug("Output is plaintext")
        print("\r\n")
        for index, row in df.iterrows():
            print("Title: "+row['title']+"\r\n"+"Date: "+row['published']+"\r\n"+"Link: "+row['link']+"\r\n")


if __name__ == "__main__":
    """This runs when you execute '$ python3 mypackage/mymodule.py'"""
    run_rss_reader()
