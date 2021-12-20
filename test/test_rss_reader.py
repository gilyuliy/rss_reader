import datetime
import os
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
        result = subprocess.run(['python', '../package/rss_reader.py', 'https://www.yahoo.com/news/rss'],
                                stdout=subprocess.PIPE)
        output = result.stdout
        teststr = "Title: "
        self.assertIn(teststr, str(output))

    def test_yahoo_rss_full_json(self):
        """
        Test for using --json output
        """
        result = subprocess.run(['python', '../package/rss_reader.py', 'https://www.yahoo.com/news/rss', '--json'],
                                stdout=subprocess.PIPE)
        output = result.stdout
        teststr = '{"columns":["title","published","link","published_Ymd"]'
        self.assertIn(teststr, str(output))

    def test_yahoo_rss_full_json_yesterday(self):
        """
        Test for using --date
        """
        result = subprocess.run(['python', '../package/rss_reader.py', 'https://www.yahoo.com/news/rss', '--json',
                                 '--date', yesterday], stdout=subprocess.PIPE)
        output = result.stdout
        teststr = '{"columns":["title","published","link","published_Ymd"]'
        self.assertIn(teststr, str(output))


if __name__ == "__main__":
    unittest.main()
