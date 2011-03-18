from subtitleOrganizer import subtitleOrganizer 
from repository import Repository 

subRepository = 't:\\subtitles\\'
#subRepository = '/Users/xamn/pythonplay/SubRep/'
movieShack = 't:\\Movieshack\\'
#movieShack =  '/Users/xamn/pythonplay/Movieshack/'

a = subtitleOrganizer(subRepository,movieShack)

for i in a.organize():
    print(i)
    

#a.organize()
"""
a = Repository(movieShack)
b = a.fileWithScore('shigeko')

for i in a.iterOverDirs():
    print(i)
"""    
    


