class Parser():
  # Constructor
  def __init__(self, tokens):
    self.tokens = tokens                                      # Lista de tokens
    self.token_indice_actual =  0                             # Indice del token actual
    self.token_actual = self.tokens[self.token_indice_actual] # Token actual

  #~ Funcion para avanzar de token
  def token_siguiente(self):
    self.token_indice_actual += 1
    if self.token_indice_actual < len(self.tokens):
      self.token_actual = self.tokens[self.token_indice_actual]
    else:
      self.token_actual = None

  #~ Funcion para verificar los tokens
  def token_esperado(self, tipo_token, valor=None):
    #° Mientras el token actual sea un comentario, avanzar al siguiente token
    while self.token_actual and self.token_actual[0] == 'CO':
      self.token_siguiente() 
    #° Si el token actual es None, lanzar un error
    if self.token_actual is None:
      raise SyntaxError("Fin inesperado de la entrada")
    #° Si el token actual no es del tipo esperado, lanzar un error
    if self.token_actual[0] != tipo_token or (valor is not None and self.token_actual[1] != valor):
      raise SyntaxError(f"Token inesperado {self.token_actual}")
    self.token_siguiente()

  #~ Funcion para el analisis sintactico
  def programa(self):
    self.token_esperado('PR', 1) # PROGRAMA
    self.token_esperado('ID') # identificador
    self.token_esperado('SE', 1) # ;
    self.bloque() # bloque
    self.token_esperado('SE', 1) # ;

  #~ Funcion para el analisis sintactico de los bloques
  def bloque(self):
    #° Si el token actual es una palabra reservada VARIABLES
    if self.token_actual[0] == 'PR': 
      self.variables()
      self.token_esperado('PR', 3) # INICIO
      self.estatutos()
      self.token_esperado('PR', 4) # FIN
    else:
      self.token_siguiente()
      self.bloque()

  #~ Funcion para el bloque de variables
  def variables(self):
    self.token_esperado('PR', 2) # VARIABLES
    #° Mientras el token actual no sea palabra reservada INICIO
    while self.token_actual and self.token_actual[0] != 'PR' and self.token_actual[1] != 3:
      self.token_esperado('ID') # A
      #° Mientras el token actual sea una coma seguir avanzando
      while self.token_actual and self.token_actual[0] == 'SE' and self.token_actual[1] == 2: # mientras sea ,
        self.token_siguiente() 
        self.token_esperado('ID') # C
      self.token_esperado('SE', 3) # :
      self.token_esperado('PR', 5) # NUMERO
      self.token_esperado('SE', 1) # ;

  #~ Funcion para los estatutos
  def estatutos(self):
    #° Mientras el token actual no sea palabra reservada FIN
    while self.token_actual and self.token_actual[0] != 'PR' and self.token_actual[1] != 4:
      #° Si el token actual es un comentario, avanzar al siguiente token y continuar
      if self.token_actual[0] == 'CO':
        self.token_siguiente()
        break
      self.estatuto()

  #~ Funcion para los estatutos
  def estatuto(self):
    self.token_esperado('ID')  # A
    self.token_esperado('SE', 4)  # =
    self.expresion()  # numero o lo que sea
    self.token_esperado('SE', 1)  # ;

  #~ Funcion para las expresiones
  def expresion(self):
    if self.token_actual[0] == 'NU':
      self.token_siguiente()
    elif self.token_actual[0] == 'ID':
      self.token_siguiente()
    elif self.token_actual[1] == 9: #° si el token actual es un parentesis (
      self.token_siguiente()
      self.expresion()
      self.token_esperado('SE', 10) #se espera que el token actual es un parentesis )
    else:
      raise SyntaxError(f"Token inesperado {self.token_actual}")
    #° Mientras el token actual sea un operador +, -, *, /
    while self.token_actual and self.token_actual[0] == 'SE' and self.token_actual[1] in [5, 6, 7, 8]: 
      self.token_siguiente()
      self.expresion()

  #~ Funcion principal
  def parser(self):
    self.programa()
