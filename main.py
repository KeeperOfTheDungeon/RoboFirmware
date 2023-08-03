COMMAND_TOKEN = b'#'
MESSAGE_START_TOKEN = b'*'
STREAM_START_TOKEN = b'$'

EXCEPTION_START_TOKEN = b'^'
ALLERT_START_TOKEN = b'!'

OK_START_TOKEN = b'O'
FAIL_START_TOKEN = b'N'
END_TOKEN = b';'


"""
output:
    1. take cmd input
    2. tokenize
    3. buffer
    4. send to pio
"""
    

def pack(message: str) -> bytes:
    frame = bytearray(COMMAND_TOKEN)
    frame += message.encode('ascii')
    frame += END_TOKEN

    return frame


"""
    input:
        1. check pio for input
        2. read and buffer
        3. tokenize
        4. build string
        5. cmd output
"""

def unpack(frame: bytearray) -> str:
    return frame.decode('ascii')[1:len(frame) - 1]

# main function
if __name__ == '__main__':
    tokens = unpack(pack('Goodbye World'))
    print(tokens)
    
