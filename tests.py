import unittest
import codecs
from tv import TvParser


class TvTests(unittest.TestCase):
  
  def setUp(self):
    f = open("tvtestdata.html")
    self.testfile = f.read()

  def test_parse_result_is_not_non(self):
    parser = TvParser()
    parsed = parser.parse(self.testfile)
    self.assertIsNotNone(parsed)

  def test_parse_result_contains_rapport(self):
    parser = TvParser()
    parsed = parser.parse(self.testfile)
    shownames = map(lambda sho: sho.name, parsed[0].shows)
    self.assertIn("Rapport", shownames)



if __name__ == "__main__":
  unittest.main()




