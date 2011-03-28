import re

class Criterion:
    """
    an abstract object that returns a score based on abitrary criteria applied to two strings
    """
    def __init__(self):
        
        pass
    
    def score(self,query,target):
        """
        process the query so it may be assessed, return final score OR flags 'match' or 'kill'
        subclasses may implement this method
        default behaviour is to not process the query and simply assess it
        """
        return self._assess(query,target)
    
    def _assess(self,query,target):
        """
        private method assess the criterion and return a score to self.score
        
        subclasses should implement this method
        """
        return 0
    
    
    

class AlphaNumericCriterion(Criterion):
    """
    basic criterion that splits the query into alphanumeric chunks
    meant to be subclassed as the criterion is not very useful
    """
    def score(self,query,target):
        """
        preprocess the query by splitting it into alphanumeric chunks and then assess the pieces versus target
        
        may be overloaded
        """
        score = 0
        #chop the query into alpha numeric chunks for easy comparison
        for match in re.finditer(r"\w+",query):
            response = self._assess(match.group(),target)
            if response == 'kill': #definitely not a match, kill comparison all the way up
                return 'kill'
            elif response == 'match':#definitely a match kill comparison all the way up
                return 'match'
            else:
                score += response #score
        return score

    
    def _assess(self,query,target):
        """
        
        default if query == target return match
        """
        
        if query == target:
            return 'match'
        else:
            return 0
        

class ExactSimilarCriterion(AlphaNumericCriterion):
    """
    10 points on an exact match (of a chunk) and 1 point on a partial match
    """
    
    def _assess(self,query,target):
        if query == target:
            return 10 
        elif re.search(query, target): 
            return 1
        else:
            return 0

class RequiredCriterion(Criterion):
    """
    this criterion requires a regular expression pattern on construction.
    This class does not need to process the query.
    """
    def __init__(self,requirement):
        self.reqPattern = requirement
    
    
    def _assess(self,query,target):
        """
        find self.reqPattern in both the query and the challenge
        if it does not exist or are not the same return 'kill'
        otherwise return 0 (no score)
        """
        match1 = re.search(self.reqPattern,query)
        match2 = re.search(self.reqPattern,target)
        if not match1 or not match2 or match1.group() != match2.group():
            return 'kill'
        
        return 0
        
class TvSeasonEpisodeCriterion(Criterion):
    """
    a criterion that specifically matches TV show season/episode strings
    current formats: (s)##x(e)## (02x21) and S##E## (s02e21)
    either format will match the other as long as the numbers are the same
    """
    
    def _assess(self,query,target):
        match1 = None
        match2 = None
        patternList = [r'(s|S)(?P<season>\d+)(e|E)(?P<episode>\d+)',r'(?P<season>\d+)(x|X)(?P<episode>\d+)']
        for pattern in patternList:
            if not match1: #process only if a match hasn't been found
                match1 = re.search(pattern,query)
            if not match2:
                match2 = re.search(pattern,target)
            
        if not match1 or not match2: return 'kill' #required pattern was not found, kill
        if match1.group('season') != match2.group('season') or match1.group('episode') != match2.group('episode'):
            #pattern was found but they aren't the same..kill
            return 'kill'
        
        return 0 #patterns were found and matched
        
        
    