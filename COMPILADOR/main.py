from lexer import Lexer
from parser import Parser
from postfix import Postfix

# Funcion principal
def main():
  print('¯'*50)
  print("Inicio del programa".center(50, ' '))
  print('_'*50)

  # Leer el archivo de entrada y almacenar el programa en una variable con un bloque try-except
  try:
    with open("_input.txt", "r") as f:
      programa = f.read()
  except FileNotFoundError:
    print("Error: Archivo no encontrado")
  except Exception as e:
    print(f"Error: {e}")
    return

  # Imprimir el programa
  print(" PROGRAMA ".center(50, '-'))
  print(programa)

  # Crear un objeto Lexer y llamar al metodo lexico
  lexer = Lexer(programa)
  tokens = lexer.lexico()

  # Imprimir los tokens
  print(" TOKENS ".center(50, '-'))
  print(' Tipo - Posicion - Valor '.center(50, '_'))
  for token in tokens:
    print(token)

  #! Descomentar para ver las listas de tokens
  # lexer.listas_tokens()

  # Crear un objeto Parser y llamar al metodo parse
  print(" ANALISIS SINTACTICO ".center(50, '-'))
  parser = Parser(tokens)
  # Imprimir el resultado del analisis sintactico con un bloque try-except
  try:
    parser.parser()
    print('La sintaxis es correcta')
  except SyntaxError as e:
    print(f"-> Syntax Error: {e}")
    return
  
  # Imprimir la expresion postfija
  print(" EXPRESION POSTFIJA ".center(50, '-'))
  postfix_converter = Postfix()
  expresiones_postfijas = []
  for i, token in enumerate(tokens):
    if token[0] == 'SE' and token[1] == 4:  # Encontrar el token '='
      expr_tokens = []
      j = i + 1
      while j < len(tokens) and not (tokens[j][0] == 'SE' and tokens[j][1] == 1):  # Hasta el ';'
        expr_tokens.append(tokens[j])
        j += 1
      postfijo = postfix_converter.infijo_a_postfijo(expr_tokens)
      expresiones_postfijas.append(postfijo)
      i = j
    
  for exp in expresiones_postfijas:
    print('Expresion postfija: ', exp)


if __name__ == "__main__":
  main()
  print(" END ".center(50, '_'))
