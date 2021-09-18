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
import math

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

NOMBRES = {
    1: 'Nulo',
    2: 'int',
    3: 'float',
    4: 'bool',
    5: 'char',
    6: 'string',
    7: 'arreglo',
    8: 'struct',
    9: 'error'
}

class Tipo():
    def __init__(self, tipo, primitivo = True,  nombre=""):
        self.tipo = tipo
        self.primitivo = primitivo
        self.nombre = nombre

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=2) 
        
    def getNombre(self):
        if self.tipo == TipoPrimitivo.NULO:
            return 'nulo'
        if self.tipo == TipoPrimitivo.ENTERO:
            return 'entero'
        if self.tipo ==  TipoPrimitivo.FLOAT:
            return 'float'
        if self.tipo ==  TipoPrimitivo.BOOL:
            return 'bool'
        if self.tipo ==  TipoPrimitivo.CHAR:
            return 'char'
        if self.tipo ==  TipoPrimitivo.STRING:
            return 'cadena'
        if self.tipo ==  TipoPrimitivo.ARREGLO:
            return 'arreglo'
        if self.tipo ==  TipoPrimitivo.STRUCT:
            return 'struct'
        if self.tipo ==  TipoPrimitivo.ERROR:
            return 'error'        

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

    def imprimir(self, valor):
        if len(self.consola) > 0:
            texto = self.consola[len(self.consola)-1]        
            self.consola[len(self.consola)-1] = texto+str(valor)
        else: 
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

class Imprimir(Instruccion):
    def __init__(self, lista_expresiones, linea, columna):
        self.lista_expresiones = lista_expresiones
        self.linea = linea
        self.columna = columna
    
    def ejecutar(self, entorno):
        cadena = ''
        for exp in self.lista_expresiones:
            valor = exp.getValor(entorno)
            cadena = cadena + valor
        entorno.tabla.imprimir(cadena)

class ImprimirLn(Instruccion):
    def __init__(self, lista_expresiones, linea, columna):
        self.lista_expresiones = lista_expresiones
        self.linea = linea
        self.columna = columna
    
    def ejecutar(self, entorno):
        cadena = ''
        for exp in self.lista_expresiones:
            valor = exp.getValor(entorno)
            cadena = cadena + valor
        entorno.tabla.imprimirln(cadena)        

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
            global_utils.registrySemanticError('+','Error Semántico. No es posible realizar la operación ' + tipoI.getNombre() + " + " + tipoD.getNombre() , self.linea, self.columna)
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

        global_utils.registrySemanticError('-','Error Semántico. No es posible realizar la operación ' + tipoI.getNombre() + " - " + tipoD.getNombre(), self.linea, self.columna)
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


class Multiplicacion(Expresion):
    def __init__(self, expresionI, expresionD, linea, columna):
        self.expresionI = expresionI
        self.expresionD = expresionD
        self.linea = linea
        self.columna = columna
    
    def getTipo(self, entorno):
        tipoI = self.expresionI.getTipo(entorno)
        tipoD = self.expresionD.getTipo(entorno)

        ## Si ambos son string se hace una concatenacion
        if(tipoI.esCadena() and tipoD.esCadena()):
            return Tipo(TipoPrimitivo.STRING)

        if (tipoI.esNumerico() and tipoD.esNumerico()):
            if (tipoI.esFloat() or tipoD.esFloat()):
                return Tipo(TipoPrimitivo.FLOAT)
            return Tipo(TipoPrimitivo.ENTERO)

        global_utils.registrySemanticError('*','Error Semántico. No es posible realizar la operación ' + tipoI.getNombre() + " * " + tipoD.getNombre() , self.linea, self.columna)
        return Tipo(TipoPrimitivo.ERROR)        
    
    def getValor(self, entorno):
        tipo_actual = self.getTipo(entorno)

        if tipo_actual.esError():
            return None
            
        valorI = self.expresionI.getValor(entorno)
        valorD = self.expresionD.getValor(entorno)            

        if tipo_actual.esCadena():
            self.valor = str(valorI) + str(valorD)
            return self.valor

        if tipo_actual.esFloat():
            self.valor = float(valorI) * float(valorD)
            return self.valor
            
        if tipo_actual.esEntero():            
            self.valor = int(valorI) * int(valorD)
            return self.valor
        
        return None 


