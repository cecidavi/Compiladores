class Parser():
  def __init__(self, tokens):
    self.tokens = tokens
    self.current_token_index = 0
    self.current_token = self.tokens[self.current_token_index]

  def advance(self):
    self.current_token_index += 1
    if self.current_token_index < len(self.tokens):
      self.current_token = self.tokens[self.current_token_index]
    else:
      self.current_token = None
  
  def expect(self, token_type, value=None):
    while self.current_token and self.current_token[0] == 'CO':
      self.advance() 
    if self.current_token is None:
      raise SyntaxError("Fin inesperado de la entrada")
    if self.current_token[0] != token_type or (value is not None and self.current_token[1] != value):
      raise SyntaxError(f"Se esperaba |{token_type} {value}| pero se encontro |{self.current_token}|")
    self.advance()

  def programa(self):
    self.expect('PR', 1) # PROGRAMA
    self.expect('ID') # identificador
    self.expect('SE', 1) # ;
    self.bloque() # bloque
    self.expect('SE', 1) # ;

  def bloque(self):
    if self.current_token[0] == 'PR': 
      self.variables()
      self.expect('PR', 3) # INICIO
      self.estatutos()
      self.expect('PR', 4)
    else:
      self.advance()
      self.bloque()

  def variables(self):
    self.expect('PR', 2) # VARIABLES
    while self.current_token and self.current_token[0] != 'PR' and self.current_token[1] != 3:
      self.expect('ID') # A
      while self.current_token and self.current_token[0] == 'SE' and self.current_token[1] == 2: # mientras sea ,
        self.advance() 
        self.expect('ID') # C
      self.expect('SE', 3) # :
      self.expect('PR', 5) # NUMERO
      self.expect('SE', 1) # ;

  def estatutos(self):
    while self.current_token and self.current_token[0] != 'PR' and self.current_token[1] != 4:
      if self.current_token[0] == 'CO':
        self.advance()
        break
      self.estatuto()
  
  def estatuto(self):
    self.expect('ID')  # A
    self.expect('SE', 4)  # =
    self.expresion()  # numero o lo que sea
    self.expect('SE', 1)  # ;

  def expresion(self):
    if self.current_token[0] == 'NU':
      self.advance()
    elif self.current_token[0] == 'ID':
      self.advance()
    elif self.current_token[1] == 9:
      self.advance()
      self.expresion()
      self.expect('SE', 10) # )
    else:
      raise SyntaxError(f"Token inesperado {self.current_token}")
    while self.current_token and self.current_token[0] == 'SE' and self.current_token[1] in [5, 6, 7, 8]: 
      self.advance()
      self.expresion()
  
  def parse(self):
    self.programa()
    print("La sintaxis es correcta")