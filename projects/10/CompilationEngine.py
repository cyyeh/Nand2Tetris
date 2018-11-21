'''
CompilationEngine: given input from JackTokenizer, it emits XML file according to
Jack Grammar
'''
class CompilationEngine:
    def __init__(self, jackTokenizedFileName, tokenDictionary):
        self.jackTokenizedFileName = jackTokenizedFileName
        self.TOKEN_DICTIONARY = tokenDictionary

    def _readFileAndParseTokens(self):
        pass

    def _parseJackTokens(self, tokenizedList):
        pass

    def parseTokens(self):
        # read file and generate token list
        jackTokenList = self._readFileAndParseTokens()

        # parse token list and generate token-parsed list
        jackTokenParsedList = self._parseJackTokens(jackTokenList)

        return jackTokenParsedList
