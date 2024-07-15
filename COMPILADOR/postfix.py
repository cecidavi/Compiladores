# Clase para la Notacion Postfija
class Postfix():
  # Constructor vacio
  def __init__(self) -> None:
    pass
  
  #~ Funcion para obtener la precedencia de los operadores
  def precedencia(self, operador):
    if operador == '+' or operador == '-':
      return 1
    if operador == '*' or operador == '/':
      return 2
    return 0

  #~ Funcion para convertir una expresion infija a postfija
  def infijo_a_postfijo(self, tokens):
    Resultado = []
    Operadores = []
    for token in tokens:
      tipo, pos, valor = token
      if tipo == 'ID' or tipo == 'NU':  # Identificadores y números
        Resultado.append(valor)
      elif valor == '(':
        Operadores.append(valor)
      elif valor == ')':
        while Operadores and Operadores[-1] != '(':
          Resultado.append(Operadores.pop())
        Operadores.pop()  # Pop '('
      else:  # Operadores
        while (Operadores and self.precedencia(Operadores[-1]) >= self.precedencia(valor)):
          Resultado.append(Operadores.pop())
        Operadores.append(valor)
    while Operadores:
      Resultado.append(Operadores.pop())
    return ' '.join(Resultado)
