# VMTranslator translates VM code(compiled from Jack programming language using Jack compiler)
# into Hack assembly

import sys
import os

# read vm code file and parse content into a list
def parseVMCodeFile(file):
    vmCodeList = []

    with open(file, mode='r') as f:
        lines = f.read().splitlines()
        for line in lines:
            if not line: # ignore empty lines
                continue
            elif line[0:2] == '//': # ignore lines with comment comes first
                continue
            else:
                if '//' in line:
                    line = line.split('//')[0]
                    vmCodeList.append(line.strip()) # ignore comments inside a line
                else:
                    vmCodeList.append(line.strip())
    
    return vmCodeList

# main algorithm for generating Hack assembly program into a list
def generateHackAssembly(vmCodeList, fileName, addComment, translationHelperData):
    # transfer VM add command into Hack assembly code
    def transferAdd():
        hackAssemblyElementList = []

        # generate Hack assembly code
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M-1')
        hackAssemblyElementList.append('A=M')
        hackAssemblyElementList.append('D=M')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M-1')
        hackAssemblyElementList.append('A=M')
        hackAssemblyElementList.append('M=D+M')         
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M+1')

        return hackAssemblyElementList
    
    # transfer VM sub command into Hack assembly code
    def trasferSub():
        hackAssemblyElementList = []

        # generate Hack assembly code
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M-1')
        hackAssemblyElementList.append('A=M')
        hackAssemblyElementList.append('D=M')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M-1')
        hackAssemblyElementList.append('A=M')
        hackAssemblyElementList.append('M=M-D')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M+1')

        return hackAssemblyElementList

    # transfer VM neg command into Hack assembly code
    def transferNeg():
        hackAssemblyElementList = []

        # generate Hack assembly code
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M-1')
        hackAssemblyElementList.append('A=M')
        hackAssemblyElementList.append('D=-M')            
        hackAssemblyElementList.append('M=D')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M+1')

        return hackAssemblyElementList

    # transfer VM eq command into Hack assembly code
    def transferEq(customLabelIndex):
        hackAssemblyElementList = []

        # generate Hack assembly code
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M-1')
        hackAssemblyElementList.append('A=M')
        hackAssemblyElementList.append('D=M')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M-1')
        hackAssemblyElementList.append('A=M')
        hackAssemblyElementList.append('D=D-M')
        hackAssemblyElementList.append('@EQUAL'+ customLabelIndex)
        hackAssemblyElementList.append('D;JEQ')
        hackAssemblyElementList.append('D=0')
        hackAssemblyElementList.append('@FINAL'+ customLabelIndex)
        hackAssemblyElementList.append('0;JEQ')
        hackAssemblyElementList.append('(EQUAL'+ customLabelIndex +')')
        hackAssemblyElementList.append('D=-1')
        hackAssemblyElementList.append('(FINAL'+ customLabelIndex +')')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('A=M')
        hackAssemblyElementList.append('M=D')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M+1')

        return hackAssemblyElementList

    # transfer VM gt command into Hack assembly code
    def transferGt(customLabelIndex):
        hackAssemblyElementList = []

        # generate Hack assembly code
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M-1')
        hackAssemblyElementList.append('A=M')
        hackAssemblyElementList.append('D=M')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M-1')
        hackAssemblyElementList.append('A=M')
        hackAssemblyElementList.append('D=M-D')
        hackAssemblyElementList.append('@GREATER_THAN'+ customLabelIndex)
        hackAssemblyElementList.append('D;JGT')
        hackAssemblyElementList.append('D=0')
        hackAssemblyElementList.append('@END'+ customLabelIndex)
        hackAssemblyElementList.append('0;JEQ')
        hackAssemblyElementList.append('(GREATER_THAN'+ customLabelIndex +')')
        hackAssemblyElementList.append('D=-1')
        hackAssemblyElementList.append('(END'+ customLabelIndex +')')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('A=M')        
        hackAssemblyElementList.append('M=D')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M+1')

        return hackAssemblyElementList

    # transfer VM lt command into Hack assembly code
    def transferLt(customLabelIndex):
        hackAssemblyElementList = []

        # generate Hack assembly code
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M-1')
        hackAssemblyElementList.append('A=M')
        hackAssemblyElementList.append('D=M')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M-1')
        hackAssemblyElementList.append('A=M')
        hackAssemblyElementList.append('D=M-D')
        hackAssemblyElementList.append('@LESS_THAN'+ customLabelIndex)
        hackAssemblyElementList.append('D;JLT')
        hackAssemblyElementList.append('D=0')
        hackAssemblyElementList.append('@END'+ customLabelIndex)
        hackAssemblyElementList.append('0;JEQ')
        hackAssemblyElementList.append('(LESS_THAN'+ customLabelIndex +')')
        hackAssemblyElementList.append('D=-1')
        hackAssemblyElementList.append('(END'+ customLabelIndex +')')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('A=M')        
        hackAssemblyElementList.append('M=D')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M+1')

        return hackAssemblyElementList

    # transfer VM and command into Hack assembly code
    def transferAnd():
        hackAssemblyElementList = []

        # generate Hack assembly code
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M-1')
        hackAssemblyElementList.append('A=M')
        hackAssemblyElementList.append('D=M')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M-1')
        hackAssemblyElementList.append('A=M')
        hackAssemblyElementList.append('D=D&M')       
        hackAssemblyElementList.append('M=D')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M+1')

        return hackAssemblyElementList

    # transfer VM or command into Hack assembly code
    def transferOr():
        hackAssemblyElementList = []

        # generate Hack assembly code
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M-1')
        hackAssemblyElementList.append('A=M')
        hackAssemblyElementList.append('D=M')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M-1')
        hackAssemblyElementList.append('A=M')
        hackAssemblyElementList.append('D=D|M')
        hackAssemblyElementList.append('M=D')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M+1')

        return hackAssemblyElementList

    # transfer VM not command into Hack assembly code
    def transferNot():
        hackAssemblyElementList = []

        # generate Hack assembly code
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M-1')
        hackAssemblyElementList.append('A=M')
        hackAssemblyElementList.append('D=!M')
        hackAssemblyElementList.append('M=D')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M+1')

        return hackAssemblyElementList

    # transfer VM push command into Hack assembly code
    def transferPush(memorySegmentDict, memorySegmentAccess, fileName, offset):
        hackAssemblyElementList = []

        # generate Hack assembly code
        if 'constant' in parsedCode:
            # *SP = i, SP++
            hackAssemblyElementList.append('@' + offset)
            hackAssemblyElementList.append('D=A')
            hackAssemblyElementList.append('@SP')
            hackAssemblyElementList.append('A=M')
            hackAssemblyElementList.append('M=D')
            hackAssemblyElementList.append('@SP')
            hackAssemblyElementList.append('M=M+1')            
        elif memorySegmentAccess in memorySegmentDict.keys():
            # addr = segmentPointer + i, *SP = *addr, SP++
            hackAssemblyElementList.append('@' + offset)
            hackAssemblyElementList.append('D=A')
            hackAssemblyElementList.append('@' + memorySegmentDict[memorySegmentAccess])
            hackAssemblyElementList.append('A=D+M')
            hackAssemblyElementList.append('D=M')
            hackAssemblyElementList.append('@SP')
            hackAssemblyElementList.append('A=M')
            hackAssemblyElementList.append('M=D')
            hackAssemblyElementList.append('@SP')
            hackAssemblyElementList.append('M=M+1')
        elif 'temp' in parsedCode:
            # addr = 5 + i, *SP = *addr, SP++
            hackAssemblyElementList.append('@' + offset)
            hackAssemblyElementList.append('D=A')
            hackAssemblyElementList.append('@5')
            hackAssemblyElementList.append('A=D+A')
            hackAssemblyElementList.append('D=M')
            hackAssemblyElementList.append('@SP')
            hackAssemblyElementList.append('A=M')
            hackAssemblyElementList.append('M=D')
            hackAssemblyElementList.append('@SP')
            hackAssemblyElementList.append('M=M+1')
        elif 'pointer' in parsedCode:
            # *SP = THIS/THAT, SP++
            if offset == '0':
                accessor = 'THIS'
            else:
                accessor = 'THAT'
            
            hackAssemblyElementList.append('@' + accessor)
            hackAssemblyElementList.append('D=M')
            hackAssemblyElementList.append('@SP')
            hackAssemblyElementList.append('A=M')
            hackAssemblyElementList.append('M=D')
            hackAssemblyElementList.append('@SP')
            hackAssemblyElementList.append('M=M+1')
        elif 'static' in parsedCode:
            hackAssemblyElementList.append('@' + fileName + '.' + offset)
            hackAssemblyElementList.append('D=M')
            hackAssemblyElementList.append('@SP')
            hackAssemblyElementList.append('A=M')
            hackAssemblyElementList.append('M=D')
            hackAssemblyElementList.append('@SP')
            hackAssemblyElementList.append('M=M+1')            
    
        return hackAssemblyElementList

    # transfer VM pop command into Hack assembly code
    def transferPop(memorySegmentDict, memorySegmentAccess, fileName, offset):
        hackAssemblyElementList = []

        # generate Hack assembly code
        if memorySegmentAccess in memorySegmentDict.keys():
            # addr = segmentPointer + i, SP--, *addr = *SP
            hackAssemblyElementList.append('@' + offset)
            hackAssemblyElementList.append('D=A')
            hackAssemblyElementList.append('@' + memorySegmentDict[memorySegmentAccess])
            hackAssemblyElementList.append('D=D+M')
            hackAssemblyElementList.append('@frame')
            hackAssemblyElementList.append('M=D')
            hackAssemblyElementList.append('@SP')
            hackAssemblyElementList.append('M=M-1')
            hackAssemblyElementList.append('A=M')
            hackAssemblyElementList.append('D=M')
            hackAssemblyElementList.append('@frame')
            hackAssemblyElementList.append('A=M')
            hackAssemblyElementList.append('M=D')
        elif 'temp' in parsedCode:
            # addr = 5 + i, SP--, *addr = *SP
            hackAssemblyElementList.append('@' + offset)
            hackAssemblyElementList.append('D=A')
            hackAssemblyElementList.append('@5')
            hackAssemblyElementList.append('D=D+A')
            hackAssemblyElementList.append('@frame')
            hackAssemblyElementList.append('M=D')
            hackAssemblyElementList.append('@SP')
            hackAssemblyElementList.append('M=M-1')
            hackAssemblyElementList.append('A=M')
            hackAssemblyElementList.append('D=M')
            hackAssemblyElementList.append('@frame')
            hackAssemblyElementList.append('A=M')
            hackAssemblyElementList.append('M=D')
        elif 'pointer' in parsedCode:
            # SP--, THIS/THAT = *SP
            if offset == '0':
                accessor = 'THIS'
            else:
                accessor = 'THAT'
            
            hackAssemblyElementList.append('@SP')
            hackAssemblyElementList.append('M=M-1')
            hackAssemblyElementList.append('A=M')
            hackAssemblyElementList.append('D=M')
            hackAssemblyElementList.append('@' + accessor)
            hackAssemblyElementList.append('M=D')
        elif 'static' in parsedCode:
            hackAssemblyElementList.append('@SP')
            hackAssemblyElementList.append('M=M-1')
            hackAssemblyElementList.append('A=M')
            hackAssemblyElementList.append('D=M')
            hackAssemblyElementList.append('@' + fileName + '.' + offset)
            hackAssemblyElementList.append('M=D')
    
        return hackAssemblyElementList

    # transfer VM label command into Hack assembly code
    def transferLabel(labelName, functionList):
        hackAssemblyElementList = []            

        # generate Hack assembly code
        if len(functionList) > 0:
            functionName = functionList[-1]
            hackAssemblyElementList.append('(' + functionName + '$' + labelName + ')')
        else:
            hackAssemblyElementList.append('('+ labelName + ')')
        
        return hackAssemblyElementList

    # transfer VM if-goto command into Hack assembly code
    def transferIfGoto(labelName, functionList):
        hackAssemblyElementList = []

        # generate Hack assembly code
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M-1')
        hackAssemblyElementList.append('A=M')
        hackAssemblyElementList.append('D=M')
        if len(functionList) > 0:
            functionName = functionList[-1]
            hackAssemblyElementList.append('@' + functionName + '$' + labelName)
        else:
            hackAssemblyElementList.append("@" + labelName)
        hackAssemblyElementList.append("D;JNE")

        return hackAssemblyElementList

    # transfer VM goto command into Hack assembly code
    def transferGoto(code, functionList):
        hackAssemblyElementList = []

        # generate Hack assembly code
        if len(functionList) > 0:
            functionName = functionList[-1]
            hackAssemblyElementList.append('@' + functionName + '$' + labelName)
        else:
            hackAssemblyElementList.append("@" + labelName)
        hackAssemblyElementList.append("0;JMP")

        return hackAssemblyElementList

    # transfer VM function command into Hack assembly code
    def transferFunction(functionName, numberOfVariables):
        hackAssemblyElementList = []

        # generate Hack assembly code
        hackAssemblyElementList.append("(" + functionName +")")
        for _ in range(numberOfVariables):
            hackAssemblyElementList.append('@0')
            hackAssemblyElementList.append('D=A')
            hackAssemblyElementList.append('@SP')
            hackAssemblyElementList.append('A=M')
            hackAssemblyElementList.append('M=D')
            hackAssemblyElementList.append('@SP')
            hackAssemblyElementList.append('M=M+1')

        return hackAssemblyElementList

    # transfer VM return command into Hack assembly code
    def transferReturn():
        hackAssemblyElementList = []

        # generate Hack assembly code
        # endFrame = LCL // endFrame is a temporary variable
        hackAssemblyElementList.append("@LCL")
        hackAssemblyElementList.append("D=M")
        hackAssemblyElementList.append("@frame")
        hackAssemblyElementList.append("M=D")
        # retAddr = *(endFrame - 5) // gets the return address
        hackAssemblyElementList.append("@5")
        hackAssemblyElementList.append('D=D-A')
        hackAssemblyElementList.append('A=D')
        hackAssemblyElementList.append("D=M")
        hackAssemblyElementList.append("@return")
        hackAssemblyElementList.append("M=D")
        # *ARG = pop()  // repositions the return value for the caller
        hackAssemblyElementList.append("@SP")
        hackAssemblyElementList.append("M=M-1")
        hackAssemblyElementList.append("A=M")
        hackAssemblyElementList.append("D=M")
        hackAssemblyElementList.append("@ARG")
        hackAssemblyElementList.append("A=M")
        hackAssemblyElementList.append("M=D")
        # SP = ARG + 1 // repositions SP of the caller
        hackAssemblyElementList.append("@ARG")
        hackAssemblyElementList.append("D=M+1")
        hackAssemblyElementList.append("@SP")
        hackAssemblyElementList.append("M=D")
        # THAT = *(endFrame - 1) // restores THAT of the caller
        hackAssemblyElementList.append("@frame")
        hackAssemblyElementList.append("D=M")
        hackAssemblyElementList.append("@1")
        hackAssemblyElementList.append('D=D-A')
        #hackAssemblyElementList.append('D=D-1')
        hackAssemblyElementList.append('A=D')
        hackAssemblyElementList.append("D=M")
        hackAssemblyElementList.append("@THAT")
        hackAssemblyElementList.append("M=D")
        # THIS = *(endFrame - 2) // restores THIS of the caller
        hackAssemblyElementList.append("@frame")
        hackAssemblyElementList.append("D=M")
        hackAssemblyElementList.append("@2")
        hackAssemblyElementList.append('D=D-A')        
        hackAssemblyElementList.append('A=D')
        hackAssemblyElementList.append("D=M")
        hackAssemblyElementList.append("@THIS")
        hackAssemblyElementList.append("M=D")
        # ARG = *(endFrame - 3) // restores ARG of the caller
        hackAssemblyElementList.append("@frame")
        hackAssemblyElementList.append("D=M")
        hackAssemblyElementList.append("@3")
        hackAssemblyElementList.append('D=D-A')            
        hackAssemblyElementList.append('A=D')
        hackAssemblyElementList.append("D=M")
        hackAssemblyElementList.append("@ARG")
        hackAssemblyElementList.append("M=D")
        # LCL = *(endFrame - 4) // restores LCL of the caller
        hackAssemblyElementList.append("@frame")
        hackAssemblyElementList.append("D=M")
        hackAssemblyElementList.append("@4")
        hackAssemblyElementList.append('D=D-A')            
        hackAssemblyElementList.append('A=D')
        hackAssemblyElementList.append("D=M")
        hackAssemblyElementList.append("@LCL")
        hackAssemblyElementList.append("M=D")        
        # goto retAddr // goes to return address in the caller's code
        hackAssemblyElementList.append("@return")
        hackAssemblyElementList.append("A=M")
        hackAssemblyElementList.append("0;JMP")

        return hackAssemblyElementList

    # transfer VM call command into Hack assembly code
    def transferCall(functionName, numberOfArguments, functionLabelIndex):
        hackAssemblyElementList = []

        # generate Hack assembly code
        # push return address
        hackAssemblyElementList.append('@'+ functionName + '$ret.' + functionLabelIndex)
        hackAssemblyElementList.append('D=A')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('A=M')
        hackAssemblyElementList.append('M=D')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M+1') 
        # push LCL
        hackAssemblyElementList.append('@LCL')
        hackAssemblyElementList.append('D=M')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('A=M')
        hackAssemblyElementList.append('M=D')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M+1')
        # push ARG
        hackAssemblyElementList.append('@ARG')
        hackAssemblyElementList.append('D=M')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('A=M')
        hackAssemblyElementList.append('M=D')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M+1')
        # push THIS
        hackAssemblyElementList.append('@THIS')
        hackAssemblyElementList.append('D=M')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('A=M')
        hackAssemblyElementList.append('M=D')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M+1') 
        # push THAT
        hackAssemblyElementList.append('@THAT')
        hackAssemblyElementList.append('D=M')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('A=M')
        hackAssemblyElementList.append('M=D')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M+1')
        # ARG = SP - 5 - number of arguments
        hackAssemblyElementList.append('D=M')
        hackAssemblyElementList.append("@" + str(5+numberOfArguments))
        hackAssemblyElementList.append('D=D-A')    
        hackAssemblyElementList.append('@ARG')
        hackAssemblyElementList.append('M=D')
        # LCL = SP
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('D=M')
        hackAssemblyElementList.append('@LCL')
        hackAssemblyElementList.append('M=D')
        # goto functionName
        hackAssemblyElementList.append('@' + functionName)
        hackAssemblyElementList.append('0;JMP')
        # (return address)
        hackAssemblyElementList.append('('+ functionName +'$ret.' + functionLabelIndex + ')')

        return hackAssemblyElementList

    hackAssemblyList = []
    memorySegmentDict = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}

    for code in vmCodeList:
        VMCommand = code.split(' ')[0]
        hackAssemblyElementList = ['//' + code] if addComment else []

        if 'add' == VMCommand:
            hackAssemblyElementList += transferAdd()
        elif 'sub' == VMCommand:
            hackAssemblyElementList += trasferSub()
        elif 'neg' == VMCommand:
            hackAssemblyElementList += transferNeg()
        elif 'eq' == VMCommand:
            hackAssemblyElementList += transferEq(str(translationHelperData["customLabelIndex"]))
            translationHelperData["customLabelIndex"] += 1
        elif 'gt' == VMCommand:
            hackAssemblyElementList += transferGt(str(translationHelperData["customLabelIndex"]))
            translationHelperData["customLabelIndex"] += 1
        elif 'lt' == VMCommand:
            hackAssemblyElementList += transferLt(str(translationHelperData["customLabelIndex"]))
            translationHelperData["customLabelIndex"] += 1
        elif 'and' == VMCommand:
            hackAssemblyElementList += transferAnd()
        elif 'or' == VMCommand:
            hackAssemblyElementList += transferOr()
        elif 'not' == VMCommand:
            hackAssemblyElementList += transferNot()
        elif 'push' == VMCommand:
            parsedCode = code.split(" ")
            memorySegmentAccess = parsedCode[1]
            offset = str(parsedCode[-1])

            hackAssemblyElementList += transferPush(memorySegmentDict, memorySegmentAccess, fileName, offset)
        elif 'pop' == VMCommand:
            parsedCode = code.split(" ")
            memorySegmentAccess = parsedCode[1]
            offset = str(parsedCode[-1])

            hackAssemblyElementList += transferPop(memorySegmentDict, memorySegmentAccess, fileName, offset)
        elif 'label' == VMCommand:
            parsedCode = code.split(" ")
            labelName = parsedCode[-1]

            hackAssemblyElementList += transferLabel(labelName, translationHelperData["functionList"])
        elif 'if-goto' == VMCommand:
            parsedCode = code.split(" ")
            labelName = parsedCode[-1]

            hackAssemblyElementList += transferIfGoto(labelName, translationHelperData["functionList"])
        elif 'goto' == VMCommand:
            parsedCode = code.split(" ")
            labelName = parsedCode[-1]

            hackAssemblyElementList += transferGoto(labelName, translationHelperData["functionList"])
        elif 'function' == VMCommand:
            parsedCode = code.split(" ")
            functionName = parsedCode[1]
            translationHelperData["functionList"].append(functionName)
            numberOfVariables = int(parsedCode[-1])

            hackAssemblyElementList += transferFunction(functionName, numberOfVariables)
        elif 'return' == VMCommand:
            hackAssemblyElementList += transferReturn()
        elif 'call' == VMCommand:
            parsedCode = code.split(' ')
            functionName = parsedCode[1]
            numberOfArguments = int(parsedCode[-1])

            hackAssemblyElementList += transferCall(functionName, numberOfArguments, str(translationHelperData["functionLabelIndex"]))
            translationHelperData["functionLabelIndex"] += 1
        
        hackAssemblyList += hackAssemblyElementList

    if len(translationHelperData["functionList"]) > 0:
        translationHelperData["functionList"].pop()

    return hackAssemblyList
                    
