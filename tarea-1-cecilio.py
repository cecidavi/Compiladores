def text_to_ascii_hex_bin(text):
    result = []
    for i, char in enumerate(text, start=1):
        ascii_val = ord(char)
        hex_val = format(ascii_val, 'x')
        bin_val = format(ascii_val, 'b')
        result.append(f"{i}: {char} {ascii_val} {hex_val} {bin_val}")
    return result

text = """PROGRAMA ObjetivoFinal;
VARIABLES
  A,B,C: NUMERO;
  X:     NUMERO;
INICIO
  A=10;
  B=20;
  X=A+B; {Operaciones Aritmétoias}
FIN;"""

result = text_to_ascii_hex_bin(text)
for line in result:
    print(line)
