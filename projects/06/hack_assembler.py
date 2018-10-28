# Hack Machine Language Assembler written in Python3
import sys
import re

# read assembly file(.asm) and parse file content into a list and returns the list, also update symbol table
def readAssemblyFile(file, updateSymbolTable):
    assemblyProgramList = []

    with open(file, mode='r') as f:
        lines = f.read().splitlines()
        lineNumber = 0
        for line in lines:
            if not line: # ignore empty lines
                continue
            elif line[0:2] == '//': # ignore lines with comment comes first
                continue
            else:
                if '//' in line:
                    line = line.split('//')[0]
                    assemblyProgramList.append(line.strip()) # ignore comments inside a line
                else:
                    assemblyProgramList.append(line.strip())
                if not updateSymbolTable(line, lineNumber):
                    lineNumber += 1
    
    return assemblyProgramList

# initialize c-type instruction table
def initializeCInstructionTable():
    cInstuctionTable = {
        "comp": {
            '0': '0101010',
            '1': '0111111',
            '-1': '0111010',
            'D': '0001100',
            'A': '0110000',
            '!D': '0001101',
            '!A': '0110001',
            '-D': '0001111',
            '-A': '0110011',
            'D+1': '0011111',
            'A+1': '0110111',
            'D-1': '0001110',
            'A-1': '0110010',
            'D+A': '0000010',
            'D-A': '0010011',
            'A-D': '0000111',
            'D&A': '0000000',
            'D|A': '0010101',
            'M': '1110000',
            '!M': '1110001',
            '-M': '1110011',
            'M+1': '1110111',
            'M-1': '1110010',
            'D+M': '1000010',
            'D-M': '1010011',
            'M-D': '1000111',
            'D&M': '1000000',
            'D|M': '1010101'
        }, 
        "dest": {
            "null": '000',
            "M": "001",
            "D": "010",
            "MD": "011",
            "A": "100",
            "AM": "101",
            "AD": "110",
            "AMD": "111"
        }, 
        "jump": {
            "null": '000',
            "JGT": "001",
            "JEQ": "010",
            "JGE": "011",
            "JLT": "100",
            "JNE": "101",
            "JLE": "110",
            "JMP": "111"
        }
    }

    return cInstuctionTable

# initialize symbol table
def initializeSymbolTable():
    symbolTable = {
        "R0": "0",
        "R1": "1",
        "R2": "2",
        "R3": "3",
        "R4": "4",
        "R5": "5",
        "R6": "6",
        "R7": "7",
        "R8": "8",
        "R9": "9",
        "R10": "10",
        "R11": "11",
        "R12": "12",
        "R13": "13",
        "R14": "14",
        "R15": "15",
        "SCREEN": "16384",
        "KBD": "24576",
        "SP": "0",
        "LCL": "1",
        "ARG": "2",
        "THIS": "3",
        "THAT": "4" 
    }

    return symbolTable

# update symbol table from user defined symbols
def updateSymbolTable(oneLineAssembly, lineNumber):
    foundParenthesis = False

    if '@' in oneLineAssembly: # update variable symbols
        symbol = oneLineAssembly.strip().split('@')[1]
        if symbol not in symbolTable and not symbol.isdigit():
            symbolTable[symbol] = USER_DEFIEND_SYMBOL_INIT
    elif '(' and ')' in oneLineAssembly: # update label symbols
        symbol = oneLineAssembly[oneLineAssembly.find("(") + 1 : oneLineAssembly.find(")")]
        symbolTable[symbol] = str(lineNumber)
        foundParenthesis = True

    return foundParenthesis

# main algorithm to transfer Hack machine language into binary format and put them into a list
def transferHackAssemblyToBinaryCode(assemblyProgramList):
    binaryProgramList = []
    variableSymbolAddress = 16

    for assembly in assemblyProgramList:
        if '@' in assembly: # decode A-type instruction
            symbol = assembly.strip().split('@')[1]
            if not symbol.isdigit():
                if symbolTable[symbol] == USER_DEFIEND_SYMBOL_INIT:
                    symbolTable[symbol] = str(variableSymbolAddress)
                    variableSymbolAddress += 1
                digitToBinary =  '{0:016b}'.format(int(symbolTable[symbol]))
            else:
                digitToBinary = '{0:016b}'.format(int(symbol))
            binaryProgramList.append(digitToBinary)                
        elif '=' in assembly or ';' in assembly: # decode C-type instruction
            firstThreeBits = '111'
            compBits = '-------'
            destBits = '000'
            jumpBits = '000'

            if '=' in assembly and ';' not in assembly:
                dest, comp = assembly.split('=')
                destBits = cInstuctionTable["dest"][dest]
                compBits = cInstuctionTable["comp"][comp]
            elif '=' in assembly and ';' in assembly:
                dest, comp, jump = re.split('=|;', assembly)
                destBits = cInstuctionTable["dest"][dest]
                compBits = cInstuctionTable["comp"][comp]
                jumpBits = cInstuctionTable["jump"][jump]
            elif ';' in assembly:
                comp, jump = assembly.split(';')
                jumpBits = cInstuctionTable["jump"][jump]
                compBits = cInstuctionTable["comp"][comp]
            binaryProgramList.append(firstThreeBits + compBits + destBits + jumpBits)

    return binaryProgramList

# write binary format program into a file
def writeBinaryProgramToFile(fileName, binaryProgramList):
    outputFileName = fileName.split('.')[0] + '.hack'

    with open(outputFileName, mode='w') as f:
        for line in binaryProgramList:
            f.write(line + '\n')

USER_DEFIEND_SYMBOL_INIT = "INIT"

# initialize c-type instruction table
cInstuctionTable = initializeCInstructionTable()

# initialize symbol table
symbolTable = initializeSymbolTable()

def main():
    if len(sys.argv) == 2:
        # read assembly file(.asm) and parse file content into a list, also update symbol table
        fileName = sys.argv[1]
        assemblyProgramList = readAssemblyFile(fileName, updateSymbolTable)

        # main algorithm to transfer Hack machine language into binary format and put them into a list
        binaryProgramList = transferHackAssemblyToBinaryCode(assemblyProgramList)

        print(binaryProgramList)

        # write binary format program into a file
        writeBinaryProgramToFile(fileName, binaryProgramList)
    else:
        print("Usage: python hack_assembler.py [assemblyFile.asm]")

if __name__ == '__main__':
    main()   