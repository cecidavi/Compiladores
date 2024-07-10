def verificarSintaxis(tokens):
    
    def verificar_palabra_reservada(palabra):
        if tokens.pop(0) != ('PR', palabra):
            raise SyntaxError(f"Se esperaba la palabra reservada {palabra}")
    
    def verificar_identificador():
        if not tokens or tokens[0][0] != 'ID':
            raise SyntaxError("Se esperaba un identificador")
        tokens.pop(0)
        
    def verificar_constante():
        if not tokens or tokens[0][0] != 'CN':
            raise SyntaxError("Se esperaba una constante")
        tokens.pop(0)
    
    def verificar_simbolo_especial(simbolo):
        if not tokens or tokens[0] != ('SE', simbolo):
            raise SyntaxError(f"Se esperaba el simbolo especial {simbolo}")
        tokens.pop(0)
        
    def verificar_expresion():
        print(tokens[0])
        if tokens[0][0] == 'ID' or tokens[0][0] == 'CN':
            if tokens[0][0] == 'ID':
                verificar_identificador()
            elif tokens[0][0] == 'CN':
                verificar_constante()

        elif tokens[0] == ('SE', 9):  # Paréntesis de apertura
            verificar_simbolo_especial(9)
            verificar_expresion()
            verificar_simbolo_especial(10)  # Paréntesis de cierre
        else:
            raise SyntaxError("Expresión inválida")
        print(tokens[0])
    
    def verificar_variable():
        while tokens and tokens[0] == ('SE', 2):
            verificar_simbolo_especial(2)
            if tokens[0]==('SE',3):
                break
            
            if tokens[0][0]=='ID':
                verificar_identificador()
            else:
                raise SyntaxError("Se esperaba un identificador")

    def verificar_estatuto():
        verificar_identificador()
        if tokens and tokens[0] == ('SE', 2):
            tokens.pop(0)
            verificar_estatuto()
        
        verificar_simbolo_especial(4)
        verificar_expresion()
        if tokens[0][1] in (5, 6, 7, 8):
            verificar_simbolo_especial(tokens[0][1])
            verificar_expresion()
        verificar_simbolo_especial(1)
        
    try:
        
        verificar_palabra_reservada(1)  
        
        verificar_identificador()
        
        verificar_simbolo_especial(1)
        
        
        verificar_palabra_reservada(2)  
###################################################################        
        while tokens and tokens[0][0] == 'ID': 
            verificar_identificador()
            
            verificar_variable()
            verificar_simbolo_especial(3)
            verificar_palabra_reservada(5)
            verificar_simbolo_especial(1)
            
###################################################################
        print(tokens[0])
        verificar_palabra_reservada(3) 
        print(tokens[0])
        while tokens and tokens[0] != ('PR', 4):
            print(tokens[0])
            verificar_estatuto()
            print(tokens[0])
        
        verificar_palabra_reservada(4)  
        verificar_simbolo_especial(1)
        
        if tokens:
            raise SyntaxError("Código después del fin del programa")
        
        print("La sintaxis es correcta")
    except SyntaxError as e:
        print(f"Error de sintaxis: {e}")

texto = 'input.txt'

with open(texto, 'r') as archivo:
    contenido = archivo.read()
    print('\n')

identificador = ''
numero = ''
comentario = ''
procesando_identificador = False
procesando_comentario = False

palabras_reservadas = ['PROGRAMA','VARIABLES','INICIO','FIN','NUMERO']
simbolos_especiales = [';',',',':','=','+','-','*','/','(',')']
identificadores = []
numeros = []
tokens = []

for i, caracter in enumerate(contenido, start=1):
    if caracter == '{': 
        procesando_comentario = True
        comentario += caracter
    elif caracter == '}':
        comentario += caracter
        procesando_comentario = False
        print(comentario, end=' ')
        print("\t\t\tComentario")
        comentario = ''
    elif procesando_comentario:
        comentario += caracter
    elif caracter.isdigit(): 
        if procesando_identificador:
            identificador += caracter
        else:
            numero += caracter
    elif caracter.isalpha():  
        if not procesando_identificador and numero: 
            print(numero, "    Numero")
            numeros.append(numero)
            tokens.append(('CN', (len(numeros))))
            numero = ''
        identificador += caracter
        procesando_identificador = True
    else:
        if identificador:
            if identificador.upper() in palabras_reservadas:
                print(identificador, end=' ') 
                print("\t\t\tPalabra Reservada")
                tokens.append(('PR', (palabras_reservadas.index(identificador.upper())+1)))
            else:
                print(identificador, end=' ')
                print("\t\t\tIdentificador")
                identificadores.append(identificador)
                tokens.append(('ID', (len(identificadores))))
            identificador = ''
            procesando_identificador = False
        if numero:
            print(numero, end=' ')
            print("\t\t\tNumero")
            numeros.append(numero)
            tokens.append(('CN', (len(numeros))))
            numero = ''
        if caracter in simbolos_especiales:
            print(caracter, end=' ')
            print("\t\t\tSimbolo Especial")
            tokens.append(('SE', (simbolos_especiales.index(caracter)+1)))

if identificador:
    if identificador.upper() in palabras_reservadas:
        print(identificador, "    Palabra Reservada")
        tokens.append(('PR', (palabras_reservadas.index(identificador.upper())+1)))
    else:
        print(identificador, "    Identificador")
        identificadores.append(identificador)
        tokens.append(('ID', (len(identificadores))))

if numero:
    print(numero, "    Numero")
    numeros.append(numero)
    tokens.append(('CN', (len(numeros))))

print('\n')
print("Tokens generados:".center(50, "-"))
print('\n')
print(tokens)
print('\n')
for token in tokens:
    print("TOKEN".center(50, "-"))
    print(token)

print(" SINTAXIS ".center(50, "-"))
verificarSintaxis(tokens)

