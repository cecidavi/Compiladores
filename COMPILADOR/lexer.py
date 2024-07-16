from CONSTATES import P_RESERVADAS, S_ESPECIALES
import re

class Lexer():
  # Constructor
  def __init__(self, programa):
    self.programa = programa # Programa a analizar
    self.tokens = [] # Lista de TOKENS
    self.identificadores = [] # Lista de IDENTIFICADORES
    self.numeros = [] # Lista de NUMEROS
    self.comentarios = [] # Lista de COMENTARIOS

  #~ Funcion para analizar el programa
  def lexico(self):
    # Expresiones regulares para los tokens
    tokens_s = [
      ('COMENTARIO', r'\{[^}]*\}'),
      ('RESERVADA', r'\b(?:' + '|'.join(P_RESERVADAS) + r')\b'),
      ('IDENTIFICADOR', r'[A-Za-z_][A-Za-z0-9_]*'),
      ('NUMERO', r'\d+'),
      ('ESPECIAL', r'[;,:=+\-*/(){}]'),
      ('SKIP', r'[ \t\n]+'),  # Skip spaces and tabs
      ('MISMATCH', r'.'),    # Any other character
    ]
    
    # token_regex es una cadena de texto que contiene los tokens y sus respectivas expresiones regulares
    token_regex = '|'.join('(?P<%s>%s)' % pair for pair in tokens_s)
    
    # re.finditer busca todas las coincidencias de la expresion regular en el programa
    for i in re.finditer(token_regex, self.programa): 
      tipo = i.lastgroup
      valor = i.group()
      if tipo == 'COMENTARIO':
        self.comentarios.append(valor)
      elif tipo == 'RESERVADA':
        self.tokens.append(('PR', P_RESERVADAS.index(valor) + 1 , valor))
      elif tipo == 'IDENTIFICADOR':
        if valor not in self.identificadores:
          self.identificadores.append(valor)
        self.tokens.append(('ID', self.identificadores.index(valor) + 1, valor))
      elif tipo == 'NUMERO':
        self.numeros.append(valor)
        self.tokens.append(('NU', len(self.numeros), valor))
      elif tipo == 'ESPECIAL':
        self.tokens.append(('SE', S_ESPECIALES.index(valor) + 1, valor))
      elif tipo == 'SKIP':
        continue
      elif tipo == 'MISMATCH':
        raise RuntimeError(f'Caracter inesperado: {valor}')
  
    return self.tokens

  #~ Funcion para imprimir las listas de tokens
  def listas_tokens(self):
    print('^'*50)
    print('Lista de Palabras Reservadas'.center(50, '^'))
    for index, char in enumerate(P_RESERVADAS, start=1):
      print(f'{index} - {char}')
    print('^'*50)
    print('Lista de Caracteres Especiales'.center(50, '^'))
    for index, char in enumerate(S_ESPECIALES, start=1):
      print(f'{index} - {char}')
    print('^'*50)
    print('Lista de Identificadores'.center(50, '^'))
    for index, char in enumerate(self.identificadores, start=1):
      print(f'{index} - {char}')
    print('^'*50)
    print('Lista de Numeros'.center(50, '^'))
    for index, char in enumerate(self.numeros, start=1):
      print(f'{index} - {char}')
    print('^'*50)
    print('Lista de Comentarios'.center(50, '^'))
    for index, char in enumerate(self.comentarios, start=1):
      print(f'{index} - {char}')
    print('^'*50)
    print('^'*50)
