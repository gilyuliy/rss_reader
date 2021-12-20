import os
import subprocess
import unittest

class WholeTestCase(unittest.TestCase):
    def test_help(self):
        result = subprocess.run(['python', 'rss_reader.py', '-h'], stdout=subprocess.PIPE)
        output= result.stdout.decode()
        teststr="show this help message and exit"
        self.assertIn(teststr,str(output))
if __name__ == "__main__":
    unittest.main()