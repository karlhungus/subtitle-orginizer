import urllib.request

class SubtitleDownloader():
    def __init__(self,url):
        self.url = url
        
    def getSubtitlesFor(self,aList):
        #Get srt's for aList where aList is a  list of dir names
        urllib.request.urlopen(self.url, None)
