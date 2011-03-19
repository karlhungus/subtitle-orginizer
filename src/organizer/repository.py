"""
Repository
A representation of a directory.
can return a score based similarity of a string to a directory or file
can rename, move, copy files
"""
import os
import re


class Repository():
    def __init__(self,dirname): #opportunistic, only get the root directory.  Create sub repositories only as needed.
        for root, dirs, files in os.walk(dirname):
            self.rootDir = root
            self.dirList = dirs
            self.fileList = files
            break #only remember the root directory
        
    #generators
    def iterOverFiles(self):
        for filename in self.fileList:
            yield filename
    
    def iterOverDirs(self):
        for dirname in self.dirList:
            yield dirname
    #end generators 
        
    def fileWithScore(self,query):
        return self._queryList(query,self.fileList)
    
    
    def dirWithScore(self,query):
        return self._queryList(query,self.dirList)
 
    def _queryList(self,query,theList):
        #generic method to return the member of the list with the highest score
        #score is determined by matching words in the query
        #return the filename in the repository with the best score according to query.  None if score of 0
        #if there is a tie it returns the first instance of the highest score (or whatever max() returns)
        #scoring: exact matches get 10 points, partial matches get 1 point
        scoreList = [0]*len(theList)
        masterList = [[i,h] for i,h in zip(scoreList,theList)]
        #FUTURE check zips, or someother way to merge the lists
        
        for match in re.finditer('\w+',query):
                #print(match.group())
            lmatch = match.group().lower()  #search should be case insensitive
            self._scoreName(lmatch,masterList)
            
        return self._highscore(masterList)
    
    #score a match group versus all entries in [1] in the masterList, adding score to [0] of masterlist
    #master list should be a list of tuples [(int,string)]
    #masterList is mutated by this method
    def _scoreName(self,match,masterList):
        for aTuple in masterList:
            lname = aTuple[1].lower() #search should be case insensitive
            if match == lname:
                aTuple[0]+= 10 #with properly named directories these should be all you get
            elif re.search(match, lname): #backup, for similar names, less score
                aTuple[0]+= 1


    def _highscore(self,masterList):
        masterList.sort()
        if masterList[-1][0] == 0:
            return None
        else:
            return masterList[-1][1]
    

 
 
 