import re

# Define regular expressions for identifiers and integers
IDENTIFIER_REGEX = re.compile(r'^[A-Za-z][A-Za-z0-9]*$')
INTEGER_REGEX = re.compile(r'^[0-9]+$')

# Special symbols
SPECIAL_SYMBOLS = {';', ':', '=', '+', '-', '*', '/', '(', ')'}

# Reserved words (example)
RESERVED_WORDS = {'PROGRAMA', 'VARIABLES', 'INICIO', 'FIN', 'NUMERO', 'CADENA'}

# Tables
identifiers_table = {}
numbers_table = {}
special_symbols_table = {symbol: idx for idx, symbol in enumerate(SPECIAL_SYMBOLS)}
reserved_words_table = {word: idx for idx, word in enumerate(RESERVED_WORDS)}

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
    current_line = 1
    
    for char in input_string:
        if in_comment:
            if char == '}':
                in_comment = False
            continue
        if char == '{':
            in_comment = True
            continue
        
        if char == '\n':
            current_line += 1
        
        if char.isspace() or char in SPECIAL_SYMBOLS or char == ',':
            if token:
                token_type, position = classify_token(token)
                tokens.append((token_type, token, position, current_line))
                token = ""
            if char in SPECIAL_SYMBOLS:
                token_type, position = classify_token(char)
                tokens.append((token_type, char, position, current_line))
            elif char == ',':
                # Manejo de la coma como un separador, pero no la añade como token
                continue
        else:
            token += char
    
    if token:
        token_type, position = classify_token(token)
        tokens.append((token_type, token, position, current_line))
    
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.symbol_table = {}

    def parse(self):
        self.program()

    def program(self):
        self.match('PR', 0)  # PROGRAMA
        program_name = self.match('ID')      # Identifier
        self.match('SE', 0)   # ;
        self.symbol_table[program_name] = 'PROGRAMA'
        self.variables()
        self.match('PR', 2)   # INICIO
        self.statements()
        self.match('PR', 3)   # FIN
        self.match('SE', 0)   # ;

    def variables(self):
        self.match('PR', 1)  # VARIABLES
        while self.current_token() == ('ID',):
            self.declaration()

    def declaration(self):
        var_name = self.match('ID')
        self.symbol_table[var_name] = 'NUMERO'  # Assuming all variables are of type 'NUMERO'
        while self.current_token() == ('SE', 0):  # ;
            self.match('SE', 0)
            var_name = self.match('ID')
            self.symbol_table[var_name] = 'NUMERO'  # Assuming all variables are of type 'NUMERO'
        self.match('SE', 1)  # ;
        self.match('PR', 4)     # Type
        self.match('SE', 0)  # ;

    def statements(self):
        while self.current_token() == ('ID',):
            self.statement()

    def statement(self):
        var_name = self.match('ID')
        if var_name not in self.symbol_table:
            self.error(f"Variable no declarada: {var_name}")
        self.match('SE', 2)  # =
        self.expression()
        self.match('SE', 0)  # ;

    def expression(self):
        self.term()
        while self.current_token() == ('SE', 3):  # +
            self.match('SE', 3)
            self.term()

    def term(self):
        if self.current_token() == ('ID',):
            var_name = self.match('ID')
            if var_name not in self.symbol_table:
                self.error(f"Variable no declarada: {var_name}")
        elif self.current_token() == ('CN',):
            self.match('CN')

    def match(self, token_type, token_value=None):
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            if token[0] == token_type and (token_value is None or token[2] == token_value):
                self.pos += 1
                if token_type == 'ID' and token[1] in self.symbol_table:
                    return token[1]
            else:
                self.error(token)
        else:
            self.error(None)

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos][0],
        return None

    def error(self, token):
        if token:
            print(f"Error: token inesperado {token} en posición {self.pos}")
        else:
            print(f"Error: fin de entrada inesperado")
        exit(1)

def main():
    input_string = """PROGRAMA ObjetivoFinal;
VARIABLES
  A,B,C: NUMERO;
  X:     NUMERO;
INICIO
  A=10;
  B=20;
  C=30;
  X=A+B; {Operaciones Aritméticas}
FIN;"""

    tokens = generate_tokens(input_string)

    for token_type, token, position, line in tokens:
        if token_type == 'error':
            print(f'***CARÁCTER INVÁLIDO: {token}***')
        elif token_type == 'COMENTARIO':
            print(f'Token: {token_type}, Valor: {token}, Línea: {line}')
        else:
            print(f'Token: {token_type}, Valor: {token}, Línea: {line}')

    parser = Parser(tokens)
    parser.parse()

    print("\nAnálisis sintáctico completado con éxito")

    # Implementación del análisis semántico
    semantic_analyzer = SemanticAnalyzer(parser)
    semantic_analyzer.analyze()

    print("\nAnálisis semántico completado con éxito")

if __name__ == "__main__":
    main()
