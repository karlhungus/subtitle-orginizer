import unittest
import urllib
from xml.dom import minidom

from organizer.downloader import SubtitleDownloader

class TestDownloader(unittest.TestCase):
   # def testQueryListReturnsNoneForNoMatches(self):
   #     repository = Downloader("http://www.addic7ed.com/")
   #     theList = ["foo", "bar", "biz", "bat"]
   #     self.assertEquals(None, repository._queryList("bilbo", theList))
   
   
   def testFindSubtitle(self):
       url= "http://search.twitter.com/search.atom?q=from%3AAddic7ed%20Archer%2002x08%20&since=2009-01-01"
       #response= urllib.request.urlopen(url, None)
       dom = minidom.parse(urllib.request.urlopen(url))
       #print(dom.getElementsByTagName('title')[0].firstChild.data)

       for node in dom.getElementsByTagName("title"):
           print(node.firstChild.data)
