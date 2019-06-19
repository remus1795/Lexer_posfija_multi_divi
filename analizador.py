#!/usr/bin/python
# -*- coding: utf-8 -*-

import lexer_rules
import parser_rules

from ply.lex import lex
from ply.yacc import yacc
from pila import *
from cola import *

class Variable:

    def __init__(self,nombre,valor):
        self.nombre = nombre
        self._valor = valor

    def set_valor(self,valor):
        self._valor = valor

    def get_valor(self):
        return self._valor

class Analizador:

    def __init__(self):
        self.pila = Pila()
        self.variables = Cola()
        self.operadores = ['-','+','*','/']

    def pos_orden(self,op):
        # Inicializa un nuevo objeto tipo Pila
        self.pila.__init__()
        
        for i in op:
            # Compara con un arreglo de operaciones definido
            if i in self.operadores:
                # Tienen que existir por lo menos dos numeros en la pila para una operación
                if self.pila.get_size() >= 2:
                    a = self.pila.desapilar()
                    b = self.pila.desapilar()
                    if i == '-':
                        self.pila.apilar(b-a)
                    elif i == '+':
                        self.pila.apilar(b+a)
                    elif i == '*':
                        self.pila.apilar(b*a)
                    else:
                        if a != 0:
                            self.pila.apilar(round((b/a),2))
                        else:
                            return "Error - Division por cero"
                else:
                    return "Error - Operación incompleta faltan operandos"
            # Compara si es un digito, de serlo lo apila
            elif i.isdigit():
                try:
                    self.pila.apilar(float(i))
                except ValueError:
                    return "Error - Valor no valido: '" + i + "'"
            else:
                # En caso de tener un "=" se crea una nueva Variable
                if i.find("=") != -1:
                    val = self.pila.desapilar()
                    self.pila.apilar(val)
                    self.variables.encolar(Variable(i.strip("="),val))
                # Cuando existe una variable su valor interno se apila para ser operado
                else:
                    j = 0
                    tam = self.variables.get_size();
                    while j < tam:
                        var = self.variables.desencolar()
                        self.variables.encolar(var)
                        if i == var.nombre:
                            self.pila.apilar(var.get_valor())
                            break
                        j+=1
                    else:
                        return "Error - No se encontro la variable: '" + i + "'"
        # Tiene que existir un unico valor en la pila al finalizar las operaciones
        if self.pila.get_size() == 1:
            return self.pila.desapilar()+"perra"
        else:
            return "Error - Valores sin evaluar"

    def lexer_parser(self,arr):
        lexer = lex(module=lexer_rules)
        parser = yacc(module=parser_rules)
        ast = parser.parse(arr, lexer)
        print ast

        lexer.input(arr)
        token = lexer.token()
        while token is not None:
            print token.type, token.value
            token = lexer.token()
