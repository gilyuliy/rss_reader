import argparse
import feedparser
import sys
import logging
import pandas as pd

__version__="0.0.2"

parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader by gilyuliy')
parser.add_argument("source", type=str, help="URL of RSS source")
parser.add_argument("--limit", type=int,
                    help="Limit news topics if this parameter provided")
parser.add_argument('--version', action='version', version='%(prog)s '+__version__, help="Print version info")
parser.add_argument('--json', action='store_true', help="Print result as JSON in stdout")
parser.add_argument('--verbose', action='store_true', help="Outputs verbose status message")

args = parser.parse_args()

if args.verbose:
    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s ', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)
else:
    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s ', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


logging.debug("Program started")

source=args.source
logging.debug("Parsing RSS: " +source)

feed = feedparser.parse(source)
entry = feed.entries[1]

if args.limit:
    limit=args.limit
else:
    limit=int(sys.maxsize)
logging.debug("Limit is "+str(limit))

posts=[]
for index, key in zip(range(limit), entry.keys()):
    posts.append((entry.title,entry.published,entry.link))
logging.debug("Data: "+str(posts))
logging.debug("Converting to DataFrame for future better processing")
df = pd.DataFrame(posts, columns=['title', 'published', 'link'])
logging.debug(df)

if args.json:
    logging.debug("Output is JSON")
    output = df.to_json(orient="split")
    print (output)
else:
    logging.debug("Output is plaintext")
    print("\r\n")
    for index, row in df.iterrows():
        print("Title: "+row['title']+"\r\n"+"Date: "+row['published']+"\r\n"+"Link: "+row['link']+"\r\n")