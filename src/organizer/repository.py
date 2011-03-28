
import os
import re
from criterion import *


class Repository():
    """
    Repository
    A representation of a directory.
    can return a score based similarity of a string to a directory or file

    """
    def __init__(self,dirname): #opportunistic, only get the root directory.  Create sub repositories only as needed.
        for root, dirs, files in os.walk(dirname):
            self.rootDir = root
            self.dirList = dirs
            self.fileList = files
            break #only remember the root directory
        self.repositories = dict()
        self.dircriteria = [] #list of criteria to apply to matching directories
        self.filecriteria = [] #list of criteria to apply to matching files
    
    #generators
    def iterOverFiles(self):
        for filename in self.fileList:
            yield filename
    
    def iterOverDirs(self):
        for dirname in self.dirList:
            yield dirname
    #end generators 
    
    #publics
    def placeFile(self,theFile):
        """
        takes a filename and decides which directory in the repository it belongs to
        then creates a repository for that directory (if necessary) and passes on the request
        IF there are no directories in the repository it attempts to match a file, if matched
        returns a tuple of (matching files rootdir, matching file name)
        """
        destination = None #assume repository is terminal
        
        if not self._isTerminal(): #if the repository isn't terminal try to match a directory
            destination = self.dirWithScore(theFile) 
        
        if not destination: #There is no destination, or the repository is terminal-->try to match a file
            return self.fileWithScore(theFile)
        
        #there is a matched directory...
        if not self._hasRepository(destination): #repository does not exist, create it.
            self._addChildRepo(destination) 
        
        repository = self._getChildRepo(destination)
        
        #pass the query to the next repository
        return repository.placeFile(theFile)
    
    def fileWithScore(self,query,requirement=None):
        return self._queryList(query,self.fileList,self.filecriteria,False)
    
    
    def dirWithScore(self,query,requirement=None):
        return self._queryList(query,self.dirList,self.dircriteria,True)
 
    #end publics
    
    #privates
    def _isTerminal(self):
        return (self.dirList == [])
    
    def _addChildRepo(self,repDir):
        self.repositories[repDir] = Repository(repDir)
    
    def _getChildRepo(self,theKey):
        try:
            return self.repositories[theKey]
        except:
            return None
        
    def _hasRepository(self,repDir):
        try:
            self.repositories[repDir]
        except:
            return False
        
        return True    
    #end privates
    
    #private query methods
    def _queryList(self,query,theList,criteria,addRoot=True):
        """        
        #generic method to return the member of the list with the highest score
        #score is determined by matching words in the query
        #return the filename in the repository with the best score according to query.  None if score of 0
        #if there is a tie it returns the first instance of the highest score (or whatever max() returns)
        #scoring: exact matches get 10 points, partial matches get 1 point
        """
        if not theList: #empty lists cannot be matched
            return None 
        
        scoreList = [0]*len(theList)
        masterList = [[i,h] for i,h in zip(scoreList,theList)]
        
        #should be case insensitive
        lquery = query.lower()
        for aList in masterList:
            for criterion in criteria:
                if aList[0] == 'kill': #score is 'kill' this entry is not a match FUTURE
                    pass
                elif aList[0] == 'match': #score is 'match' this is the match no further processing required FUTURE
                    return self._highscore([aList],addRoot)
                else: #continue scoring
                    aList[0] = criterion.score(lquery,aList[1].lower())
                   
        return self._highscore(masterList,addRoot)
        
    def _highscore(self,masterList,addRoot=True):
        self._removeKills(masterList)
        masterList.sort()
        if masterList[-1][0] == 0:
            return None
        else:
            if addRoot: #add the root directory info to the result (it is a directory)
                return ''.join([self.rootDir,masterList[-1][1],'\\']) # equivalent to: self.Rootdir + masterList[-1][1] + '\\'
            else: #do not add it, it is a file
                return masterList[-1][1]
        return None   
    
    def _removeKills(self,masterList):
        """
        changes any kills in the masterList to 0 a sortable non match
        """
        for aList in masterList:
            if aList[0] == 'kill':
                aList[0] = 0 #no match
    #end query methods
    
class TVRepository(Repository):
    """
    subclass that sets the match criteria to TV files
    FUTURE make the criteria class variables
    """
    def __init__(self,dirname):
        super(TVRepository, self).__init__(dirname)
        criteria = ExactSimilarCriterion()
        self.dircriteria = [criteria]
        self.filecriteria = [TvSeasonEpisodeCriterion(),criteria]
        
    def _addChildRepo(self,repDir):
        self.repositories[repDir] = TVRepository(repDir)
    