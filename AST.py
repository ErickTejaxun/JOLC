'''
Erick Tejaxún
erickteja@gmail.com 
Compiladores 2
USAC 2021
'''

from abc import ABC, abstractmethod
from enum import Enum

### Tabla de símbolo
class TipoPrimitivo(Enum):
    NULO = 1
    ENTERO = 2
    FLOAT = 3
    BOOL = 4
    CHAR = 5
    STRING = 6
    ARREGLO = 7
    STRUCT = 8

class Tipo():
    def __init__(self, tipo):
        self.tipo = tipo
        self.primitivo = True 
        self.nombre = ""

    def __init__(self, tipo, nombre):
        self.tipo = tipo
        self.primitivo = False
        self.nombre = nombre


class Simbolo():
    def __init__(self, id, tipo, valor, linea, columna):
        self.id = id 
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna
    
    def getTipo(self):
        return self.tipo

class TablaSimbolo():
    def __init__(self):
        self.tabla = []
        self.consola = []

    def registrarSimbolo(self, simbolo):
        self.tabla.append(simbolo)
    
    def getSimbolo(self, id):
        return self.tabla[id]
    
    def imprimirln(self, valor):
        self.consola.append(str(valor))

class Entorno():
    def __init__(self, padre):
        self.tabla = TablaSimbolo()
        self.padre = padre
    
    def getSimbolo(self, id):
        return self.tabla.getSimbolo(id)


### AST 
class NodoAST(ABC):
    pass

### Definición de expresion
class Expresion(NodoAST):

    @abstractmethod
    def getValor(self, tabla):
        pass

    @abstractmethod
    def getTipo(self, tabla):
        pass


## Definición de instruccion
class Instruccion(NodoAST):
    @abstractmethod
    def ejecutar(self, tabla):
        pass

## Instrucciones ------------------------------------------------
class Imprimir(Instruccion):
    def __init__(self, expresion, linea, columna):
        self.expresion = expresion
        self.linea = linea
        self.columna = columna
    
    def ejecutar(self, tabla):
        valor = self.expresion.getValor(tabla)
        tabla.imprimirln(valor)

## Expresion -----------------------------------------------------

class Entero(Expresion):
    def __init__(self, valor, linea, columna):
        self.valor = valor
        self.linea = linea
        self.columna = columna
        self.tipo = Tipo(TipoPrimitivo.ENTERO,'')
    
    def getValor(self, tabla):
        return self.valor
    
    def getTipo(self, tabla):
        return self.tipo


