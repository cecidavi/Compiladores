import re

# Define regular expressions for identifiers and integers
IDENTIFIER_REGEX = re.compile(r'^[A-Za-z][A-Za-z0-9]*$')
INTEGER_REGEX = re.compile(r'^[0-9]+$')

# Special symbols
SPECIAL_SYMBOLS = {';', ':', '=', '+', '-', '*', '/', '(', ')' }

# Reserved words (example)
RESERVED_WORDS = {'PROGRAMA', 'VARIABLES', 'INICIO', 'FIN', 'NUMERO'}

# Tables
identifiers_table = {}
numbers_table = {}
special_symbols_table = {symbol: idx for idx, symbol in enumerate(SPECIAL_SYMBOLS)}
reserved_words_table = {word: idx for idx, word in enumerate(RESERVED_WORDS)}

# Error messages
ERROR_MESSAGES = [
    "PROGRAMA esperado",
    "identificador esperado",
    "; esperado",
    "identificador definido anteriormente",
    ": esperado",
    "INICIO esperado",
    "FIN esperado",
    "NUMERO esperado"
]

def classify_token(token):
    token_upper = token.upper()
    if IDENTIFIER_REGEX.match(token):
        if token_upper in RESERVED_WORDS:
            return 'PR', reserved_words_table[token_upper]
        if token not in identifiers_table:
            identifiers_table[token] = len(identifiers_table)
        return 'ID', identifiers_table[token]
    elif INTEGER_REGEX.match(token):
        if token not in numbers_table:
            numbers_table[token] = len(numbers_table)
        return 'CN', numbers_table[token]
    elif token in SPECIAL_SYMBOLS:
        return 'SE', special_symbols_table[token]
    else:
        return 'error', None

def generate_tokens(input_string):
    tokens = []
    in_comment = False
    token = ""
    
    for char in input_string:
        if in_comment:
            if char == '}':
                in_comment = False
            continue
        if char == '{':
            in_comment = True
            continue
        
        if char.isspace() or char in SPECIAL_SYMBOLS:
            if token:
                token_type, position = classify_token(token)
                tokens.append((token_type, token, position))
                token = ""
            if char in SPECIAL_SYMBOLS:
                token_type, position = classify_token(char)
                tokens.append((token_type, char, position))
        else:
            token += char
    
    if token:
        token_type, position = classify_token(token)
        tokens.append((token_type, token, position))
    
    return tokens

def print_token_table(tokens):
    pt = 0
    for token_type, token, position in tokens:
        if token_type == 'error':
            print(f'***CARÁCTER INVÁLIDO: {token}***')
        else:
            print(f'{token_type},{position} {pt} {token}')
            pt += 1

def print_error_table(tokens):
    for token_type, token, position in tokens:
        if token_type == 'error':
            print(f'{token} ER,? ERROR')
        else:
            if position is not None:
                if token_type == 'ID':
                    print(f'{token} ID,{position} {identifiers_table[token]}')
                elif token_type == 'CN':
                    print(f'{token} CN,{position} {numbers_table[token]}')
                elif token_type == 'SE':
                    print(f'{token} SE,{position} {special_symbols_table[token]}')
                elif token_type == 'PR':
                    print(f'{token} PR,{position} {reserved_words_table[token]}')

# Example input based on the provided example
input_string = """PROGRAMA ObjetivoFinal;
VARIABLES
  A,B,C: NUMERO;
  X:     NUMERO;
INICIO
  A=10;
  B=20;
  X=A+B; {Operaciones Aritméticas}
FIN;"""

tokens = generate_tokens(input_string)

# Print the token table
print("Token Table:")
print_token_table(tokens)

# Print the error table
print("\nError Table:")
print_error_table(tokens)
