# Template by Bruce A. Maxwell, 2015
#
# implements a simple assembler for the following assembly language
# 
# - One instruction or label per line.
#
# - Blank lines are ignored.
#
# - Comments start with a # as the first character and all subsequent
# - characters on the line are ignored.
#
# - Spaces delimit instruction elements.
#
# - A label ends with a colon and must be a single symbol on its own line.
#
# - A label can be any single continuous sequence of printable
# - characters; a colon or space terminates the symbol.
#
# - All immediate and address values are given in decimal.
#
# - Address values must be positive
#
# - Negative immediate values must have a preceeding '-' with no space
# - between it and the number.
#

# Language definition:
#
# LOAD D A   - load from address A to destination D
# LOADA D A  - load using the address register from address A + RE to destination D
# STORE S A  - store value in S to address A
# STOREA S A - store using the address register the value in S to address A + RE
# BRA L      - branch to label A
# BRAZ L     - branch to label A if the CR zero flag is set
# BRAN L     - branch to label L if the CR negative flag is set
# BRAO L     - branch to label L if the CR overflow flag is set
# BRAC L     - branch to label L if the CR carry flag is set
# CALL L     - call the routine at label L
# RETURN     - return from a routine
# HALT       - execute the halt/exit instruction
# PUSH S     - push source value S to the stack
# POP D      - pop form the stack and put in destination D
# OPORT S    - output to the global port from source S
# IPORT D    - input from the global port to destination D
# ADD A B C  - execute C <= A + B
# SUB A B C  - execute C <= A - B
# AND A B C  - execute C <= A and B  bitwise
# OR  A B C  - execute C <= A or B   bitwise
# XOR A B C  - execute C <= A xor B  bitwise
# SHIFTL A C - execute C <= A shift left by 1
# SHIFTR A C - execute C <= A shift right by 1
# ROTL A C   - execute C <= A rotate left by 1
# ROTR A C   - execute C <= A rotate right by 1
# MOVE A C   - execute C <= A where A is a source register
# MOVEI V C  - execute C <= value V
#

# 2-pass assembler
# pass 1: read through the instructions and put numbers on each instruction location
#         calculate the label values
#
# pass 2: read through the instructions and build the machine instructions
#

import sys

# converts d to an 8-bit 2-s complement binary value
def dec2comp8( d, linenum ):
    try:
        if d > 0:
            l = d.bit_length()
            v = "00000000"
            v = v[0:8-l] + format( d, 'b')
        elif d < 0:
            dt = 128 + d
            l = dt.bit_length()
            v = "10000000"
            v = v[0:8-l] + format( dt, 'b')[:]
        else:
            v = "00000000"
    except:
        print ('Invalid decimal number on line %d' % (linenum))
        exit()

    return v

# converts d to an 8-bit unsigned binary value
def dec2bin8( d, linenum ):
    if d > 0:
        l = d.bit_length()
        v = "00000000"
        v = v[0:8-l] + format( d, 'b' )
    elif d == 0:
        v = "00000000"
    else:
        print ('Invalid address on line %d: value is negative' % (linenum))
        exit()

    return v


# Tokenizes the input data, discarding white space and comments
# returns the tokens as a list of lists, one list for each line.
#
# The tokenizer also converts each character to lower case.
def tokenize( fp ):
    tokens = []

    # start of the file
    fp.seek(0)

    lines = fp.readlines()

    # strip white space and comments from each line
    for line in lines:
        ls = line.strip()
        uls = ''
        for c in ls:
            if c != '#':
                uls = uls + c
            else:
                break

        # skip blank lines
        if len(uls) == 0:
            continue

        # split on white space
        words = uls.split()

        newwords = []
        for word in words:
            newwords.append( word.lower() )

        tokens.append( newwords )

    return tokens

# reads through the file and returns a dictionary of all location
# labels with their line numbers
def pass1( tokens ):
    index = 0
    label_dict = {}

    updated_tokens = []

    for inst in tokens:
        if inst[0][-1] == ":":
            if inst[0][:-1] not in label_dict.keys():
                label_dict[inst[0][:-1]] = index
            else:
                print("Duplicate Label Error: "  + str(inst[0]))
                exit()
        else:
            updated_tokens.append(inst)
            index+=1
    return [updated_tokens, label_dict]


    

