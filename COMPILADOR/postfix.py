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
    #° Recorremos los tokens
    for token in tokens:
      tipo, pos, valor = token
      #° Si es un numero o un identificador lo agregamos al resultado
      if tipo == 'ID' or tipo == 'NU':  # Identificadores y números
        Resultado.append(valor)
      elif valor == '(':
        Operadores.append(valor)
      elif valor == ')':
        #° mientras el ultimo operador sea diferente de '(' lo agregamos al resultado
        while Operadores and Operadores[-1] != '(':
          Resultado.append(Operadores.pop())
        Operadores.pop()  # Pop '(' 
      else:  # Operadores
        #° Mientras el ultimo operador tenga mayor precedencia que el actual lo agregamos al resultado
        while (Operadores and self.precedencia(Operadores[-1]) >= self.precedencia(valor)):
          Resultado.append(Operadores.pop())
        Operadores.append(valor)
    #° Mientras haya operadores los agregamos al resultado
    while Operadores:
      Resultado.append(Operadores.pop())
    #° Retornamos el resultado
    return ' '.join(Resultado)

  # Funcion para evaluar una expresion postfija
  def evaluar_postfijo(self, expresion_postfija, variables):
    pila = []
    for token in expresion_postfija.split():
      if token.isdigit():  # Si es un número
        pila.append(int(token))
      elif token in variables:  # Si es una variable
        pila.append(variables[token])
      else:  # Si es un operador
        operando2 = pila.pop()
        operando1 = pila.pop()
        if token == '+':
          pila.append(operando1 + operando2)
        elif token == '-':
          pila.append(operando1 - operando2)
        elif token == '*':
          pila.append(operando1 * operando2)
        elif token == '/':
          pila.append(operando1 / operando2)
    return pila[0]  # El resultado final está en la cima de la pila
