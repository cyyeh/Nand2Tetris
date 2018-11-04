//push constant 111
@111
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 333
@333
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 888
@888
D=A
@SP
A=M
M=D
@SP
M=M+1
//pop static 8
@8
D=A
@MemoryAccess/StaticTest/StaticTest.8
M=D
//pop static 3
@3
D=A
@MemoryAccess/StaticTest/StaticTest.3
M=D
//pop static 1
@1
D=A
@MemoryAccess/StaticTest/StaticTest.1
M=D
//push static 3
@3
D=A
@MemoryAccess/StaticTest/StaticTest.3
M=D
//push static 1
@1
D=A
@MemoryAccess/StaticTest/StaticTest.1
M=D
//sub
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M-D
@SP
M=M+1
//push static 8
@8
D=A
@MemoryAccess/StaticTest/StaticTest.8
M=D
//add
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=D+M
@SP
M=M+1