# booting code for Hack computer
def generateBootstrapCode(addComment):
    hackAssemblyElementList = []

    # SP=256
    if addComment:
        hackAssemblyElementList.append('//SP=256')
    hackAssemblyElementList.append('@256')
    hackAssemblyElementList.append('D=A')
    hackAssemblyElementList.append('@SP')
    hackAssemblyElementList.append('M=D')
    # call Sys.init
    if addComment:
        hackAssemblyElementList.append('//call Sys.init 0')
    # push return address
    hackAssemblyElementList.append('@Bootstrap$ret')
    hackAssemblyElementList.append('D=A')
    hackAssemblyElementList.append('@SP')
    hackAssemblyElementList.append('A=M')
    hackAssemblyElementList.append('M=D')
    hackAssemblyElementList.append('@SP')
    hackAssemblyElementList.append('M=M+1') 
    # push LCL
    hackAssemblyElementList.append('@LCL')
    hackAssemblyElementList.append('D=M')
    hackAssemblyElementList.append('@SP')
    hackAssemblyElementList.append('A=M')
    hackAssemblyElementList.append('M=D')
    hackAssemblyElementList.append('@SP')
    hackAssemblyElementList.append('M=M+1')
    # push ARG
    hackAssemblyElementList.append('@ARG')
    hackAssemblyElementList.append('D=M')
    hackAssemblyElementList.append('@SP')
    hackAssemblyElementList.append('A=M')
    hackAssemblyElementList.append('M=D')
    hackAssemblyElementList.append('@SP')
    hackAssemblyElementList.append('M=M+1')
    # push THIS
    hackAssemblyElementList.append('@THIS')
    hackAssemblyElementList.append('D=M')
    hackAssemblyElementList.append('@SP')
    hackAssemblyElementList.append('A=M')
    hackAssemblyElementList.append('M=D')
    hackAssemblyElementList.append('@SP')
    hackAssemblyElementList.append('M=M+1') 
    # push THAT
    hackAssemblyElementList.append('@THAT')
    hackAssemblyElementList.append('D=M')
    hackAssemblyElementList.append('@SP')
    hackAssemblyElementList.append('A=M')
    hackAssemblyElementList.append('M=D')
    hackAssemblyElementList.append('@SP')
    hackAssemblyElementList.append('M=M+1')
    # ARG = SP - 5
    hackAssemblyElementList.append('@SP')
    hackAssemblyElementList.append('D=M')
    hackAssemblyElementList.append('@5')
    hackAssemblyElementList.append('D=D-A')
    hackAssemblyElementList.append('@ARG')
    hackAssemblyElementList.append('M=D')
    # LCL = SP
    hackAssemblyElementList.append('@SP')
    hackAssemblyElementList.append('D=M')
    hackAssemblyElementList.append('@LCL')
    hackAssemblyElementList.append('M=D')
    # goto functionName
    hackAssemblyElementList.append('@Sys.init')
    hackAssemblyElementList.append('0;JMP')
    # (return address)
    hackAssemblyElementList.append('(Bootstrap' +'$ret)')    

    return hackAssemblyElementList