class Division(Expresion):
    def __init__(self, expresionI, expresionD, linea, columna):
        self.expresionI = expresionI
        self.expresionD = expresionD
        self.linea = linea
        self.columna = columna
    
    def getTipo(self, entorno):
        tipoI = self.expresionI.getTipo(entorno)
        tipoD = self.expresionD.getTipo(entorno)

        if (tipoI.esNumerico() and tipoD.esNumerico()):
            return Tipo(TipoPrimitivo.FLOAT)

        global_utils.registrySemanticError('/','Error Semántico. No es posible realizar la operación ' + tipoI.getNombre() + " / " + tipoD.getNombre() , self.linea, self.columna)
        return Tipo(TipoPrimitivo.ERROR)        
    
    def getValor(self, entorno):
        tipo_actual = self.getTipo(entorno)

        if tipo_actual.esError():
            return None
            
        if tipo_actual.esFloat():
            valorI = self.expresionI.getValor(entorno)
            valorD = self.expresionD.getValor(entorno)
            self.valor = float(valorI) / float(valorD)
            return self.valor
            
        if tipo_actual.esEntero():            
            valorI = self.expresionI.getValor(entorno)
            valorD = self.expresionD.getValor(entorno)
            self.valor = int(valorI) / int(valorD)
            return self.valor
        
        return None  

class Potencia(Expresion):
    def __init__(self, expresionI, expresionD, linea, columna):
        self.expresionI = expresionI
        self.expresionD = expresionD
        self.linea = linea
        self.columna = columna
    
    def getTipo(self, entorno):
        tipoI = self.expresionI.getTipo(entorno)
        tipoD = self.expresionD.getTipo(entorno)

        if (tipoI.esNumerico() and tipoD.esNumerico()):
            if(tipoI.esFloat() or tipoD.esFloat()):
                return Tipo(TipoPrimitivo.FLOAT)
            else:
                return Tipo(TipoPrimitivo.ENTERO)

        if (tipoI.esCadena() and tipoD.esEntero()):
            return Tipo(TipoPrimitivo.STRING)

        global_utils.registrySemanticError('^','Error Semántico. No es posible realizar la operación ' + tipoI.getNombre() + " ^ " + tipoD.getNombre() , self.linea, self.columna)
        return Tipo(TipoPrimitivo.ERROR)        
    
    def getValor(self, entorno):
        tipo_actual = self.getTipo(entorno)

        if tipo_actual.esError():
            return None
            
        if tipo_actual.esFloat():
            valorI = self.expresionI.getValor(entorno)
            valorD = self.expresionD.getValor(entorno)
            self.valor = float(pow(valorI, valorD))
            return self.valor
            
        if tipo_actual.esEntero():            
            valorI = self.expresionI.getValor(entorno)
            valorD = self.expresionD.getValor(entorno)
            self.valor = int(pow(valorI,valorD))
            return self.valor

        if tipo_actual.esCadena():
            valorI = self.expresionI.getValor(entorno)
            valorD = self.expresionD.getValor(entorno)
            self.valor = '' 
            contador = 0 
            while ( contador < valorD):
                self.valor = self.valor + str(valorI)
                contador = contador + 1
            return self.valor
        
        return None    

class Modulo(Expresion):
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

        global_utils.registrySemanticError('-','Error Semántico. No es posible realizar la operación ' + tipo.getNombre() + " - " + tipo.getNombre() , self.linea, self.columna)
        return Tipo(TipoPrimitivo.ERROR)        
    
    def getValor(self, entorno):
        tipo_actual = self.getTipo(entorno)

        if tipo_actual.esError():
            return None
            
        valorI = self.expresionI.getValor(entorno)
        valorD = self.expresionD.getValor(entorno)

        if tipo_actual.esFloat():            
            self.valor = float(valorI) % float(valorD)
            return self.valor
            
        if tipo_actual.esEntero():                        
            self.valor = int(valorI) % int(valorD)
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

        global_utils.registrySemanticError('-','Error Semántico. No es posible realizar la operación (-) ' + tipo.getNombre() , self.linea, self.columna)
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

