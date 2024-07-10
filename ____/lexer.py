from CONSTATES import *
import re

class Lexer():
  def __init__(self, program):
    self.program = program
    self.token_type = ''
    self.l_token = []
    self.l_identificadores = []
    self.l_numeros = []
    self.l_comenterios = []
  
  def lex(self):
    split = re.findall(r'\{[^}]*\}|[A-Za-z_][A-Za-z0-9_]*|\d+|[ \n\t\r\+]+|[.,:;=(){}]', self.program)
    for index, char in enumerate(split, start=1):
      if char.strip():
        if char.startswith('{') and char.endswith('}'):
          id = 'CO'
          self.token_type = 'Comentario'
          self.l_comenterios.append(char)
          position = len(self.l_comenterios)
        elif char in P_RESERVADAS:
          id = 'PR'
          self.token_type = 'Palabra Reservada'
          position = P_RESERVADAS.index(char) + 1
        elif char.isalpha() or (char.isidentifier() and not char.isnumeric()):
          id = 'ID'
          self.token_type = 'Identificador'
          if char not in self.l_identificadores:
            self.l_identificadores.append(char)
          position = self.l_identificadores.index(char) + 1
        elif char.isdigit():
          id = 'NU'
          self.token_type = 'Numero'
          self.l_numeros.append(char)
          position = len(self.l_numeros)
        elif char in S_ESPECIALES :
          id = 'SE'
          self.token_type = 'Simbolo Especial'
          position = S_ESPECIALES.index(char) + 1

        self.l_token.append((id, position, char))
        # print(f'{char.ljust(30)} -> {self.token_type}')
    
    return self.l_token
  
  def imp_token(self):
    print('\n\n')
    print('Palabras reservadas'.center(30, '-'))
    for i in P_RESERVADAS:
      print(i)
    print('\n')
    print('Simbolos especiales'.center(30, '-'))
    for i in S_ESPECIALES:
      print(i)
    print('\n')
    print('Identificadores'.center(30, '-'))
    for i in self.l_identificadores:
      print(i)
    print('\n')
    print('Numeros'.center(30, '-'))
    for i in self.l_numeros:
      print(i)
    print('\n')
    print('Comentarios'.center(30, '-'))
    for i in self.l_comenterios:
      print(i)
    print('\n\n')