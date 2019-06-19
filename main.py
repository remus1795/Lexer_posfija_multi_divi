from analizador import *

with open("operaciones.txt",'rU') as f:
    content = f.readlines()

analisis = Analizador()

for i in content:
    content = i.strip('\n').split(' ') 
    analisis.pos_orden(content)
    analisis.lexer_parser(i)
