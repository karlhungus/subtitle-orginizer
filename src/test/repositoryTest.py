import unittest

from organizer.repository import Repository

class TestRepository(unittest.TestCase):
    def testQueryListReturnsNoneForNoMatches(self):
        repository = Repository("fakedir")
        theList = ["foo", "bar", "biz", "bat"]
        self.assertEquals(None, repository._queryList("bilbo", theList))
        
    def testQueryListReturnsBestMatch(self):
        repository = Repository("fakedir")
        theList = ["bil", "billbo", "BILbiz", "BILBO"]
        self.assertEquals("BILBO",repository._queryList("bilbo", theList))
        
