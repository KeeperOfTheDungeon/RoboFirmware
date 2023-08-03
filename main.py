
"""
output:
    1. take cmd input
    2. tokenize
    3. buffer
    4. send to pio
"""

def string_tokenizer(message: str):
    for token in message:
        print(token + '\n')
    



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
    string_tokenizer('Goodbye World')
