import os
import subprocess
import unittest


class WholeTestCase(unittest.TestCase):
    def test_help(self):
        result = subprocess.run(['python', 'package/rss_reader.py', '-h'], stdout=subprocess.PIPE)
        output = result.stdout.decode()
        teststr = "show this help message and exit"
        self.assertIn(teststr, str(output))

    def test_version(self):
        result = subprocess.run(['python', 'package/rss_reader.py', '--version'], stdout=subprocess.PIPE)
        output = result.stdout.decode()
        teststr = "rss_reader.py "
        self.assertIn(teststr, str(output))

    def test_yahoo_rss_full(self):
        result = subprocess.run(['python', 'package/rss_reader.py', 'https://www.yahoo.com/news/rss'],
                               stdout=subprocess.PIPE)
        output = result.stdout
        teststr = "Title: "
        self.assertIn(teststr, str(output))

    def test_yahoo_rss_full_json(self):
        result = subprocess.run(['python', 'package/rss_reader.py', 'https://www.yahoo.com/news/rss', '--json'],
                                stdout=subprocess.PIPE)
        output = result.stdout
        teststr = '{"columns":["title","published","link"],"index":'
        self.assertIn(teststr, str(output))


if __name__ == "__main__":
    unittest.main()
