'''
CompilationEngine: given input from JackTokenizer, it emits XML file according to
Jack Grammar
'''
class CompilationEngine:
    def __init__(self, jackTokenizedFileName, tokenDictionary):
        self.jackTokenizedFileName = jackTokenizedFileName
        self.TOKEN_DICTIONARY = tokenDictionary

    def _readFileAndParseTokens(self):
        jackTokenList = []

        with open(self.jackTokenizedFileName, mode="r") as f:
            lines = f.read().splitlines()[1:-1]

            for line in lines:
                jackTokenList.append(line)

        return jackTokenList
                
    def _parseJackTokens(self, tokenizedList):
        def appendToParsedList(blank):
            nonlocal cursorPosition

            if cursorPosition < len(tokenizedList):
                jackTokenParsedList.append(" " * (blank  + 2) + tokenizedList[cursorPosition])
                cursorPosition += 1

        def getTagContent(tag):
            return tag.split(" ")[1]

        '''
        format: 
        'class' className '{' classVarDec* subroutineDec* '}'
        '''
        def compileClass(blank):
            nonlocal cursorPosition

            # <class>
            jackTokenParsedList.append(" " * blank + "<class>")

            # 'class' className '{'
            for _ in range(3):
                appendToParsedList(blank)
            
            # classVarDec*
            while cursorPosition < len(tokenizedList) and \
                    ("static" in getTagContent(tokenizedList[cursorPosition]) or \
                    "field" in getTagContent(tokenizedList[cursorPosition])):
                compielClassVarDec(blank + 2)
            
            # subroutineDec*
            while cursorPosition < len(tokenizedList) and \
                    ("constructor" in getTagContent(tokenizedList[cursorPosition]) or \
                    "function" in getTagContent(tokenizedList[cursorPosition]) or \
                    "method" in getTagContent(tokenizedList[cursorPosition])):
                compileSubroutine(blank + 2)

            # }
            appendToParsedList(blank)

            # </class>
            jackTokenParsedList.append(" " * blank + "</class>")

        '''
        format: 
        ('static'|'field') type varName (',' varName)* ';'
        '''
        def compielClassVarDec(blank):
            nonlocal cursorPosition

            # <classVarDec>
            jackTokenParsedList.append(" " * blank + "<classVarDec>")

            # ('static'|'field')
            appendToParsedList(blank)

            # type varName (',' varName)*
            while cursorPosition < len(tokenizedList) and \
                ";" not in getTagContent(tokenizedList[cursorPosition]):
                appendToParsedList(blank)

            # ;
            appendToParsedList(blank)

            # </classVarDec>
            jackTokenParsedList.append(" " * blank + "</classVarDec>")

        '''
        format: 
        ('constructor'|'function'|'method') ('void'|type) subroutineName '(' parameterList ')' subroutineBody
        '''
        def compileSubroutine(blank):
            nonlocal cursorPosition

            # <subroutineDec>
            jackTokenParsedList.append(" " * blank + "<subroutineDec>")
            
            # ('constructor'|'function'|'method') ('void'|type) subroutineName '('
            for _ in range(4):
                appendToParsedList(blank)
            
            # parameterList
            compileParameterList(blank + 2)

            # )
            appendToParsedList(blank)

            # subroutineBody
            compileSubroutineBody(blank + 2)

            # </subroutineDec>
            jackTokenParsedList.append(" " * blank + "</subroutineDec>")
        
        '''
        format:
        '{' varDec* statements '}'
        '''
        def compileSubroutineBody(blank):
            nonlocal cursorPosition

            # <subroutineBody>
            jackTokenParsedList.append(" " * blank + "<subroutineBody>")

            # {
            appendToParsedList(blank)

            # varDec*
            while cursorPosition < len(tokenizedList) and \
                    ("let" not in getTagContent(tokenizedList[cursorPosition]) and \
                    "if" not in getTagContent(tokenizedList[cursorPosition]) and \
                    "while" not in getTagContent(tokenizedList[cursorPosition]) and \
                    "do" not in getTagContent(tokenizedList[cursorPosition]) and \
                    "return" not in getTagContent(tokenizedList[cursorPosition])):
                compileVarDec(blank + 2)

            # statements
            if cursorPosition < len(tokenizedList) and \
                    ("let" in getTagContent(tokenizedList[cursorPosition]) or \
                    "if" in getTagContent(tokenizedList[cursorPosition]) or \
                    "while" in getTagContent(tokenizedList[cursorPosition]) or \
                    "do" in getTagContent(tokenizedList[cursorPosition]) or \
                    "return" in getTagContent(tokenizedList[cursorPosition])):
                compileStatements(blank + 2)

            # }
            appendToParsedList(blank)
            # </subroutineBody>
            jackTokenParsedList.append(" " * blank + "</subroutineBody>")

        '''
        format: 
        ((type varName) (',' type varName)*)
        '''
        def compileParameterList(blank):
            nonlocal cursorPosition

            # <parameterList>
            jackTokenParsedList.append(" " * blank + "<parameterList>")

            while cursorPosition < len(tokenizedList) and \
                ")" not in getTagContent(tokenizedList[cursorPosition]):
                # type varName
                for _ in range(2):
                    appendToParsedList(blank)

                # ,
                if cursorPosition < len(tokenizedList) and \
                    "," in getTagContent(tokenizedList[cursorPosition]):
                    appendToParsedList(blank)

            # </parameterList>
            jackTokenParsedList.append(" " * blank + "</parameterList>")

        '''
        format: 
        'var' type varName (',' varName)* ';'
        '''
        def compileVarDec(blank):
            nonlocal cursorPosition
            
            # <varDec>
            jackTokenParsedList.append(" " * blank + "<varDec>")

            # 'var' type varName
            for _ in range(3):
                appendToParsedList(blank)

            # (',' varName)*
            while cursorPosition < len(tokenizedList) and \
                ";" not in getTagContent(tokenizedList[cursorPosition]):
                # ',' varName
                for _ in range(2):
                    appendToParsedList(blank)

            # ;
            appendToParsedList(blank)

            # </varDec>
            jackTokenParsedList.append(" " * blank + "</varDec>")
        
        '''
        format:
        letStatement, ifStatement, whileStatement, doStatement, returnStatement 
        '''
        def compileStatements(blank):
            nonlocal cursorPosition

            # <statements>
            jackTokenParsedList.append(" " * blank + "<statements>")

            while cursorPosition < len(tokenizedList) and \
                "}" not in getTagContent(tokenizedList[cursorPosition]):
                if cursorPosition < len(tokenizedList) and \
                    "let" in getTagContent(tokenizedList[cursorPosition]):
                    compileLet(blank + 2)
                elif cursorPosition < len(tokenizedList) and \
                    "if" in getTagContent(tokenizedList[cursorPosition]):
                    compileIf(blank + 2)
                elif cursorPosition < len(tokenizedList) and \
                    "while" in getTagContent(tokenizedList[cursorPosition]):
                    compileWhile(blank + 2)
                elif cursorPosition < len(tokenizedList) and \
                    "do" in getTagContent(tokenizedList[cursorPosition]):
                    compileDo(blank + 2)
                elif cursorPosition < len(tokenizedList) and \
                    "return" in getTagContent(tokenizedList[cursorPosition]): 
                    compileReturn(blank + 2)
            
            # </statements>
            jackTokenParsedList.append(" " * blank + "</statements>")

        '''
        format:
        'do' subroutineCall ';'
        '''
        def compileDo(blank):
            nonlocal cursorPosition
            
            # <doStatement>
            jackTokenParsedList.append(" " * blank + "<doStatement>")

            # do
            appendToParsedList(blank)

            # subroutineCall
            compileSubroutineCall(blank)          

            # ;
            appendToParsedList(blank)

            # </doStatement>
            jackTokenParsedList.append(" " * blank + "</doStatement>")

        '''
        format:
        subroutineName '(' expressionList ')' | (className | varName) '.' subroutineName '(' expressionList ')'
        '''
        def compileSubroutineCall(blank):
            nonlocal cursorPosition

            # (className|varName)'.'
            if cursorPosition + 1< len(tokenizedList) and \
                "." in getTagContent(tokenizedList[cursorPosition + 1]):
                for _ in range(2):
                    appendToParsedList(blank)
            
            # subroutineName '('
            for _ in range(2):
                appendToParsedList(blank)
            # expressionList
            compileExpressionList(blank + 2)
            # )
            appendToParsedList(blank)

        '''
        format: 
        'let' varName ('[' expression ']')? '=' expression ';'
        '''
        def compileLet(blank):
            nonlocal cursorPosition
            
            # <letStatement>
            jackTokenParsedList.append(" " * blank + "<letStatement>")

            # let varName
            for _ in range(2):
                appendToParsedList(blank)

            # ('[' expression ']')?
            if cursorPosition < len(tokenizedList) and \
                "[" in getTagContent(tokenizedList[cursorPosition]):
                # [
                appendToParsedList(blank)
                # expression
                compileExpression(blank + 2)
                # ]
                appendToParsedList(blank)
            
            # =
            appendToParsedList(blank)

            # expression
            compileExpression(blank + 2)

            # ;
            appendToParsedList(blank)

            # </letStatement>
            jackTokenParsedList.append(" " * blank + "</letStatement>")

        '''
        format:
        'while' '(' expression ')' '{' statements '}'
        '''
        def compileWhile(blank):
            nonlocal cursorPosition

            # <whileStatement>
            jackTokenParsedList.append(" " * blank + "<whileStatement>")

            # while (
            for _ in range(2):
                appendToParsedList(blank)

            # expression
            compileExpression(blank + 2)

            # ) {
            for _ in range(2):
                appendToParsedList(blank)
            
            # statements
            compileStatements(blank + 2)
            
            # }
            appendToParsedList(blank)

            # </whileStatement>
            jackTokenParsedList.append(" " * blank + "</whileStatement>")
            
        '''
        format:
        'return' expression? ';'
        '''
        def compileReturn(blank):
            nonlocal cursorPosition
            
            # <returnStatement>
            jackTokenParsedList.append(" " * blank + "<returnStatement>")

            # return
            appendToParsedList(blank)

            # expression?
            if cursorPosition < len(tokenizedList) and \
                ";" not in getTagContent(tokenizedList[cursorPosition]):
                compileExpression(blank + 2)
            
            # ;
            appendToParsedList(blank)

            # </returnStatement>
            jackTokenParsedList.append(" " * blank + "</returnStatement>")

        '''
        format:
        'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
        '''
        def compileIf(blank):
            nonlocal cursorPosition
            
            # <ifStatement>
            jackTokenParsedList.append(" " * blank + "<ifStatement>")

            # if '('
            for _ in range(2):
                appendToParsedList(blank)
            # expression
            compileExpression(blank + 2)
            
            # ) {
            for _ in range(2):
                appendToParsedList(blank)
            
            # statements
            compileStatements(blank + 2)
            
            # }
            appendToParsedList(blank)

            # ('else' '{' statments '}')?
            if cursorPosition < len(tokenizedList) and \
                "else" in getTagContent(tokenizedList[cursorPosition]):
                # else {
                for _ in range(2):
                    appendToParsedList(blank)
                # statements
                compileStatements(blank + 2)
                # }
                appendToParsedList(blank)

            # </ifStatement>
            jackTokenParsedList.append(" " * blank + "</ifStatement>")
            
        '''
        format:
        term (op term)*
        '''
        def compileExpression(blank):
            nonlocal cursorPosition
            
            # <expression>
            jackTokenParsedList.append(" " * blank + "<expression>")

            # term
            compileTerm(blank + 2)

            # (op term)*
            while cursorPosition < len(tokenizedList) and \
                    ("+" in getTagContent(tokenizedList[cursorPosition]) or \
                    "-" in getTagContent(tokenizedList[cursorPosition]) or \
                    "*" in getTagContent(tokenizedList[cursorPosition]) or \
                    "/" in getTagContent(tokenizedList[cursorPosition]) or \
                    "&amp;" in getTagContent(tokenizedList[cursorPosition]) or \
                    "|" in getTagContent(tokenizedList[cursorPosition]) or \
                    "&lt;" in getTagContent(tokenizedList[cursorPosition]) or \
                    "&gt;" in getTagContent(tokenizedList[cursorPosition]) or \
                    "=" in getTagContent(tokenizedList[cursorPosition])):
                appendToParsedList(blank)
                compileTerm(blank + 2)

            # </expression>
            jackTokenParsedList.append(" " * blank + "</expression>")

        '''
        format:
        integerConstant | stringConstant | keywordConstant | varName |
        varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term
        '''
        def compileTerm(blank):
            nonlocal cursorPosition
            
            # <term>
            jackTokenParsedList.append(" " * blank + "<term>")

            # varName '[' expression ']'
            if cursorPosition + 1< len(tokenizedList) and \
                "[" in getTagContent(tokenizedList[cursorPosition + 1]):
                # varName '['
                for _ in range(2):
                    appendToParsedList(blank)
                # expression
                compileExpression(blank + 2)
                # ']'
                appendToParsedList(blank)
            # unaryOp term
            elif cursorPosition < len(tokenizedList) and \
                    ("-" in getTagContent(tokenizedList[cursorPosition]) or \
                    "~" in getTagContent(tokenizedList[cursorPosition])):
                # unaryOp
                appendToParsedList(blank)
                # term
                compileTerm(blank + 2)
            # '(' expression ')'
            elif cursorPosition < len(tokenizedList) and \
                "(" in getTagContent(tokenizedList[cursorPosition]):
                # '('
                appendToParsedList(blank)
                # expression
                compileExpression(blank + 2)
                # ')'
                appendToParsedList(blank)
            # subroutineCall
            elif cursorPosition + 1 < len(tokenizedList) and \
                    ("(" in getTagContent(tokenizedList[cursorPosition + 1]) or \
                    "." in getTagContent(tokenizedList[cursorPosition + 1])):
                compileSubroutineCall(blank)
            # integerConstant | stringConstant | keywordConstant | varName
            else:
                appendToParsedList(blank)

            # </term>
            jackTokenParsedList.append(" " * blank + "</term>")

        '''
        format:
        (expression (',' expression)*)?
        '''
        def compileExpressionList(blank):
            nonlocal cursorPosition
            
            # <expressionList>
            jackTokenParsedList.append(" " * blank + "<expressionList>")

            while cursorPosition < len(tokenizedList) and \
                ")" not in getTagContent(tokenizedList[cursorPosition]):
                # expression
                compileExpression(blank + 2)

                # (',' expression)*
                while cursorPosition < len(tokenizedList) and \
                    "," in getTagContent(tokenizedList[cursorPosition]):
                    appendToParsedList(blank)
                    compileExpression(blank + 2)

            # </expressionList>
            jackTokenParsedList.append(" " * blank + "</expressionList>")

        jackTokenParsedList = []
        cursorPosition = 0
        blank = 0 # number of blank space

        compileClass(blank)

        return jackTokenParsedList

    def parseTokens(self):
        # read file and generate token list
        jackTokenList = self._readFileAndParseTokens()

        # parse token list and generate token-parsed list
        jackTokenParsedList = self._parseJackTokens(jackTokenList)

        return jackTokenParsedList
