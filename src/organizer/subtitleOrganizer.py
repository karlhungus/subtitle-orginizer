from repository import *
import shutil

class subtitleOrganizer:
    def __init__(self,subRep,movRep):
        self.subtitleRepository = Repository(subRep)
        self.movieRepository = TVRepository(movRep)
        
        
    def organize(self):
        #iterate over the files in the subtitleRepository
        #find the directory they belong in and FUTURE move them there.
        #FUTURE find the matching movie file and rename the subtitlefile
        
        for subFile in self.subtitleRepository.iterOverFiles():
            target = self.movieRepository.placeFile(subFile)
            if target:
                self.transferSub(self.subtitleRepository.rootDir,subFile,target[0],target[1])
        
    
    def transferSub(self,sourceDir,sourceFile,destDir,destFile):
        """
        sourceDir is location of sourceFile
        destDir is location of destFile
        renames sourceFile to match destfile (minus extension) then moves it to destdir
        """
        newName = destFile[:-3] + 'srt'

        shutil.move(sourceDir + sourceFile,destDir + newName) 