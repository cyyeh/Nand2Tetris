# VMTranslator translates VM code(compiled from Jack programming language using Jack compiler)
# into Hack machine language

import sys

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

# main algorithm for generating Hack machine language program into a list
def generateHackMachineLanguage(vmCodeList, fileName):
    if '/' in fileName:
        fileName = fileName.split('/')[-1]

    # transfer VM add command into Hack machine language code
    def transferAdd(code):
        hackMachineCodeList = []

        # generate Hack machine language code
        hackMachineCodeList.append('//' + code)
        hackMachineCodeList.append('@SP')
        hackMachineCodeList.append('M=M-1')
        hackMachineCodeList.append('A=M')
        hackMachineCodeList.append('D=M')
        hackMachineCodeList.append('@SP')
        hackMachineCodeList.append('M=M-1')
        hackMachineCodeList.append('A=M')
        hackMachineCodeList.append('M=D+M')         
        hackMachineCodeList.append('@SP')
        hackMachineCodeList.append('M=M+1')

        return hackMachineCodeList
    
    # transfer VM sub command into Hack machine language code
    def trasferSub(code):
        hackMachineCodeList = []

        # generate Hack machine language code
        hackMachineCodeList.append('//' + code)
        hackMachineCodeList.append('@SP')
        hackMachineCodeList.append('M=M-1')
        hackMachineCodeList.append('A=M')
        hackMachineCodeList.append('D=M')
        hackMachineCodeList.append('@SP')
        hackMachineCodeList.append('M=M-1')
        hackMachineCodeList.append('A=M')
        hackMachineCodeList.append('M=M-D')
        hackMachineCodeList.append('@SP')
        hackMachineCodeList.append('M=M+1')

        return hackMachineCodeList

    # transfer VM neg command into Hack machine language code
    def transferNeg(code):
        hackMachineCodeList = []

        # generate Hack machine language code
        hackMachineCodeList.append('//' + code)
        hackMachineCodeList.append('@SP')
        hackMachineCodeList.append('M=M-1')
        hackMachineCodeList.append('A=M')
        hackMachineCodeList.append('D=-M')            
        hackMachineCodeList.append('M=D')
        hackMachineCodeList.append('@SP')
        hackMachineCodeList.append('M=M+1')

        return hackMachineCodeList

    # transfer VM eq command into Hack machine language code
    def transferEq(code, index):
        hackMachineCodeList = []

        # generate Hack machine language code
        hackMachineCodeList.append('//' + code)
        hackMachineCodeList.append('@SP')
        hackMachineCodeList.append('M=M-1')
        hackMachineCodeList.append('A=M')
        hackMachineCodeList.append('D=M')
        hackMachineCodeList.append('@SP')
        hackMachineCodeList.append('M=M-1')
        hackMachineCodeList.append('A=M')
        hackMachineCodeList.append('D=D-M')
        hackMachineCodeList.append('@EQUAL'+ str(index))
        hackMachineCodeList.append('D;JEQ')
        hackMachineCodeList.append('D=0')
        hackMachineCodeList.append('@FINAL'+ str(index))
        hackMachineCodeList.append('0;JEQ')
        hackMachineCodeList.append('(EQUAL'+ str(index) +')')
        hackMachineCodeList.append('D=-1')
        hackMachineCodeList.append('(FINAL'+ str(index) +')')
        hackMachineCodeList.append('@SP')
        hackMachineCodeList.append('A=M')
        hackMachineCodeList.append('M=D')
        hackMachineCodeList.append('@SP')
        hackMachineCodeList.append('M=M+1')

        index += 1

        return hackMachineCodeList, index

    # transfer VM gt command into Hack machine language code
    def transferGt(code, index):
        hackMachineCodeList = []

        # generate Hack machine language code
        hackMachineCodeList.append('//' + code)
        hackMachineCodeList.append('@SP')
        hackMachineCodeList.append('M=M-1')
        hackMachineCodeList.append('A=M')
        hackMachineCodeList.append('D=M')
        hackMachineCodeList.append('@SP')
        hackMachineCodeList.append('M=M-1')
        hackMachineCodeList.append('A=M')
        hackMachineCodeList.append('D=M-D')
        hackMachineCodeList.append('@GREATER_THAN'+ str(index))
        hackMachineCodeList.append('D;JGT')
        hackMachineCodeList.append('D=0')
        hackMachineCodeList.append('@END'+ str(index))
        hackMachineCodeList.append('0;JEQ')
        hackMachineCodeList.append('(GREATER_THAN'+ str(index) +')')
        hackMachineCodeList.append('D=-1')
        hackMachineCodeList.append('(END'+ str(index) +')')
        hackMachineCodeList.append('@SP')
        hackMachineCodeList.append('A=M')        
        hackMachineCodeList.append('M=D')
        hackMachineCodeList.append('@SP')
        hackMachineCodeList.append('M=M+1')

        index += 1

        return hackMachineCodeList, index

    # transfer VM lt command into Hack machine language code
    def transferLt(code, index):
        hackMachineCodeList = []

        # generate Hack machine language code
        hackMachineCodeList.append('//' + code)
        hackMachineCodeList.append('@SP')
        hackMachineCodeList.append('M=M-1')
        hackMachineCodeList.append('A=M')
        hackMachineCodeList.append('D=M')
        hackMachineCodeList.append('@SP')
        hackMachineCodeList.append('M=M-1')
        hackMachineCodeList.append('A=M')
        hackMachineCodeList.append('D=M-D')
        hackMachineCodeList.append('@LESS_THAN'+ str(index))
        hackMachineCodeList.append('D;JLT')
        hackMachineCodeList.append('D=0')
        hackMachineCodeList.append('@END'+ str(index))
        hackMachineCodeList.append('0;JEQ')
        hackMachineCodeList.append('(LESS_THAN'+ str(index) +')')
        hackMachineCodeList.append('D=-1')
        hackMachineCodeList.append('(END'+ str(index) +')')
        hackMachineCodeList.append('@SP')
        hackMachineCodeList.append('A=M')        
        hackMachineCodeList.append('M=D')
        hackMachineCodeList.append('@SP')
        hackMachineCodeList.append('M=M+1')

        index += 1

        return hackMachineCodeList, index

    # transfer VM and command into Hack machine language code
    def transferAnd(code):
        hackMachineCodeList = []

        # generate Hack machine language code
        hackMachineCodeList.append('//' + code)
        hackMachineCodeList.append('@SP')
        hackMachineCodeList.append('M=M-1')
        hackMachineCodeList.append('A=M')
        hackMachineCodeList.append('D=M')
        hackMachineCodeList.append('@SP')
        hackMachineCodeList.append('M=M-1')
        hackMachineCodeList.append('A=M')
        hackMachineCodeList.append('D=D&M')       
        hackMachineCodeList.append('M=D')
        hackMachineCodeList.append('@SP')
        hackMachineCodeList.append('M=M+1')

        return hackMachineCodeList

    # transfer VM or command into Hack machine language code
    def transferOr(code):
        hackMachineCodeList = []

        # generate Hack machine language code
        hackMachineCodeList.append('//' + code)
        hackMachineCodeList.append('@SP')
        hackMachineCodeList.append('M=M-1')
        hackMachineCodeList.append('A=M')
        hackMachineCodeList.append('D=M')
        hackMachineCodeList.append('@SP')
        hackMachineCodeList.append('M=M-1')
        hackMachineCodeList.append('A=M')
        hackMachineCodeList.append('D=D|M')
        hackMachineCodeList.append('M=D')
        hackMachineCodeList.append('@SP')
        hackMachineCodeList.append('M=M+1')

        return hackMachineCodeList

    # transfer VM not command into Hack machine language code
    def transferNot(code):
        hackMachineCodeList = []

        # generate Hack machine language code
        hackMachineCodeList.append('//' + code)
        hackMachineCodeList.append('@SP')
        hackMachineCodeList.append('M=M-1')
        hackMachineCodeList.append('A=M')
        hackMachineCodeList.append('D=!M')
        hackMachineCodeList.append('M=D')
        hackMachineCodeList.append('@SP')
        hackMachineCodeList.append('M=M+1')

        return hackMachineCodeList

    # transfer VM push command into Hack machine language code
    def transferPush(code, fileName):
        hackMachineCodeList = []
        parsedCode = code.split(" ")
        memorySegmentAccess = parsedCode[1]
        offset = parsedCode[-1]
        memorySegmentDict = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}

        # generate Hack machine language code
        hackMachineCodeList.append('//' + code)
        if 'constant' in parsedCode:
            # *SP = i, SP++
            hackMachineCodeList.append('@' + str(offset))
            hackMachineCodeList.append('D=A')
            hackMachineCodeList.append('@SP')
            hackMachineCodeList.append('A=M')
            hackMachineCodeList.append('M=D')
            hackMachineCodeList.append('@SP')
            hackMachineCodeList.append('M=M+1')            
        elif memorySegmentAccess in {'local', 'argument', 'this', 'that'}:
            # addr = segmentPointer + i, *SP = *addr, SP++
            hackMachineCodeList.append('@' + str(offset))
            hackMachineCodeList.append('D=A')
            hackMachineCodeList.append('@' + memorySegmentDict[memorySegmentAccess])
            hackMachineCodeList.append('A=D+M')
            hackMachineCodeList.append('D=M')
            hackMachineCodeList.append('@SP')
            hackMachineCodeList.append('A=M')
            hackMachineCodeList.append('M=D')
            hackMachineCodeList.append('@SP')
            hackMachineCodeList.append('M=M+1')
        elif 'temp' in parsedCode:
            # addr = 5 + i, *SP = *addr, SP++
            hackMachineCodeList.append('@' + str(offset))
            hackMachineCodeList.append('D=A')
            hackMachineCodeList.append('@5')
            hackMachineCodeList.append('A=D+A')
            hackMachineCodeList.append('D=M')
            hackMachineCodeList.append('@SP')
            hackMachineCodeList.append('A=M')
            hackMachineCodeList.append('M=D')
            hackMachineCodeList.append('@SP')
            hackMachineCodeList.append('M=M+1')
        elif 'pointer' in parsedCode:
            # *SP = THIS/THAT, SP++
            if offset == '0':
                accessor = 'THIS'
            else:
                accessor = 'THAT'
            
            hackMachineCodeList.append('@' + accessor)
            hackMachineCodeList.append('D=M')
            hackMachineCodeList.append('@SP')
            hackMachineCodeList.append('A=M')
            hackMachineCodeList.append('M=D')
            hackMachineCodeList.append('@SP')
            hackMachineCodeList.append('M=M+1')
        elif 'static' in parsedCode:
            hackMachineCodeList.append('@' + fileName + '.' + str(offset))
            hackMachineCodeList.append('D=M')
            hackMachineCodeList.append('@SP')
            hackMachineCodeList.append('A=M')
            hackMachineCodeList.append('M=D')
            hackMachineCodeList.append('@SP')
            hackMachineCodeList.append('M=M+1')            
    
        return hackMachineCodeList

    # transfer VM pop command into Hack machine language code
    def transferPop(code, fileName):
        hackMachineCodeList = []
        parsedCode = code.split(" ")
        memorySegmentAccess = parsedCode[1]
        offset = parsedCode[-1]
        memorySegmentDict = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}

        # generate Hack machine language code
        hackMachineCodeList.append('//' + code)
        if memorySegmentAccess in {'local', 'argument', 'this', 'that'}:
            # addr = segmentPointer + i, SP--, *addr = *SP
            hackMachineCodeList.append('@' + str(offset))
            hackMachineCodeList.append('D=A')
            hackMachineCodeList.append('@' + memorySegmentDict[memorySegmentAccess])
            hackMachineCodeList.append('D=D+M')
            hackMachineCodeList.append('@R13')
            hackMachineCodeList.append('M=D')
            hackMachineCodeList.append('@SP')
            hackMachineCodeList.append('M=M-1')
            hackMachineCodeList.append('A=M')
            hackMachineCodeList.append('D=M')
            hackMachineCodeList.append('@R13')
            hackMachineCodeList.append('A=M')
            hackMachineCodeList.append('M=D')
        elif 'temp' in parsedCode:
            # addr = 5 + i, SP--, *addr = *SP
            hackMachineCodeList.append('@' + str(offset))
            hackMachineCodeList.append('D=A')
            hackMachineCodeList.append('@5')
            hackMachineCodeList.append('D=D+A')
            hackMachineCodeList.append('@R13')
            hackMachineCodeList.append('M=D')
            hackMachineCodeList.append('@SP')
            hackMachineCodeList.append('M=M-1')
            hackMachineCodeList.append('A=M')
            hackMachineCodeList.append('D=M')
            hackMachineCodeList.append('@R13')
            hackMachineCodeList.append('A=M')
            hackMachineCodeList.append('M=D')
        elif 'pointer' in parsedCode:
            # SP--, THIS/THAT = *SP
            if offset == '0':
                accessor = 'THIS'
            else:
                accessor = 'THAT'
            
            hackMachineCodeList.append('@SP')
            hackMachineCodeList.append('M=M-1')
            hackMachineCodeList.append('A=M')
            hackMachineCodeList.append('D=M')
            hackMachineCodeList.append('@' + accessor)
            hackMachineCodeList.append('M=D')
        elif 'static' in parsedCode:
            hackMachineCodeList.append('@SP')
            hackMachineCodeList.append('M=M-1')
            hackMachineCodeList.append('A=M')
            hackMachineCodeList.append('D=M')
            hackMachineCodeList.append('@' + fileName + '.' + str(offset))
            hackMachineCodeList.append('M=D')
    
        return hackMachineCodeList

    hackMachineLanguageList = []
    index = 0

    for line in vmCodeList:
        if 'add' in line:
            hackMachineCodeList = transferAdd(line)
        elif 'sub' in line:
            hackMachineCodeList = trasferSub(line)
        elif 'neg' in line:
            hackMachineCodeList = transferNeg(line)
        elif 'eq' in line:
            hackMachineCodeList, index = transferEq(line, index)
        elif 'gt' in line:
            hackMachineCodeList, index = transferGt(line, index)
        elif 'lt' in line:
            hackMachineCodeList, index = transferLt(line, index)
        elif 'and' in line:
            hackMachineCodeList = transferAnd(line)
        elif 'or' in line:
            hackMachineCodeList = transferOr(line)
        elif 'not' in line:
            hackMachineCodeList = transferNot(line)
        elif 'push' in line:
            hackMachineCodeList = transferPush(line, fileName)
        elif 'pop' in line:
            hackMachineCodeList = transferPop(line, fileName)
        
        hackMachineLanguageList += hackMachineCodeList

    return hackMachineLanguageList
                    
# write hack machine language program into a file
def writeHackMachineLangugeToFile(fileName, hackMachineLanguageList):
    outputFileName = fileName + '.asm'

    with open(outputFileName, mode='w') as f:
        for line in hackMachineLanguageList:
            f.write(line + '\n')

def main():
    if len(sys.argv) == 2:
        # read vm code file and parse content into a list
        vmCodeFile = sys.argv[1]
        fileName = vmCodeFile.split('.')[0]
        vmCodeList = parseVMCodeFile(vmCodeFile)

        # main algorithm for generating Hack machine language program into a list
        hackMachineLanguageList = generateHackMachineLanguage(vmCodeList, fileName)

        # write hack machine language program into a file
        writeHackMachineLangugeToFile(fileName, hackMachineLanguageList)
    else:
        print("Usage: python VMTranslator.py [VMCodeFile].vm")

if __name__ == "__main__":
    main()