class Uppercase(Expresion):
    def __init__(self, expresion, linea, columna):
        self.expresion = expresion
        self.linea = linea
        self.columna = columna
    
    def getTipo(self, entorno):
        tipo_tmp = self.expresion.getTipo(entorno)
        if tipo_tmp.esCadena():
            return Tipo(TipoPrimitivo.STRING)
        return Tipo(TipoPrimitivo.ERROR)
    
    def getValor(self, entorno):
        tipo_tmp = self.getTipo(entorno)
        if tipo_tmp.esCadena():
            valor  = self.expresion.getValor(entorno)
            self.valor = str(valor).upper()
            return self.valor
        return None

class Lowercase(Expresion):
    def __init__(self, expresion, linea, columna):
        self.expresion = expresion
        self.linea = linea
        self.columna = columna
    
    def getTipo(self, entorno):
        tipo_tmp = self.expresion.getTipo(entorno)
        if tipo_tmp.esCadena():
            return Tipo(TipoPrimitivo.STRING)
        global_utils.registrySemanticError('lowercase','Esta primitiva solo acepta valores de tipo Cadena, se ha recibido un valor de tipo' + tipo_tmp.getNombre() , self.linea, self.columna)
        return Tipo(TipoPrimitivo.ERROR)
    
    def getValor(self, entorno):
        tipo_tmp = self.getTipo(entorno)
        if tipo_tmp.esCadena():
            valor  = self.expresion.getValor(entorno)
            self.valor = str(valor).lower()
            return self.valor
        return None

class Log10(Expresion):
    def __init__(self, expresion, linea, columna):
        self.expresion = expresion
        self.linea = linea
        self.columan = columna
    
    def getTipo(self, entorno):
        tipo_tmp = self.expresion.getTipo(entorno)
        if tipo_tmp.esNumerico():
            return tipo_tmp
        return Tipo(TipoPrimitivo.ERROR)
    
    def getValor(self, entorno):
        tipo_tmp = self.getTipo(entorno)
        if tipo_tmp.esNumerico():
            valor = self.expresion.getValor(entorno)            
            self.valor = math.log10(valor)
            return self.valor
        return None
        

class Log(Expresion):
    def __init__(self, expresionI, expresionD, linea, columna):
        self.expresionI = expresionI
        self.expresionD = expresionD
        self.linea = linea
        self.columan = columna
    
    def getTipo(self, entorno):
        tipoI = self.expresionI.getTipo(entorno)
        tipoD = self.expresionD.getTipo(entorno)
        if tipoI.esNumerico() and tipoD.esNumerico():
            return tipoI
        return Tipo(TipoPrimitivo.ERROR)
    
    def getValor(self, entorno):
        tipo_tmp = self.getTipo(entorno)
        if tipo_tmp.esNumerico():
            valorI = self.expresionI.getValor(entorno)
            valorD = self.expresionD.getValor(entorno)            
            self.valor = math.log(valorD, valorI)
            return self.valor
        return None
                
class Sin(Expresion):
    def __init__(self, expresion, linea, columna):
        self.expresion = expresion        
        self.linea = linea
        self.columan = columna
    
    def getTipo(self, entorno):
        tipo = self.expresion.getTipo(entorno)        
        if tipo.esNumerico():
            return tipo
        return Tipo(TipoPrimitivo.ERROR)
    
    def getValor(self, entorno):
        tipo_tmp = self.getTipo(entorno)
        if tipo_tmp.esNumerico():
            valor = self.expresion.getValor(entorno)            
            self.valor = math.sin(valor)
            return self.valor
        return None
                

class Cos(Expresion):
    def __init__(self, expresion, linea, columna):
        self.expresion = expresion        
        self.linea = linea
        self.columan = columna
    
    def getTipo(self, entorno):
        tipo = self.expresion.getTipo(entorno)        
        if tipo.esNumerico():
            return tipo
        return Tipo(TipoPrimitivo.ERROR)
    
    def getValor(self, entorno):
        tipo_tmp = self.getTipo(entorno)
        if tipo_tmp.esNumerico():
            valor = self.expresion.getValor(entorno)            
            self.valor = math.cos(valor)
            return self.valor
        return None                