# write hack assembly program into a file
def writeHackAssemblyToFile(fileName, hackAssemblyList):
    outputFileName = fileName + '.asm'

    with open(outputFileName, mode='w') as f:
        for line in hackAssemblyList:
            f.write(line + '\n')

def main():
    if len(sys.argv) == 2:
        addComment = True
        translationHelperData = {
            "customLabelIndex": 0,
            "functionLabelIndex": 0,
            "functionList": []
        }

        if sys.argv[1].endswith(".vm"):
            # read vm code file and parse content into a list
            vmCodeFile = sys.argv[1]
            fileName = vmCodeFile.split('/')[-1].split('.')[0]
            vmCodeList = parseVMCodeFile(vmCodeFile)

            # main algorithm for generating Hack assembly program into a list
            hackAssemblyList = generateHackAssembly(vmCodeList, fileName, addComment, translationHelperData)
        else:
            # read each vm code file in a directory
            vmCodeDirectory = sys.argv[1]
            hackAssemblyList =  generateBootstrapCode(addComment)
            
            for fileName in os.listdir(vmCodeDirectory):
                if fileName.endswith(".vm"):
                    vmCodeList = parseVMCodeFile(vmCodeDirectory + '/' + fileName)
                    fileName = fileName.split('.')[0]

                    # main algorithm for generating Hack assembly program into a list
                    hackAssemblyList += generateHackAssembly(vmCodeList, fileName, addComment, translationHelperData)

        # write hack assembly program into a file
        if sys.argv[1].endswith(".vm"):
            destinationFileName = sys.argv[1].split(".")[0]
        else:
            destinationDirectory = sys.argv[1]
            destinationFileName = destinationDirectory + '/' + destinationDirectory.split('/')[-1] # destination directory as file name
        writeHackAssemblyToFile(destinationFileName, hackAssemblyList)
    else:
        print("Usage: python VMTranslator.py [VMCodeFile].vm or python VMTranslator.py [VMDirectory]")

if __name__ == "__main__":
    main()