from subtitleOrganizer import subtitleOrganizer 
from criterion import *

subRepository = 't:\\subtitles\\'
#subRepository = '/Users/xamn/pythonplay/SubRep/'
movieShack = 't:\\Movieshack\\'
#movieShack =  '/Users/xamn/pythonplay/Movieshack/'


a = subtitleOrganizer(subRepository,movieShack)

for i in a.organize():
    print(i)
    




"""
a = TvSeasonEpisodeCriterion()

b = '23x11'
c = '23x11'

print(a.score('23x11','23x11')) #m
print(a.score('s23e11','s23e11')) #m
print(a.score('23X11','23x11')) #m
print(a.score('S23E11','s23e11')) #m
print(a.score('23x11','S23E11')) #m
print(a.score('22x11','23x11')) #kill
print(a.score('23x10','23x11')) #kill
print(a.score('hello','23x11')) #kill
print(a.score('23x11','hello')) #kill
"""