class Tan(Expresion):
    def __init__(self, expresion, linea, columna):
        self.expresion = expresion        
        self.linea = linea
        self.columan = columna
    
    def getTipo(self, entorno):
        tipo = self.expresion.getTipo(entorno)        
        if tipo.esNumerico():
            return tipo
        return Tipo(TipoPrimitivo.ERROR)
    
    def getValor(self, entorno):
        tipo_tmp = self.getTipo(entorno)
        if tipo_tmp.esNumerico():
            valor = self.expresion.getValor(entorno)            
            self.valor = math.tan(valor)
            return self.valor
        return None     

class Sqrt(Expresion):
    def __init__(self, expresion, linea, columna):
        self.expresion = expresion        
        self.linea = linea
        self.columan = columna
    
    def getTipo(self, entorno):
        tipo = self.expresion.getTipo(entorno)        
        if tipo.esNumerico():
            return tipo
        return Tipo(TipoPrimitivo.ERROR)
    
    def getValor(self, entorno):
        tipo_tmp = self.getTipo(entorno)
        if tipo_tmp.esNumerico():
            valor = self.expresion.getValor(entorno)            
            self.valor = math.sqrt(valor)
            return self.valor
        return None     

## Operaciones Relacionales ---------------------
class Mayor(Expresion):
    def __init__(self, expresionI, expresionD, linea, columna):
        self.expresionI = expresionI
        self.expresionD = expresionD
        self.linea = linea
        self.columna = columna
    
    def getTipo(self, entorno):
        tipoI = self.expresionI.getTipo(entorno)
        tipoD = self.expresionI.getTipo(entorno)
        if tipoI.esNumerico() and tipoD.esNumerico():
            return tipoI
        if tipoI.esCadena() and tipoD.esCadena():
            return tipoI
        global_utils.registrySemanticError('>','No es posible realizar la operación ' + tipoI.getNombre() + ' > '+ tipoD.getNombre() , self.linea, self.columna)
        return Tipo(TipoPrimitivo.ERROR)

    def getValor(self, entorno):
        tipo_tmp = self.getTipo(entorno)
        if tipo_tmp.esError():
            return None
        valorI = self.expresionI.getValor(entorno)
        valorD = self.expresionD.getValor(entorno)
        if tipo_tmp.esNumerico():        
            self.valor = valorI > valorD
            return self.valor
        if tipo_tmp.esCadena():
            self.valor = valorI > valorD
            return self.valor

class MayorIgual(Expresion):
    def __init__(self, expresionI, expresionD, linea, columna):
        self.expresionI = expresionI
        self.expresionD = expresionD
        self.linea = linea
        self.columna = columna
    
    def getTipo(self, entorno):
        tipoI = self.expresionI.getTipo(entorno)
        tipoD = self.expresionI.getTipo(entorno)
        if tipoI.esNumerico() and tipoD.esNumerico():
            return tipoI
        if tipoI.esCadena() and tipoD.esCadena():
            return tipoI
        global_utils.registrySemanticError('>=','No es posible realizar la operación ' + tipoI.getNombre() + ' >= '+ tipoD.getNombre() , self.linea, self.columna)
        return Tipo(TipoPrimitivo.ERROR)

    def getValor(self, entorno):
        tipo_tmp = self.getTipo(entorno)
        if tipo_tmp.esError():
            return None
        valorI = self.expresionI.getValor(entorno)
        valorD = self.expresionD.getValor(entorno)
        if tipo_tmp.esNumerico():        
            self.valor = valorI >= valorD
            return self.valor
        if tipo_tmp.esCadena():
            self.valor = valorI >= valorD
            return self.valor            

