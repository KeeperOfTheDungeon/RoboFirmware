
"""
output:
    1. take cmd input
    2. tokenize
    3. buffer
    4. send to pio
"""

def string_tokenizer(message: str):
    tokens = []
    for token in message:
        tokens.append(token)
    return tokens
    



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
    tokens = string_tokenizer('Goodbye World')
    for token in tokens:
        print(token)
    
