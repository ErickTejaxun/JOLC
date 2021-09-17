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
    ERROR = 9

class Tipo():
    def __init__(self, tipo, primitivo = True,  nombre=""):
        self.tipo = tipo
        self.primitivo = primitivo
        self.nombre = nombre

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=2) 

    def esCadena(self):
        return self.tipo == TipoPrimitivo.STRING
    def esNulo(self):
        return self.tipo == TipoPrimitivo.NULO
    def esEntero(self):
        return self.tipo == TipoPrimitivo.ENTERO
    def esFloat(self):
        return self.tipo == TipoPrimitivo.FLOAT
    def esBool(self):
        return self.tipo == TipoPrimitivo.BOOL 
    def esChar(self):
        return self.tipo == TipoPrimitivo.CHAR
    def esError(self):
        return self.tipo == TipoPrimitivo.ERROR
    def esNumerico(self):
        return self.tipo == TipoPrimitivo.ENTERO or self.tipo == TipoPrimitivo.FLOAT 


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

class Suma(Expresion):
    def __init__(self, expresionI, expresionD, linea, columna):
        self.expresionI = expresionI
        self.expresionD = expresionD
        self.linea = linea
        self.columna = columna
    
    def getTipo(self, entorno):
        tipoI = self.expresionI.getTipo(entorno)
        tipoD = self.expresionD.getTipo(entorno)

        if(tipoI.esCadena() or tipoD.esCadena()):        
            global_utils.registrySemanticError('+','Error Semántico. No es posible realizar la operación ' + tipoI + " + " + tipoD , self.linea, self.columna)
            return Tipo(TipoPrimitivo.ERROR)
        if(tipoI.esFloat() or tipoD.esFloat()):
            return Tipo(TipoPrimitivo.FLOAT)
        return Tipo(TipoPrimitivo.ENTERO)
    
    def getValor(self, entorno):
        tipo_actual = self.getTipo(entorno)

        if tipo_actual.esError():
            return None

        if tipo_actual.esFloat():
            valorI = self.expresionI.getValor(entorno)
            valorD = self.expresionD.getValor(entorno)
            self.valor = float(valorI) + float(valorD)
            return self.valor
            
        if tipo_actual.esEntero():            
            valorI = self.expresionI.getValor(entorno)
            valorD = self.expresionD.getValor(entorno)
            self.valor = int(valorI)+ int(valorD)
            return self.valor
        
        return None


class Resta(Expresion):
    def __init__(self, expresionI, expresionD, linea, columna):
        self.expresionI = expresionI
        self.expresionD = expresionD
        self.linea = linea
        self.columna = columna
    
    def getTipo(self, entorno):
        tipoI = self.expresionI.getTipo(entorno)
        tipoD = self.expresionD.getTipo(entorno)

        if (tipoI.esNumerico() and tipoD.esNumerico()):
            if (tipoI.esFloat() or tipoD.esFloat()):
                return Tipo(TipoPrimitivo.FLOAT)
            return Tipo(TipoPrimitivo.ENTERO)

        global_utils.registrySemanticError('-','Error Semántico. No es posible realizar la operación ' + tipoI + " - " + tipoD , self.linea, self.columna)
        return Tipo(TipoPrimitivo.ERROR)        
    
    def getValor(self, entorno):
        tipo_actual = self.getTipo(entorno)

        if tipo_actual.esError():
            return None
            
        if tipo_actual.esFloat():
            valorI = self.expresionI.getValor(entorno)
            valorD = self.expresionD.getValor(entorno)
            self.valor = float(valorI) - float(valorD)
            return self.valor
            
        if tipo_actual.esEntero():            
            valorI = self.expresionI.getValor(entorno)
            valorD = self.expresionD.getValor(entorno)
            self.valor = int(valorI) - int(valorD)
            return self.valor
        
        return None        
        
class Negativo(Expresion):
    def __init__(self, expresion, linea, columna):
        self.expresion = expresion        
        self.linea = linea
        self.columna = columna
    
    def getTipo(self, entorno):
        tipo = self.expresion.getTipo(entorno)        

        if tipo.esNumerico():
            if tipo.esFloat():
                return Tipo(TipoPrimitivo.FLOAT)
            return Tipo(TipoPrimitivo.ENTERO)

        global_utils.registrySemanticError('-','Error Semántico. No es posible realizar la operación (-) ' + tipoD , self.linea, self.columna)
        return Tipo(TipoPrimitivo.ERROR)        
    
    def getValor(self, entorno):
        tipo_actual = self.getTipo(entorno)

        if tipo_actual.esError():
            return None
            
        valor = self.expresion.getValor(entorno)
        if tipo_actual.esFloat():                        
            self.valor = float(valor) * -1 
            return self.valor
            
        if tipo_actual.esEntero():                                            
            self.valor = int(valor) * -1 
            return self.valor

        return None  



class Nulo(Expresion):
    def __init__(self, linea, columna):        
        self.linea = linea
        self.columna = columna
        self.valor = None
        self.tipo = Tipo(TipoPrimitivo.NULO,'')
    
    def getValor(self, entorno):
        return self.valor
    
    def getTipo(self, entorno):
        return self.tipo

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

class Float(Expresion):
    def __init__(self, valor, linea, columna):
        self.valor = valor
        self.linea = linea
        self.columna = columna
        self.tipo = Tipo(TipoPrimitivo.FLOAT,'')
    
    def getValor(self, entorno):
        return self.valor
    
    def getTipo(self, entorno):
        return self.tipo


class Bool(Expresion):
    def __init__(self, valor, linea, columna):
        self.valor = valor
        self.linea = linea
        self.columna = columna
        self.tipo = Tipo(TipoPrimitivo.BOOL,'')
    
    def getValor(self, entorno):
        return self.valor
    
    def getTipo(self, entorno):
        return self.tipo


class Char(Expresion):
    def __init__(self, valor, linea, columna):
        self.valor = valor
        self.linea = linea
        self.columna = columna
        self.tipo = Tipo(TipoPrimitivo.CHAR,'')
    
    def getValor(self, entorno):
        return self.valor
    
    def getTipo(self, entorno):
        return self.tipo

class String(Expresion):
    def __init__(self, valor, linea, columna):
        self.valor = valor
        self.linea = linea
        self.columna = columna
        self.tipo = Tipo(TipoPrimitivo.STRING,'')
    
    def getValor(self, entorno):
        return self.valor
    
    def getTipo(self, entorno):
        return self.tipo        