class Menor(Expresion):
    def __init__(self, expresionI, expresionD, linea, columna):
        self.expresionI = expresionI
        self.expresionD = expresionD
        self.linea = linea
        self.columna = columna
    
    def getTipo(self, entorno):
        tipoI = self.expresionI.getTipo(entorno)
        tipoD = self.expresionI.getTipo(entorno)
        if tipoI.esNumerico() and tipoD.esNumerico():
            return tipoI
        if tipoI.esCadena() and tipoD.esCadena():
            return tipoI
        global_utils.registrySemanticError('<','No es posible realizar la operación ' + tipoI.getNombre() + ' < '+ tipoD.getNombre() , self.linea, self.columna)
        return Tipo(TipoPrimitivo.ERROR)

    def getValor(self, entorno):
        tipo_tmp = self.getTipo(entorno)
        if tipo_tmp.esError():
            return None
        valorI = self.expresionI.getValor(entorno)
        valorD = self.expresionD.getValor(entorno)
        if tipo_tmp.esNumerico():        
            self.valor = valorI < valorD
            return self.valor
        if tipo_tmp.esCadena():
            self.valor = valorI < valorD
            return self.valor    

class MenorIgual(Expresion):
    def __init__(self, expresionI, expresionD, linea, columna):
        self.expresionI = expresionI
        self.expresionD = expresionD
        self.linea = linea
        self.columna = columna
    
    def getTipo(self, entorno):
        tipoI = self.expresionI.getTipo(entorno)
        tipoD = self.expresionI.getTipo(entorno)
        if tipoI.esNumerico() and tipoD.esNumerico():
            return tipoI
        if tipoI.esCadena() and tipoD.esCadena():
            return tipoI
        global_utils.registrySemanticError('<=','No es posible realizar la operación ' + tipoI.getNombre() + ' <= '+ tipoD.getNombre() , self.linea, self.columna)
        return Tipo(TipoPrimitivo.ERROR)

    def getValor(self, entorno):
        tipo_tmp = self.getTipo(entorno)
        if tipo_tmp.esError():
            return None
        valorI = self.expresionI.getValor(entorno)
        valorD = self.expresionD.getValor(entorno)
        if tipo_tmp.esNumerico():        
            self.valor = valorI <= valorD
            return self.valor
        if tipo_tmp.esCadena():
            self.valor = valorI <= valorD
            return self.valor                       

class Or(Expresion):
    def __init__(self, expresionI, expresionD, linea, columna):
        self.expresionI = expresionI 
        self.expresionD = expresionD
        self.linea = linea
        self.columna = columna
    
    def getTipo(self, entorno):
        tipoI = self.expresionI.getTipo(entorno)
        tipoD = self.expresionD.getTipo(entorno)
        if tipoI.esBool() and tipoD.esBool():
            return tipoI
        return Tipo(TipoPrimitivo.Error)
    
    def getValor(self, entorno):
        tipo_tmp = self.getTipo(entorno)
        if tipo_tmp.esBool():
            valorI = self.expresionI.getValor(entorno)
            valorD = self.expresionD.getValor(entorno)
            self.valor = valorI or valorD
            return self.valor
        return None

class And(Expresion):
    def __init__(self, expresionI, expresionD, linea, columna):
        self.expresionI = expresionI 
        self.expresionD = expresionD
        self.linea = linea
        self.columna = columna
    
    def getTipo(self, entorno):
        tipoI = self.expresionI.getTipo(entorno)
        tipoD = self.expresionD.getTipo(entorno)
        if tipoI.esBool() and tipoD.esBool():
            return tipoI
        return Tipo(TipoPrimitivo.Error)
    
    def getValor(self, entorno):
        tipo_tmp = self.getTipo(entorno)
        if tipo_tmp.esBool():
            valorI = self.expresionI.getValor(entorno)
            valorD = self.expresionD.getValor(entorno)
            self.valor = valorI and valorD
            return self.valor
        return None        

class Not(Expresion):
    def __init__(self, expresion, linea, columna):
        self.expresion = expresion
        self.linea = linea
        self.columna = columna
    
    def getTipo(self, entorno):
        tipo = self.expresion.getTipo(entorno)
        if tipo.esBool():
            return tipo
        return Tipo(TipoPrimitivo.ERROR)
    
    def getValor(self, entorno):
        tipo_tmp = self.getTipo(entorno)
        if tipo_tmp.esBool():
            valor = self.expresion.getValor(entorno)
            self.valor = not valor
            return self.valor
        return None

