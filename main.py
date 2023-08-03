COMMAND_TOKEN = b'1FA'
END_TOKEN = b'1FF'


"""
output:
    1. take cmd input
    2. tokenize
    3. buffer
    4. send to pio
"""
    

def packer(message: str) -> bytes:
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


# main function
if __name__ == '__main__':
    tokens = packer('Goodbye World')
    print(tokens)
    
