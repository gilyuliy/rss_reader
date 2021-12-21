import argparse
import dateutil.parser as dateparser
from fpdf import FPDF
import feedparser
import logging
import os
import pandas as pd
import random
import re
from skimage import io
import sys
import time


def dftoPDF(df, path):
    '''
    Creates pdf from Dataframe and saves as file in specified path
    '''
    pdf = FPDF(format='a4', unit='cm')
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    effective_page_width = pdf.w-2*pdf.l_margin
    for index, row in df.iterrows():
        row["title"] = row["title"].encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(effective_page_width, 0.5, "Title: "+row["title"])
        pdf.ln(0.5)
        pdf.multi_cell(effective_page_width, 0.5, "Date: "+row["published"])
        pdf.ln(0.5)
        row["link"] = row["link"].encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(effective_page_width, 0.5, "Link: "+row["link"])
        pdf.ln(0.5)
        row["published"] = row["published"].encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(effective_page_width, 0.5, "Date: "+row["published"])
        pdf.ln(0.5)
        row["mediaLink"] = row["mediaLink"].encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(effective_page_width, 0.5, "MediaLink: "+row["mediaLink"])
        pdf.ln(0.5)
        image = row["mediaContent"]
        if str(image) != '':
            tempfilename = str(random.randint(1, 1000000000000))+".jpg"
            logging.debug("Export DF array to temp image as: "+tempfilename)
            io.imsave(tempfilename, image)
            pdf.image(tempfilename, w=effective_page_width)
            os.remove(tempfilename)
            pdf.ln(1)

    fullPath = os.path.join(path, time.strftime("%Y%m%d-%H%M%S")+".pdf")
    logging.debug("Exporing PDF as: "+fullPath)
    pdf.output(fullPath)
    return True


def dftoHTML(df, path):
    '''
    Creates HTML from Dataframe and saves as file in specified path
    '''
    data = "<html><body>"
    for index, row in df.iterrows():
        row["title"] = row["title"].encode('latin-1', 'replace').decode('latin-1')
        row["link"] = row["link"].encode('latin-1', 'replace').decode('latin-1')
        row["mediaLink"] = row["mediaLink"].encode('latin-1', 'replace').decode('latin-1')
        row["published"] = row["published"].encode('latin-1', 'replace').decode('latin-1')
        data = data+row["title"]
        data = data+"<br>"
        data = data+row["link"]
        data = data+"<br>"
        data = data+"<a href=\""+row["mediaLink"]+"\">Image</a>"
        data = data+"<br>"
        data = data+row["published"]
        data = data+"<hr>\r\n"
    data = data+"</body></html>"
    fullPath = os.path.join(path, time.strftime("%Y%m%d-%H%M%S")+".html")
    logging.debug("Exporing HTML as: "+fullPath)
    f = open(fullPath, "w")
    f.write(data)
    f.close()

    return True


def run_rss_reader():
    """
    Main funciton
    """
    __version__ = "0.0.7"
    STORAGE = "rss_storage.h5"

    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader by gilyuliy')
    parser.add_argument("source", type=str, help="URL of RSS source", nargs='*')
    parser.add_argument("--limit", type=int,
                        help="Limit news topics if this parameter provided")
    parser.add_argument('--version', action='version', version='%(prog)s '+__version__, help="Print version info")
    parser.add_argument('--json', action='store_true', help="Print result as JSON in stdout")
    parser.add_argument('--verbose', action='store_true', help="Outputs verbose status message")
    parser.add_argument("--date", type=int, help='Date in Ymd format to read cache')
    parser.add_argument("--to-pdf", type=str, help='Path where to export PDF')
    parser.add_argument("--to-html", type=str, help='Path where to export HTML')

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
        logging.debug("Parsing RSS: " + str(source))
        feed = feedparser.parse(source)
        posts = []
        for index, key in zip(range(limit), feed.entries):
            entry = feed.entries[index]
            if 'media_content' in entry:
                mediaLink = entry.media_content[0]['url']
                mediaContent = io.imread(entry.media_content[0]['url'])
                logging.debug("Found media at url: "+str(mediaLink))
            else:
                mediaContent = ""
                mediaLink = ""

            posts.append((entry.title, entry.published, entry.link,
                          (dateparser.parse(entry.published)).strftime('%Y%m%d'), mediaLink, mediaContent))

        logging.debug("Converting to DataFrame for future better processing")
        df = pd.DataFrame(posts, columns=['title', 'published', 'link', 'published_Ymd', 'mediaLink', 'mediaContent'])
        df.to_pickle(STORAGE)
        logging.debug("Shape of DataFrame: "+str(df.shape))
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
            logging.debug("Shape of DataFrame: "+str(df.shape))
        else:
            print("--date in %Y%m%d format is required if source is not specificed")
            sys.exit(-1)

    if args.to_pdf:
        logging.debug("Creating PDF at "+str(args.to_pdf))
        dftoPDF(df, str(args.to_pdf))

    if args.to_html:
        logging.debug("Creating HTML at "+str(args.to_html))
        dftoHTML(df, str(args.to_html))

    if args.json:
        logging.debug("Output is JSON")
        df_forjson = df[['title', 'published', 'link', 'published_Ymd', 'mediaLink']]
        output = df_forjson.to_json(orient="split")
        print(output)
    else:
        logging.debug("Output is plaintext")
        print("\r\n")
        for index, row in df.iterrows():
            print("Title: "+row['title']+"\r\n"+"Date: "+row['published']+"\r\n"+"Link: "+row['link']+"\r\n" +
                  "Media: "+row['mediaLink']+"\r\n")


if __name__ == "__main__":
    """This runs when you execute '$ python3 mypackage/mymodule.py'"""
    run_rss_reader()
