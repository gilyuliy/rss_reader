import os
import sys
modpath = '../package/'
sys.path.insert(0, modpath)

if True:
    import datetime
    import pandas as pd
    import rss_reader
    import subprocess
    import unittest

yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y%m%d')


class WholeTestCase(unittest.TestCase):
    def test_help(self):
        """
        Test for running with -h
        """
        result = subprocess.run(['python', '../package/rss_reader.py', '-h'], stdout=subprocess.PIPE)
        output = result.stdout.decode()
        teststr = "show this help message and exit"
        self.assertIn(teststr, str(output))

    def test_version(self):
        """
        Test for running with --version
        """
        result = subprocess.run(['python', '../package/rss_reader.py', '--version'], stdout=subprocess.PIPE)
        output = result.stdout.decode()
        teststr = "rss_reader.py "
        self.assertIn(teststr, str(output))

    def test_yahoo_rss_full(self):
        """
        Test for regular use
        """
        result = subprocess.run(['python', '../package/rss_reader.py', 'https://www.yahoo.com/news/rss',
                                '--limit', '2'], stdout=subprocess.PIPE)
        output = result.stdout.decode()
        teststr = "Title: "
        self.assertIn(teststr, str(output))

    def test_yahoo_rss_full_json(self):
        """
        Test for using --json output
        """
        result = subprocess.run(['python', '../package/rss_reader.py', 'https://www.yahoo.com/news/rss', '--json',
                                '--limit', '2'], stdout=subprocess.PIPE)
        output = result.stdout
        teststr = '{"columns":["title","published","link","published_Ymd"'
        self.assertIn(teststr, str(output))

    def test_yahoo_rss_full_json_yesterday(self):
        """
        Test for using --date
        """
        result = subprocess.run(['python', '../package/rss_reader.py', 'https://www.yahoo.com/news/rss', '--json',
                                 '--date', yesterday, '--limit', '2'], stdout=subprocess.PIPE)
        output = result.stdout.decode()
        teststr = '{"columns":["title","published","link","published_Ymd"'
        self.assertIn(teststr, str(output))

    def test_yahoo_rss_full_pdf(self):
        """
        Test for using pdf in command line
        """
        result = subprocess.run(['python', '../package/rss_reader.py', 'https://www.yahoo.com/news/rss', '--to-pdf',
                                 '.', '--limit', '2'], stdout=subprocess.PIPE)
        output = result.stdout.decode()
        teststr = 'Title:'
        self.assertIn(teststr, str(output))

    def test_dftoPDF(self):
        """
        Test for converting PDF function only
        """
        data = {'title': ['Title1', 'Title2'],
                'published': ['2021-12-19T16:29:42Z', '2021-12-19T16:29:43Z'],
                'link': ['http://localhost', 'http://localhost2'],
                'mediaLink': ['', ''],
                'mediaContent': ['', '']}
        df = pd.DataFrame(data)
        self.assertTrue(rss_reader.dftoPDF(df, '.'))


if __name__ == "__main__":
    unittest.main()
