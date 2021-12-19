import argparse
import feedparser

VERSION=0.0.1

feed = feedparser.parse("https://news.yahoo.com/rss/")
entry = feed.entries[1]

for key in entry.keys():
    print ("Title: "+entry.title)
    print ("Date: "+entry.published)
    print ("Link: "+entry.link) 