def pass2(tokens, labels):
    machine_instructions = []
    line_number = 0
    for token in tokens:
        machine_instr = ""
        match token[0]:
            case "load":
                machine_instr = "00000"
                match token[1]:
                    case "ra": machine_instr += "000"
                    case "rb": machine_instr += "001"
                    case "rc": machine_instr += "010"
                    case "rd": machine_instr += "011"
                    case "re": machine_instr += "100"
                    case "sp": machine_instr += "101"
                machine_instr += dec2bin8(int(token[2]), line_number)
            case "loada":
                machine_instr = "00001"
                match token[1]:
                    case "ra": machine_instr += "000"
                    case "rb": machine_instr += "001"
                    case "rc": machine_instr += "010"
                    case "rd": machine_instr += "011"
                    case "re": machine_instr += "100"
                    case "sp": machine_instr += "101"
                machine_instr += dec2bin8(int(token[2]), line_number)
            case "store":
                machine_instr = "00010"
                match token[1]:
                    case "ra": machine_instr += "000"
                    case "rb": machine_instr += "001"
                    case "rc": machine_instr += "010"
                    case "rd": machine_instr += "011"
                    case "re": machine_instr += "100"
                    case "sp": machine_instr += "101"
                machine_instr += dec2bin8(int(token[2]), line_number)
            case "storea":
                machine_instr = "00011"
                match token[1]:
                    case "ra": machine_instr += "000"
                    case "rb": machine_instr += "001"
                    case "rc": machine_instr += "010"
                    case "rd": machine_instr += "011"
                    case "re": machine_instr += "100"
                    case "sp": machine_instr += "101"
                machine_instr += dec2bin8(int(token[2]), line_number)
            case "bra": machine_instr = "00101111" + dec2bin8(labels[token[1]], line_number)
            case "braz": machine_instr = "00110000" + dec2bin8(labels[token[1]], line_number)
            case "bran": machine_instr = "00110001" + dec2bin8(labels[token[1]], line_number)
            case "brao": machine_instr = "00110010" + dec2bin8(labels[token[1]], line_number)
            case "brac": machine_instr = "00110011" + dec2bin8(labels[token[1]], line_number)
            case "call": machine_instr = "00110111" + dec2bin8(labels[token[1]], line_number)
            case "return": machine_instr = "0011101111111111"
            case "halt": machine_instr = "0011111111111111"
            case "push":
                machine_instr = "0100"
                match token[1]:
                    case "ra": machine_instr += "000111111111"
                    case "rb": machine_instr += "001111111111"
                    case "rc": machine_instr += "010111111111"
                    case "rd": machine_instr += "011111111111"
                    case "re": machine_instr += "100111111111"
                    case "sp": machine_instr += "101111111111"
                    case "pc": machine_instr += "110111111111"
                    case "cr": machine_instr += "111111111111"
            case "pop":
                machine_instr = "0101"
                match token[1]:
                    case "ra": machine_instr += "000111111111"
                    case "rb": machine_instr += "001111111111"
                    case "rc": machine_instr += "010111111111"
                    case "rd": machine_instr += "011111111111"
                    case "re": machine_instr += "100111111111"
                    case "sp": machine_instr += "101111111111"
                    case "pc": machine_instr += "110111111111"
                    case "cr": machine_instr += "111111111111"
            case "oport":
                machine_instr = "0110"
                match token[1]:
                    case "ra": machine_instr += "000111111111"
                    case "rb": machine_instr += "001111111111"
                    case "rc": machine_instr += "010111111111"
                    case "rd": machine_instr += "011111111111"
                    case "re": machine_instr += "100111111111"
                    case "sp": machine_instr += "101111111111"
                    case "pc": machine_instr += "110111111111"
                    case "ir": machine_instr += "111111111111"
            case "iport":
                machine_instr = "0111"
                match token[1]:
                    case "ra": machine_instr += "000111111111"
                    case "rb": machine_instr += "001111111111"
                    case "rc": machine_instr += "010111111111"
                    case "rd": machine_instr += "011111111111"
                    case "re": machine_instr += "100111111111"
                    case "sp": machine_instr += "101111111111"
                    case "pc": machine_instr += "110111111111"
                    case "ir": machine_instr += "111111111111"
            case "add":
                machine_instr = "1000"
                match token[1]:
                    case "ra": machine_instr += "000"
                    case "rb": machine_instr += "001"
                    case "rc": machine_instr += "010"
                    case "rd": machine_instr += "011"
                    case "re": machine_instr += "100"
                    case "sp": machine_instr += "101"
                    case "zeros": machine_instr += "110"
                    case "ones": machine_instr += "111"
                match token[2]:
                    case "ra": machine_instr += "000111"
                    case "rb": machine_instr += "001111"
                    case "rc": machine_instr += "010111"
                    case "rd": machine_instr += "011111"
                    case "re": machine_instr += "100111"
                    case "sp": machine_instr += "101111"
                    case "zeros": machine_instr += "110111"
                    case "ones": machine_instr += "111111"
                match token[3]:
                    case "ra": machine_instr += "000"
                    case "rb": machine_instr += "001"
                    case "rc": machine_instr += "010"
                    case "rd": machine_instr += "011"
                    case "re": machine_instr += "100"
                    case "sp": machine_instr += "101"
            case "sub":
                machine_instr = "1001"
                match token[1]:
                    case "ra": machine_instr += "000"
                    case "rb": machine_instr += "001"
                    case "rc": machine_instr += "010"
                    case "rd": machine_instr += "011"
                    case "re": machine_instr += "100"
                    case "sp": machine_instr += "101"
                    case "zeros": machine_instr += "110"
                    case "ones": machine_instr += "111"
                match token[2]:
                    case "ra": machine_instr += "000111"
                    case "rb": machine_instr += "001111"
                    case "rc": machine_instr += "010111"
                    case "rd": machine_instr += "011111"
                    case "re": machine_instr += "100111"
                    case "sp": machine_instr += "101111"
                    case "zeros": machine_instr += "110111"
                    case "ones": machine_instr += "111111"
                match token[3]:
                    case "ra": machine_instr += "000"
                    case "rb": machine_instr += "001"
                    case "rc": machine_instr += "010"
                    case "rd": machine_instr += "011"
                    case "re": machine_instr += "100"
                    case "sp": machine_instr += "101"
            case "and":
                machine_instr = "1010"
                match token[1]:
                    case "ra": machine_instr += "000"
                    case "rb": machine_instr += "001"
                    case "rc": machine_instr += "010"
                    case "rd": machine_instr += "011"
                    case "re": machine_instr += "100"
                    case "sp": machine_instr += "101"
                    case "zeros": machine_instr += "110"
                    case "ones": machine_instr += "111"
                match token[2]:
                    case "ra": machine_instr += "000111"
                    case "rb": machine_instr += "001111"
                    case "rc": machine_instr += "010111"
                    case "rd": machine_instr += "011111"
                    case "re": machine_instr += "100111"
                    case "sp": machine_instr += "101111"
                    case "zeros": machine_instr += "110111"
                    case "ones": machine_instr += "111111"
                match token[3]:
                    case "ra": machine_instr += "000"
                    case "rb": machine_instr += "001"
                    case "rc": machine_instr += "010"
                    case "rd": machine_instr += "011"
                    case "re": machine_instr += "100"
                    case "sp": machine_instr += "101"
            case "or":
                machine_instr = "1011"
                match token[1]:
                    case "ra": machine_instr += "000"
                    case "rb": machine_instr += "001"
                    case "rc": machine_instr += "010"
                    case "rd": machine_instr += "011"
                    case "re": machine_instr += "100"
                    case "sp": machine_instr += "101"
                    case "zeros": machine_instr += "110"
                    case "ones": machine_instr += "111"
                match token[2]:
                    case "ra": machine_instr += "000111"
                    case "rb": machine_instr += "001111"
                    case "rc": machine_instr += "010111"
                    case "rd": machine_instr += "011111"
                    case "re": machine_instr += "100111"
                    case "sp": machine_instr += "101111"
                    case "zeros": machine_instr += "110111"
                    case "ones": machine_instr += "111111"
                match token[3]:
                    case "ra": machine_instr += "000"
                    case "rb": machine_instr += "001"
                    case "rc": machine_instr += "010"
                    case "rd": machine_instr += "011"
                    case "re": machine_instr += "100"
                    case "sp": machine_instr += "101"
            case "xor":
                machine_instr = "1100"
                match token[1]:
                    case "ra": machine_instr += "000"
                    case "rb": machine_instr += "001"
                    case "rc": machine_instr += "010"
                    case "rd": machine_instr += "011"
                    case "re": machine_instr += "100"
                    case "sp": machine_instr += "101"
                    case "zeros": machine_instr += "110"
                    case "ones": machine_instr += "111"
                match token[2]:
                    case "ra": machine_instr += "000111"
                    case "rb": machine_instr += "001111"
                    case "rc": machine_instr += "010111"
                    case "rd": machine_instr += "011111"
                    case "re": machine_instr += "100111"
                    case "sp": machine_instr += "101111"
                    case "zeros": machine_instr += "110111"
                    case "ones": machine_instr += "111111"
                match token[3]:
                    case "ra": machine_instr += "000"
                    case "rb": machine_instr += "001"
                    case "rc": machine_instr += "010"
                    case "rd": machine_instr += "011"
                    case "re": machine_instr += "100"
                    case "sp": machine_instr += "101"
            case "shiftl":
                machine_instr = "11010"
                match token[1]:
                    case "ra": machine_instr += "00011111"
                    case "rb": machine_instr += "00111111"
                    case "rc": machine_instr += "01011111"
                    case "rd": machine_instr += "01111111"
                    case "re": machine_instr += "10011111"
                    case "sp": machine_instr += "10111111"
                    case "zeros": machine_instr += "11011111"
                    case "ones": machine_instr += "11111111"
                match token[2]:
                    case "ra": machine_instr += "000"
                    case "rb": machine_instr += "001"
                    case "rc": machine_instr += "010"
                    case "rd": machine_instr += "011"
                    case "re": machine_instr += "100"
                    case "sp": machine_instr += "101"
            case "shiftr":
                machine_instr = "11011"
                match token[1]:
                    case "ra": machine_instr += "00011111"
                    case "rb": machine_instr += "00111111"
                    case "rc": machine_instr += "01011111"
                    case "rd": machine_instr += "01111111"
                    case "re": machine_instr += "10011111"
                    case "sp": machine_instr += "10111111"
                    case "zeros": machine_instr += "11011111"
                    case "ones": machine_instr += "11111111"
                match token[2]:
                    case "ra": machine_instr += "000"
                    case "rb": machine_instr += "001"
                    case "rc": machine_instr += "010"
                    case "rd": machine_instr += "011"
                    case "re": machine_instr += "100"
                    case "sp": machine_instr += "101"
            case "rotl":
                machine_instr = "11100"
                match token[1]:
                    case "ra": machine_instr += "00011111"
                    case "rb": machine_instr += "00111111"
                    case "rc": machine_instr += "01011111"
                    case "rd": machine_instr += "01111111"
                    case "re": machine_instr += "10011111"
                    case "sp": machine_instr += "10111111"
                    case "zeros": machine_instr += "11011111"
                    case "ones": machine_instr += "11111111"
                match token[2]:
                    case "ra": machine_instr += "000"
                    case "rb": machine_instr += "001"
                    case "rc": machine_instr += "010"
                    case "rd": machine_instr += "011"
                    case "re": machine_instr += "100"
                    case "sp": machine_instr += "101"
            case "rotr":
                machine_instr = "11101"
                match token[1]:
                    case "ra": machine_instr += "00011111"
                    case "rb": machine_instr += "00111111"
                    case "rc": machine_instr += "01011111"
                    case "rd": machine_instr += "01111111"
                    case "re": machine_instr += "10011111"
                    case "sp": machine_instr += "10111111"
                    case "zeros": machine_instr += "11011111"
                    case "ones": machine_instr += "11111111"
                match token[2]:
                    case "ra": machine_instr += "000"
                    case "rb": machine_instr += "001"
                    case "rc": machine_instr += "010"
                    case "rd": machine_instr += "011"
                    case "re": machine_instr += "100"
                    case "sp": machine_instr += "101"
            case "move":
                machine_instr = "11110"
                match token[1]:
                    case "ra": machine_instr += "00011111"
                    case "rb": machine_instr += "00111111"
                    case "rc": machine_instr += "01011111"
                    case "rd": machine_instr += "01111111"
                    case "re": machine_instr += "10011111"
                    case "sp": machine_instr += "10111111"
                    case "pc": machine_instr += "11011111"
                    case "ir": machine_instr += "11111111"
                match token[2]:
                    case "ra": machine_instr += "000"
                    case "rb": machine_instr += "001"
                    case "rc": machine_instr += "010"
                    case "rd": machine_instr += "011"
                    case "re": machine_instr += "100"
                    case "sp": machine_instr += "101"
            case "movei":
                machine_instr = "11111"
                machine_instr += dec2comp8(int(token[1]), line_number)
                match token[2]:
                    case "ra": machine_instr += "000"
                    case "rb": machine_instr += "001"
                    case "rc": machine_instr += "010"
                    case "rd": machine_instr += "011"
                    case "re": machine_instr += "100"
                    case "sp": machine_instr += "101"
        line_number += 1
        machine_instructions.append(machine_instr + ";")
    return machine_instructions


def main( argv ):
    if len(argv) < 2:
        print ('Usage: python %s <filename>' % (argv[0]))
        exit()

    fp = open( argv[1], 'r' )

    tokens = tokenize( fp )

    fp.close()

    # execute pass1 and pass2 then print it out as an MIF file

    pass1_list = pass1(tokens)
    pass2_list = pass2(pass1_list[0], pass1_list[1])
    line = 0
    print("-- program memory file for " + str(argv[1].rsplit(".")[0]) + ".a")
    print("DEPTH = 256;")
    print("WIDTH = 16;")
    print("ADDRESS_RADIX = HEX;")
    print("DATA_RADIX = BIN;")
    print("CONTENT")
    print("BEGIN")
    for instr in pass2_list:
        print("%02X : %s" % (line, instr))
        line += 1
    print("[%02X..FF] : 1111111111111111;" % (line))
    print("END")
    return


if __name__ == "__main__":
    main(sys.argv)
    