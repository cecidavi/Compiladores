import re

class Lexer:
    def __init__(self, input_code):
        self.input_code = input_code
        self.tokens = []
        self.token_specs = [
            ('Programa', r'PROGRAMA'),        # Palabra clave PROGRAMA
            ('VARIABLES', r'VARIABLES'),      # Palabra clave VARIABLES
            ('INICIO', r'INICIO'),            # Palabra clave INICIO
            ('FIN', r'FIN'),                  # Palabra clave FIN
            ('NUMERO', r'NUMERO'),            # Palabra clave NUMERO
            ('ID', r'[A-Za-z]+'),             # Identificadores
            ('NUMBER', r'\d+(\.\d*)?'),       # Números
            ('ASSIGN', r'='),                 # Operador de asignación
            ('PLUS', r'\+'),                  # Operador de suma
            ('MINUS', r'-'),                  # Operador de resta
            ('MULT', r'\*'),                  # Operador de multiplicación
            ('DIV', r'/'),                    # Operador de división
            ('LPAREN', r'\('),                # Paréntesis izquierdo
            ('RPAREN', r'\)'),                # Paréntesis derecho
            ('SEMICOLON', r';'),              # Punto y coma
            ('COLON', r':'),                  # Dos puntos
            ('COMMA', r','),                  # Coma
            ('SKIP', r'[ \t\n]+'),            # Espacios, tabulaciones y nuevas líneas
            ('COMMENT', r'\{[^}]*\}'),        # Comentarios entre {}
            ('MISMATCH', r'.'),               # Cualquier otro carácter
        ]

    def tokenize(self):
        token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in self.token_specs)
        for mo in re.finditer(token_regex, self.input_code):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'NUMBER':
                value = float(value) if '.' in value else int(value)
            elif kind == 'SKIP' or kind == 'COMMENT':
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'{value} inesperado en la entrada')
            self.tokens.append((kind, value))
        return self.tokens

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def define(self, name, type):
        self.symbols[name] = {'type': type, 'value': None}

    def lookup(self, name):
        if name in self.symbols:
            return self.symbols[name]
        else:
            raise RuntimeError(f'{name} no definido')

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.symbol_table = SymbolTable()

    def parse(self):
        try:
            self.program()
            return "Programa Parseado Correctamente"
        except RuntimeError as e:
            return str(e)

    def consume(self, expected_type):
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == expected_type:
            self.pos += 1
        else:
            raise RuntimeError(f'Se esperaba {expected_type} pero se encontró {self.tokens[self.pos][0]}')

    def program(self):
        self.consume('PROGRAMA')
        program_name = self.tokens[self.pos][1]
        self.consume('ID')
        self.consume('SEMICOLON')
        self.bloque()
        self.consume('SEMICOLON')

    def bloque(self):
        self.consume('VARIABLES')
        self.variable_declaration()
        self.consume('INICIO')
        self.statements()
        self.consume('FIN')

    def variable_declaration(self):
        while self.tokens[self.pos][0] == 'ID':
            var_name = self.tokens[self.pos][1]
            self.symbol_table.define(var_name, 'NUMERO')  # Definir el identificador
            self.consume('ID')
            while self.tokens[self.pos][0] == 'COMMA':
                self.consume('COMMA')
                var_name = self.tokens[self.pos][1]
                self.symbol_table.define(var_name, 'NUMERO')  # Definir el identificador
                self.consume('ID')
            self.consume('COLON')
            self.consume('NUMERO')
            self.consume('SEMICOLON')

    def statements(self):
        while self.tokens[self.pos][0] != 'FIN':
            self.statement()

    def statement(self):
        self.consume('ID')
        self.consume('ASSIGN')
        self.expression()
        self.consume('SEMICOLON')

    def expression(self):
        self.term()
        while self.tokens[self.pos][0] in ('PLUS', 'MINUS'):
            self.consume(self.tokens[self.pos][0])
            self.term()

    def term(self):
        self.factor()
        while self.tokens[self.pos][0] in ('MULT', 'DIV'):
            self.consume(self.tokens[self.pos][0])
            self.factor()

    def factor(self):
        if self.tokens[self.pos][0] == 'NUMBER':
            self.consume('NUMBER')
        elif self.tokens[self.pos][0] == 'ID':
            self.consume('ID')
        elif self.tokens[self.pos][0] == 'LPAREN':
            self.consume('LPAREN')
            self.expression()
            self.consume('RPAREN')
        else:
            raise RuntimeError('Token inesperado')

# Ejemplo de uso
# cambiar el input_string por el código que se desea analizar
# no forzar la lectura de un archivo
input_string = """PROGRAMA ObjetivoFinal;
VARIABLES
  A,B,C,D: NUMERO;
  X:     NUMERO;
INICIO
  A=10;
  B=20;
  c=30;
    D=40;
  X=A+B; {Operaciones Aritméticas}
FIN;"""

lexer = Lexer(input_string)
tokens = lexer.tokenize()
print("Tokens:")
for token in tokens:
    print(token)

parser = Parser(tokens)
result = parser.parse()
print("\nResultado del análisis:")
print(result)

print("\nTabla de símbolos:")
for name, info in parser.symbol_table.symbols.items():
    print(name, info)
