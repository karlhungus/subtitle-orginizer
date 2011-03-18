from repository import Repository 

class subtitleOrganizer:
    def __init__(self,subRep,movRep):
        self.subtitleRepository = Repository(subRep)
        self.movieRepository = Repository(movRep)
        
        
    def organize(self):
        #iterate over the files in the subtitleRepository
        #find the directory they belong in and FUTURE move them there.
        #FUTURE find the matching movie file and rename the subtitlefile
        
        for subFile in self.subtitleRepository.iterOverFiles():
            yield (subFile, self.movieRepository.dirWithScore(subFile))
            