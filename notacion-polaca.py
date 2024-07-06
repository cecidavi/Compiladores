# Definimos la precedencia de los operadores
precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

# Función para verificar si un carácter es un operador
def is_operator(c):
    return c in precedence

# Función para convertir una expresión infija a notación polaca
def infix_to_prefix(expression):
    # Agregamos paréntesis al inicio y final de la expresión
    expression = '(' + expression + ')'
    stack = []
    output = []

    # Invertimos la expresión y reemplazamos los paréntesis
    expression = expression[::-1]
    expression = expression.replace('(', ')temp')
    expression = expression.replace(')', '(')
    expression = expression.replace(')temp', ')')
    
    # Iteramos a través de la expresión invertida
    for char in expression:
        # Si el carácter es un operador
        if is_operator(char):
            while (stack and stack[-1] != ')' and precedence[char] < precedence[stack[-1]]):
                output.append(stack.pop())
            stack.append(char)
        # Si el carácter es un paréntesis de cierre
        elif char == ')':
            stack.append(char)
        # Si el carácter es un paréntesis de apertura
        elif char == '(':
            while stack and stack[-1] != ')':
                output.append(stack.pop())
            if stack:
                stack.pop()  # Eliminar el paréntesis de cierre ')'
        else:
            output.append(char)

    # Invertimos la salida y unimos los caracteres
    output = output[::-1]
    return ''.join(output)

# Ejemplo de uso
expression = "A+B*C-D"
print(infix_to_prefix(expression))  # Debería imprimir "+A*BC-D"
