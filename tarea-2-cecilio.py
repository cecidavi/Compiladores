import re

# Definición de expresiones regulares para identificadores y números enteros
IDENTIFIER_REGEX = re.compile(r'^[A-Za-z][A-Za-z0-9]*$')
INTEGER_REGEX = re.compile(r'^[0-9]+$')

def classify_token(token):
    if IDENTIFIER_REGEX.match(token):
        return 'identificador'
    elif INTEGER_REGEX.match(token):
        return 'numero'
    else:
        return None

def generate_tokens(input_string):
    tokens = []
    # Divide la entrada en posibles tokens (palabras y símbolos)
    possible_tokens = re.findall(r'\w+|[^\s\w]', input_string)
    
    for token in possible_tokens:
        token_type = classify_token(token)
        if token_type:
            tokens.append((token, token_type))
        else:
            tokens.append((token, 'simbolo'))
    
    return tokens

# Ejemplo de entrada según el ejemplo proporcionado
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

# Imprimir la tabla de tokens
for token, token_type in tokens:
    if token_type == 'simbolo':
        print(f'{token}')
    else:
        print(f'{token}\t{token_type}')
