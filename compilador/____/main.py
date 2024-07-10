''' --------------------
  Compilador en Python
--------------------'''
from lexer import Lexer
from parser import Parser

if __name__ == "__main__":

  print("Compilador")
  print('\n')

  try:
    with open("input.txt", "r") as f:
      programa = f.read()
  except FileNotFoundError:
    print("Error: Archivo no encontrado")
  except Exception as e:
    print(f"Error: {e}")

  print("Programa:")
  print(programa)
  print('\n')

  lexer = Lexer(programa)
  tokens = lexer.lex()

  print('\n')
  print("Tokens:".center(50, '°'))
  for token in tokens:
    print(token)
  print('\n')
  
  parser = Parser(tokens)
  try:
    parser.parse()
  except SyntaxError as e:
    print('\n')
    print(f"Syntax Error: {e}")
    print('\n')
  
  print("Fin del programa")


