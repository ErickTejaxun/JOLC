'''
Erick Tejaxún
erickteja@gmail.com 
Compiladores 2
USAC 2021
'''

from abc import ABC, abstractmethod
from enum import Enum
from json import JSONEncoder

from singlenton import global_utils

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

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=2)          


class Simbolo():
    def __init__(self, id, tipo, valor, linea, columna):
        self.id = id 
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna
    
    def getTipo(self):
        return self.tipo

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=2)  

'''Tabla de símbolos -------------------------------------------'''
class TablaSimbolo():
    def __init__(self):
        self.tabla = []
        self.consola = []

    def registrarSimbolo(self, simbolo):
        self.tabla.append(simbolo)
    
    def getSimbolo(self, id):
        entornoActual = self
        return self.tabla[id]
    
    def imprimirln(self, valor):
        self.consola.append(str(valor))

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=2)          

'''Entorno -------------------------------------------------------'''
class Entorno():
    def __init__(self, padre):
        self.tabla = TablaSimbolo()
        self.padre = padre
    
    def getSimbolo(self, id):
        '''Buscamos en el entorno actual y si no está, buscamos en el entorno superior'''
        entornoActual = self
        while entornoActual is not None:
            tmpValor = entornoActual.tabla.getSimbolo(id)
            if tmpValor is None:
                entornoActual = self.padre
            else: 
                return tmpValor
        return None        
    
    def insertSimbolo(self, simbolo):
        self.tabla.registrarSimbolo(simbolo)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=2)         

### AST 
class NodoAST(ABC):
    pass

### Definición de expresion
class Expresion(NodoAST):

    @abstractmethod
    def getValor(self, entorno):
        pass

    @abstractmethod
    def getTipo(self, entorno):
        pass


## Definición de instruccion
class Instruccion(NodoAST):
    @abstractmethod
    def ejecutar(self, entorno):
        pass

## Instrucciones ------------------------------------------------
class Imprimir(Instruccion):
    def __init__(self, expresion, linea, columna):
        self.expresion = expresion
        self.linea = linea
        self.columna = columna
    
    def ejecutar(self, entorno):
        valor = self.expresion.getValor(entorno)
        entorno.tabla.imprimirln(valor)

class Bloque(Instruccion):
    def __init__(self, linea, columna):
        self.linea = linea
        self.columna = columna
        self.instrucciones = []
    
    def agregarInstruccion(self, instruccion):
        self.instrucciones.append(instruccion)
    
    def ejecutar(self, entorno):
        for inst in self.instrucciones:
            inst.ejecutar(entorno)

## Expresion -----------------------------------------------------

class Entero(Expresion):
    def __init__(self, valor, linea, columna):
        self.valor = valor
        self.linea = linea
        self.columna = columna
        self.tipo = Tipo(TipoPrimitivo.ENTERO,'')
    
    def getValor(self, entorno):
        return self.valor
    
    def getTipo(self, entorno):
        return self.tipo


