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


consola = []


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
    DINAMICO =20

class Rol(Enum):
    VAR = 10
    FUNCION = 11

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
            return 'Int64'
        if self.tipo ==  TipoPrimitivo.FLOAT:
            return 'Float64'
        if self.tipo ==  TipoPrimitivo.BOOL:
            return 'Bool'
        if self.tipo ==  TipoPrimitivo.CHAR:
            return 'char'
        if self.tipo ==  TipoPrimitivo.STRING:
            return 'String'
        if self.tipo ==  TipoPrimitivo.ARREGLO:
            return 'arreglo'
        if self.tipo ==  TipoPrimitivo.STRUCT:
            return 'struct'
        if self.tipo ==  TipoPrimitivo.DINAMICO:
            return 'dinamico'            
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
    def esArreglo(self):
        return self.tipo == TipoPrimitivo.ARREGLO
    def esLlamada(self):
        return self.tipo == TipoPrimitivo.LLAMADA   
    def esDinamico(self):
        return self.tipo == TipoPrimitivo.DINAMICO              
    def esNumerico(self):
        return self.tipo == TipoPrimitivo.ENTERO or self.tipo == TipoPrimitivo.FLOAT 
    def compararTipo(self, tipo):
        return self.tipo == tipo.tipo


class Simbolo():
    def __init__(self, id, tipo, valor, linea, columna):
        self.id = id 
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna
        self.rol = Rol.VAR
    
    def getTipo(self):
        return self.tipo

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=2)

    def getRol(self):
        if self.rol == Rol.FUNCION:
            return 'funcion'
        if self.rol == Rol.VAR:
            return 'variable'              

class FuncionSimbolo(Simbolo):
    def __init__(self, id, parametros, instrucciones, linea, columna):
        self.id = id 
        self.parametros = parametros
        self.rol = Rol.FUNCION
        self.linea = linea 
        self.columna = columna 
        self.instrucciones = instrucciones
        self.tipo = Tipo(TipoPrimitivo.DINAMICO)

    def getTipo(self, entorno):
        tmp = self.instrucciones.ejecutar(entorno)
        if tmp is None:
            return Tipo(TipoPrimitivo.ERROR)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=2)
    def getRol(self):
        if self.rol == Rol.FUNCION:
            return 'funcion'
        if self.rol == Rol.VAR:
            return 'variable'



'''Tabla de símbolos -------------------------------------------'''
class TablaSimbolo():
    def __init__(self):
        self.tabla = {}
        self.consola = []

    def registrarSimbolo(self, simbolo):        
        tmp_simbolo = self.tabla.get(simbolo.id)
        if tmp_simbolo is not None:
            if tmp_simbolo.rol == simbolo.rol:
                if tmp_simbolo.rol == Rol.VAR:
                    global_utils.registrySemanticError('Declaracion', 'Ya se ha declarado previamente una variable con el nombre '+ simbolo.id, simbolo.linea, simbolo.columna)
                    return 
                else:
                    if simbolo.parametros is None or tmp_simbolo.parametros is None:
                        global_utils.registrySemanticError('Declaracion', 'Ya se ha declarado previamente una función con el nombre '+ simbolo.id + ' con 0 parámetros.', simbolo.linea, simbolo.columna)
                        return                         
                    if len(simbolo.parametros) == len(tmp_simbolo.parametros):                        
                        global_utils.registrySemanticError('Declaracion', 'Ya se ha declarado previamente una función con el nombre '+ simbolo.id + ' con ' +str(len(simbolo.parametros)) + ' parámetros.', simbolo.linea, simbolo.columna)
                        return                     
                    else:                        
                        self.tabla[simbolo.id] = simbolo                    
            else:
                self.tabla[simbolo.id] = simbolo

        else:
            self.tabla[simbolo.id] = simbolo
    
    def getSimbolo(self, id):
        entornoActual = self
        return self.tabla.get(id)

    def getFuncion(self, id, numero_parametros):
        entornoActual = self
        return self.tabla.get(id)        
    
    def imprimirln(self, valor):        
        global consola
        consola.append(str(valor))

    def imprimir(self, valor):
        global consola
        if len(consola) > 0:
            texto = consola[len(consola)-1]        
            consola[len(consola)-1] = texto+str(valor)
        else:             
            consola.append(str(valor))

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
                entornoActual = entornoActual.padre
            else: 
                return tmpValor
        return None        
    
    def insertSimbolo(self, simbolo):
        self.tabla.registrarSimbolo(simbolo)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=2)  

    '''
    NULO = 1
    ENTERO = 2
    FLOAT = 3
    BOOL = 4
    CHAR = 5
    STRING = 6
    ARREGLO = 7
    STRUCT = 8
    ERROR = 9
    '''
    def obtenerTipo(self, valor):
        if valor is None:
            return Tipo(TipoPrimitivo.NULO)
        if isinstance(valor, int):
            return Tipo(TipoPrimitivo.ENTERO)
        if isinstance(valor, float):
            return Tipo(TipoPrimitivo.FLOAT)
        if isinstance(valor, bool):
            return Tipo(TipoPrimitivo.BOOL)
        if isinstance(valor, str):
            return Tipo(TipoPrimitivo.STRING)            
        if isinstance(valor, Simbolo):
            return valor.tipo
        return Tipo(TipoPrimitivo.ERROR)
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

    @abstractmethod
    def graficar(self, padre, grafo):
        pass    


## Definición de instruccion
class Instruccion(NodoAST):
    @abstractmethod
    def ejecutar(self, entorno):
        pass

    @abstractmethod
    def graficar(self, padre, grafo):
        pass       

## Instrucciones ------------------------------------------------
class Bloque(Instruccion):
    def __init__(self, linea, columna):
        self.linea = linea
        self.columna = columna
        self.instrucciones = []
    
    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self))
        grafo.node(id, '(Inst)Bloque_Instrucciones')
        grafo.edge(padre, id)
        for inst in self.instrucciones:
            inst.graficar(id, grafo)
        


    def agregarInstruccion(self, instruccion):
        self.instrucciones.append(instruccion)
    
    def ejecutar(self, entorno):
        for inst in self.instrucciones:
            if isinstance(inst, Break):
                return inst
            elif isinstance(inst, Continue):
                return inst
            elif isinstance(inst, Retorno):
                return inst.ejecutar(entorno)
            else:
                if isinstance(inst, Instruccion):
                    val = inst.ejecutar(entorno)
                    if val is not None:
                        if isinstance(val, Break):
                            return val
                        if isinstance(val, Continue):
                            return val
                        return val
                elif isinstance(inst, Expresion):
                    val = inst.getValor(entorno)
                    if val is not None:
                        if isinstance(val, Break):
                            return val
                        if isinstance(val, Continue):
                            return val                    


class Imprimir(Instruccion):
    def __init__(self, lista_expresiones, linea, columna):
        self.lista_expresiones = lista_expresiones
        self.linea = linea
        self.columna = columna

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self))
        grafo.node(id, '(Inst)Imprimir')
        grafo.edge(padre, id)
        for inst in self.lista_expresiones:
            inst.graficar(id, grafo)        
    
    def ejecutar(self, entorno):
        cadena = ''
        for exp in self.lista_expresiones:
            tipo_tmp = exp.getTipo(entorno)
            if tipo_tmp is not None:
                if tipo_tmp.esArreglo():                    
                    cadena = self.imprimirArreglo(exp, entorno, cadena)
                elif not tipo_tmp.esError():
                    valor = exp.getValor(entorno)
                    if valor == None:
                        valor = 'nothing'
                    cadena = str(cadena) + str(valor)
        entorno.tabla.imprimir(cadena)

    def imprimirArreglo(self, exp, entorno, cadena):        
        valor = exp.getValor(entorno)
        if valor is None:
            valor = exp.valor
        for i in valor:
            if i.tipo.esArreglo():
                cadena = self.imprimirArreglo(i, entorno, cadena)
            elif not i.tipo.esError():                           
                cadena = str(cadena) + str(i.valor)
        return cadena
        

class ImprimirLn(Instruccion):
    def __init__(self, lista_expresiones, linea, columna):
        self.lista_expresiones = lista_expresiones
        self.linea = linea
        self.columna = columna
        
    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self))
        grafo.node(id, '(Inst)ImprimirLn')
        grafo.edge(padre, id)
        for inst in self.lista_expresiones:
            inst.graficar(id, grafo)  

    def ejecutar(self, entorno):
        cadena = ''
        for exp in self.lista_expresiones:
            if not isinstance(exp, Llamada):
                tipo_tmp = exp.getTipo(entorno)
                if tipo_tmp is not None:                
                    if tipo_tmp.esArreglo():                    
                        cadena = '[' + self.imprimirArreglo(exp, entorno, cadena) + ']'                        
                    elif not tipo_tmp.esError():
                        valor = exp.getValor(entorno)
                        if valor == None:
                            valor = 'nothing'
                        cadena = str(cadena) + str(valor)
            else:
                valor = exp.getValor(entorno)
                tipo_tmp = entorno.obtenerTipo(valor)
                if tipo_tmp is not None:                
                    if tipo_tmp.esArreglo():                    
                        cadena = '[' + self.imprimirArreglo(exp, entorno, cadena) + ']'
                    elif not tipo_tmp.esError():                        
                        if valor == None:
                            valor = 'nothing'
                        cadena = str(cadena) + str(valor)                

        entorno.tabla.imprimirln(cadena) 

    def imprimirArreglo(self, exp, entorno, cadena):  
        if isinstance(exp, Simbolo):
            valor = exp.valor
            for i in valor:
                if i.tipo.esArreglo():                
                    cadena = '[' + self.imprimirArreglo(i, entorno, cadena) + ']'
                elif not i.tipo.esError():
                    if len(cadena) > 0:
                        if cadena[len(cadena)-1] !='[':
                            cadena = str(cadena) + ',' +  str(i.valor)            
                        else:
                            cadena = str(cadena) + str(i.valor) 
                    else:           
                        cadena = str(cadena) + str(i.valor) 
            return cadena
        else:
            valor = exp.getValor(entorno)
            if valor is None:
                valor = exp.valor
            for i in valor:
                if i.tipo.esArreglo():                
                    cadena = cadena + '[' + self.imprimirArreglo(i, entorno, cadena)+ ']'
                elif not i.tipo.esError():
                    if len(cadena) > 0:
                        if cadena[len(cadena)-1] !='[':
                            cadena = str(cadena) + ',' + str(i.valor)
                        else:        
                            cadena = str(cadena) +  str(i.valor)
                    else:
                        cadena = str(cadena) +  str(i.valor)
            return cadena


class Declaracion(Instruccion):
    def __init__(self, id, expresion, tipo , linea, columna):
        self.id = id
        self.expresion = expresion
        self.tipo = tipo
        self.linea = linea
        self.columna = columna

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self))
        grafo.node(id, '(Inst)Declaracion')
        grafo.node(id+self.id,'Id '+ self.id)                
        grafo.edge(id,id+self.id)
        grafo.edge(padre, id) 
        if self.expresion is not None:
            self.expresion.graficar(id, grafo)          
    
    def ejecutar(self, entorno):                
        val_tmp = entorno.tabla.getSimbolo(self.id)
        if val_tmp is not None:
            # Asignacion porque el ID ya existe.
            nuevo_tipo = self.expresion.getTipo(entorno)
            if nuevo_tipo.compararTipo(val_tmp.tipo):         
                val_nuevo = self.expresion.getValor(entorno)
                val_tmp.valor = val_nuevo
            else:
                global_utils.registrySemanticError('Asignacion', 'Tipo incorrecto, se esperaba un valor de tipo ' +val_tmp.tipo.getNombre() + ' y se ha recibido un valor de tipo '+ nuevo_tipo.getNombre(), self.linea, self.columna)
            return 
        else:
            # Nueva variable
            if self.tipo is not None:                
                tipo_tmp = self.expresion.getTipo(entorno)
                if tipo_tmp is not None:
                    if not tipo_tmp.compararTipo(self.tipo):
                        global_utils.registrySemanticError('Declaracion',  self.id + '. Se esperaba un valor de tipo ' + self.tipo.getNombre() + ', se obtuvo un valor de tipo ' + tipo_tmp.getNombre(), self.linea, self.columna)
                        return
                    valor = self.expresion.getValor(entorno)
                    nuevo_simbolo = Simbolo(self.id, self.tipo, valor, self.linea, self.columna)            
                    entorno.tabla.registrarSimbolo(nuevo_simbolo)
                else:
                    global_utils.registrySemanticError('Declaracion', self.id + '. Se esperaba un valor de tipo ' + self.tipo.getNombre() + ' y no se ha obtenido valor. ', self.linea, self.columna) 
            else: 
                # O puede ser una asignación
                if isinstance(self.expresion, Llamada):
                    valor = self.expresion.getValor(entorno)
                    tipo = entorno.obtenerTipo(valor)                    
                    nuevo_simbolo = Simbolo(self.id, tipo, valor, self.linea, self.columna)            
                    entorno.tabla.registrarSimbolo(nuevo_simbolo)                      
                else:
                    tipo_tmp = self.expresion.getTipo(entorno)        
                    valor = self.expresion.getValor(entorno)
                    nuevo_simbolo = Simbolo(self.id, tipo_tmp, valor, self.linea, self.columna)            
                    entorno.tabla.registrarSimbolo(nuevo_simbolo)        

class If(Instruccion):
    def __init__(self, expresion, bloque, sino, linea, columna):
        self.expresion = expresion
        self.bloque = bloque 
        self.sino = sino
        self.linea = linea 
        self.columna = columna
        
    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self)) 
        grafo.node(id, 'if')
        grafo.edge(padre, id) 
        self.expresion.graficar(id, grafo)
        self.bloque.graficar(id,grafo)
        if self.sino is not None:
            self.sino.graficar(id,grafo)
        

    def ejecutar(self, entorno):
        #print('Ejecutando IF')
        tipo_tmp = self.expresion.getTipo(entorno)
        if tipo_tmp is None:
            global_utils.registrySemanticError('if', 'Valor inválido de la expresión condicional.', self.linea, self.columna) 
            return
        if tipo_tmp.esError():
            global_utils.registrySemanticError('if', 'Valor inválido de la expresión condicional.', self.linea, self.columna)             
            #global_utils.registrySemanticError('if', 'Tipo expresión condicional inválido. ' + tipo_tmp.getNombre() , self.linea, self.columna) 
            return 
        valor_condicion = self.expresion.getValor(entorno)
        if valor_condicion:
            val = self.bloque.ejecutar(entorno)
            if val is not None:
                if isinstance(val, Break):
                    return val
                if isinstance(val, Continue):
                    return val  
                return val                  
        else:
            if self.sino != None:
                val  = self.sino.ejecutar(entorno)
                if val is not None:
                    if isinstance(val, Break):
                        return val           
                    if isinstance(val, Continue):
                        return val  
                    return val                                          

class While(Instruccion):
    def __init__(self, expresion, bloque, linea, columna):
        self.expresion = expresion
        self.bloque = bloque         
        self.linea = linea 
        self.columna = columna  

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self))
        grafo.node(id, 'while')
        grafo.edge(padre, id) 
        self.expresion.graficar(id, grafo)
        self.bloque.graficar(id, grafo)
    
    def ejecutar(self, entorno):
        tipo_tmp = self.expresion.getTipo(entorno)
        if tipo_tmp is None:
            global_utils.registrySemanticError('while', 'Valor inválido de la expresión condicional.', self.linea, self.columna) 
            return  
        if tipo_tmp.esError():
            global_utils.registrySemanticError('while', 'Valor inválido de la expresión condicional.', self.linea, self.columna)
            return                   
        valor_condicion = self.expresion.getValor(entorno)
        while valor_condicion :
            ## ¿Nuevo entorno?            
            val = self.bloque.ejecutar(entorno)
            if val is not None:
                if isinstance(val, Break):
                    return 
                if isinstance(val, Continue):
                    valor_condicion = self.expresion.getValor(entorno)
                    continue
            valor_condicion = self.expresion.getValor(entorno)

class For(Instruccion):
    def __init__(self, id, expresion, bloque, linea, columna ):
        self.id = id
        self.expresion = expresion
        self.linea = linea
        self.columna = columna
        self.bloque = bloque

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self))   
        grafo.node(id, 'for')
        grafo.edge(padre, id)
        grafo.node(id+self.id,'[id] ' +self.id)
        grafo.edge(id,id+self.id) 
        self.expresion.graficar(id, grafo)
        self.bloque.graficar(id, grafo)             
    
    def ejecutar(self, entorno):
        if isinstance(self.expresion, Rango):
            tipo_tmp = self.expresion.getTipo(entorno)
            if not tipo_tmp.esError():
                rango = self.expresion.getValor(entorno)                
                entornoLocal = Entorno(entorno)
                #Creamos la variable temporal
                variable = Simbolo(self.id, Tipo(TipoPrimitivo.ENTERO),'',self.linea, self.columna)
                entornoLocal.insertSimbolo(variable)                
                for i in rango:
                    variable.valor = i
                    resultado_ejecucion = self.bloque.ejecutar(entornoLocal)
                    if resultado_ejecucion is not None:
                        if isinstance(resultado_ejecucion, Break):
                            return resultado_ejecucion
                        if isinstance(resultado_ejecucion, Continue):
                            return resultado_ejecucion                            
        else:
            tipo_tmp = self.expresion.getTipo(entorno)            
            if tipo_tmp is not None:
                #Cadena
                if tipo_tmp.esCadena():
                    valor = self.expresion.getValor(entorno) 
                    entornoLocal = Entorno(None)
                    #Creamos la variable temporal
                    variable = Simbolo(self.id, Tipo(TipoPrimitivo.STRING),'',self.linea, self.columna)
                    entornoLocal.insertSimbolo(variable)
                    for i in valor:
                            variable.valor = i
                            resultado_ejecucion = self.bloque.ejecutar(entornoLocal)
                            if resultado_ejecucion is not None:
                                if isinstance(resultado_ejecucion, Break):
                                    return resultado_ejecucion
                                if isinstance(resultado_ejecucion, Continue):
                                    return resultado_ejecucion
                #Arrelgo
                if tipo_tmp.esArreglo():
                    # Esto nos devuelve un arreglo
                    valor = self.expresion.getValor(entorno)                                                            
                    entornoLocal = Entorno(None)
                    #Creamos la variable temporal                                           
                    simbolo = Simbolo(self.id, None, None, self.linea, self.columna)
                    entornoLocal.insertSimbolo(simbolo)
                    for i in valor:       
                        tipo_tmp = i.tipo
                        if tipo_tmp is not None:
                            valor_tmp = i.valor
                            simbolo.valor = valor_tmp
                            simbolo.tipo = tipo_tmp                                                 
                            resultado_ejecucion = self.bloque.ejecutar(entornoLocal)
                            if resultado_ejecucion is not None:
                                if isinstance(resultado_ejecucion, Break):
                                    return resultado_ejecucion
                                if isinstance(resultado_ejecucion, Continue):
                                    return resultado_ejecucion                    
                        
class Break(Instruccion):
    def __init__(self, linea, columna):
        self.linea = linea;
        self.columna = columna;

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self))  
        grafo.node(id, 'break')     
        grafo.edge(padre, id)
    
    def ejecutar(self, entorno):
        return self

class Continue(Instruccion):
    def __init__(self, linea, columna):
        self.linea = linea;
        self.columna = columna;

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self))  
        grafo.node(id,'continue') 
        grafo.edge(padre, id)
              
    
    def ejecutar(self, entorno):
        return self

class Retorno(Instruccion):
    def __init__(self,expresion, linea, columna):
        self.expresion = expresion
        self.linea = linea;
        self.columna = columna;

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self))  
        grafo.node(id, 'retorno')
        grafo.edge(padre, id) 
        self.expresion.graficar(id, grafo)
              
    
    def ejecutar(self, entorno):
        if self.expresion is None:
            return self
        tipo_valor = self.expresion.getTipo(entorno)
        if tipo_valor is not None:
            if not tipo_valor.esError():
                valor_tmp = self.expresion.getValor(entorno)
                return valor_tmp
            else:
                global_utils.registrySemanticError('return', 'valor de retorno inválido. Verifique variables', self.linea, self.columna)            

class Funcion(Instruccion):
    def __init__(self, nombre, parametros_formales, instrucciones, linea, columna):
        self.id = nombre
        self.parametros_formales = parametros_formales
        self.instrucciones = instrucciones 
        self.linea = linea
        self.columna = columna 

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self))  
        grafo.node(id, '[Dec] Funcion [ID]' + self.id)      
        grafo.edge(padre, id)
        if self.parametros_formales is not None:
            for i in self.parametros_formales:
                i.graficar(id, grafo)
        if self.instrucciones is not None:
            self.instrucciones.graficar(id, grafo)


    def ejecutar(self, entorno):
        # Creamos el símbolo de tipo funcion
        nombre = self.id 
        if self.parametros_formales is not None:
            for i in self.parametros_formales:
                nombre = nombre +'$var'
        self.id = nombre
        funcion = FuncionSimbolo(self.id, self.parametros_formales, self.instrucciones, self.linea, self.columna)
        entorno.insertSimbolo(funcion)

## Expresion -----------------------------------------------------

class Suma(Expresion):
    def __init__(self, expresionI, expresionD, linea, columna):
        self.expresionI = expresionI
        self.expresionD = expresionD
        self.linea = linea
        self.columna = columna

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self))  
        grafo.node(id, 'suma')  
        grafo.edge(padre,id)
        self.expresionI.graficar(id,grafo)
        self.expresionD.graficar(id,grafo)
    
    def getTipo(self, entorno):
        tipoI = self.expresionI.getTipo(entorno)
        tipoD = self.expresionD.getTipo(entorno)
        if tipoI== None or tipoD == None:
            global_utils.registrySemanticError('+','Se ha recibido una variable no declarada.' , self.linea, self.columna)  
            return Tipo(TipoPrimitivo.ERROR) 

        if tipoI.esDinamico() or tipoD.esDinamico():
            return Tipo(TipoPrimitivo.DINAMICO)                      

        if(tipoI.esCadena() or tipoD.esCadena()):        
            global_utils.registrySemanticError('+',' No es posible realizar la operación ' + tipoI.getNombre() + " + " + tipoD.getNombre() , self.linea, self.columna)
            return Tipo(TipoPrimitivo.ERROR)
        if(tipoI.esFloat() or tipoD.esFloat()):
            return Tipo(TipoPrimitivo.FLOAT)
        return Tipo(TipoPrimitivo.ENTERO)
    
    def getValor(self, entorno):
        tipo_actual = self.getTipo(entorno)

        if tipo_actual.esError():
            return None

        valorI = self.expresionI.getValor(entorno)
        valorD = self.expresionD.getValor(entorno)

        if tipo_actual.esDinamico():
            tipoI = entorno.obtenerTipo(valorI)
            tipoD = entorno.obtenerTipo(valorD)

            if tipoI.esFloat() or tipoD.esFloat():
                self.valor = float(valorI) + float(valorD)
                return self.valor             
            if tipoI.esEntero() and tipoD.esEntero():
                self.valor = int(valorI) + int(valorD)
                return self.valor   
            global_utils.registrySemanticError('+',' No es posible realizar la operación ' + tipoI.getNombre() + " - " + tipoD.getNombre(), self.linea, self.columna)                           
            return None            

        if tipo_actual.esFloat():
            self.valor = float(valorI) + float(valorD)
            return self.valor
            
        if tipo_actual.esEntero():                        
            self.valor = int(valorI)+ int(valorD)
            return self.valor
        
        return None

class Concatenacion(Expresion):
    def __init__(self, expresionI, expresionD, linea, columna):
        self.expresionI = expresionI
        self.expresionD = expresionD
        self.linea = linea
        self.columna = columna

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self))  
        grafo.node(id, 'concatenacion')  
        grafo.edge(padre,id)
        self.expresionI.graficar(id,grafo)
        self.expresionD.graficar(id,grafo)              
    
    def getTipo(self, entorno):
        tipoI = self.expresionI.getTipo(entorno)
        tipoD = self.expresionD.getTipo(entorno)
        
        if tipoI == None or tipoD == None :
            global_utils.registrySemanticError('Concatenación','Error al realizar la conctaneación, se ha recibido una variable no declarada.' , self.linea, self.columna)
            return Tipo(TipoPrimitivo.ERROR)  

        if tipoI.esDinamico() or tipoD.esDinamico():
            return Tipo(TipoPrimitivo.STRING)                       

        if tipoI.esError() or tipoD.esError():
            return Tipo(TipoPrimitivo.ERROR)
        return Tipo(TipoPrimitivo.STRING)
    
    def getValor(self, entorno):
        cadena = ''
        tipo_tmp = self.getTipo(entorno)        
        if tipo_tmp.esError():
            return None
                
        valorI = self.expresionI.getValor(entorno)
        valorD = self.expresionD.getValor(entorno)                 
        cadena = self.recorrer(valorI, cadena)
        cadena = self.recorrer(valorD, cadena)
        return cadena
    
    def recorrer(self,valor, cadena):
        if isinstance(valor, str) or isinstance(valor, list ):
            for i in valor:
                if isinstance(i, Simbolo):
                    cadena = cadena + str(i.valor)
                elif isinstance(i,list):
                    self.recorrer(i, cadena)
                else:
                    cadena = cadena + str(i)
            return cadena
        else:
            return str(valor)

        
        

class Resta(Expresion):
    def __init__(self, expresionI, expresionD, linea, columna):
        self.expresionI = expresionI
        self.expresionD = expresionD
        self.linea = linea
        self.columna = columna

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self))  
        grafo.node(id, 'resta')  
        grafo.edge(padre,id)
        self.expresionI.graficar(id,grafo)
        self.expresionD.graficar(id,grafo)                
    
    def getTipo(self, entorno):
        tipoI = self.expresionI.getTipo(entorno)
        tipoD = self.expresionD.getTipo(entorno)

        if tipoI== None or tipoD == None:
            global_utils.registrySemanticError('-','Se ha recibido una variable no declarada.' , self.linea, self.columna)  
            return Tipo(TipoPrimitivo.ERROR) 

        if tipoI.esDinamico() or tipoD.esDinamico():
            return Tipo(TipoPrimitivo.DINAMICO)                    

        if (tipoI.esNumerico() and tipoD.esNumerico()):
            if (tipoI.esFloat() or tipoD.esFloat()):
                return Tipo(TipoPrimitivo.FLOAT)
            return Tipo(TipoPrimitivo.ENTERO)

        global_utils.registrySemanticError('-',' No es posible realizar la operación ' + tipoI.getNombre() + " - " + tipoD.getNombre(), self.linea, self.columna)
        return Tipo(TipoPrimitivo.ERROR)        
    
    def getValor(self, entorno):
        tipo_actual = self.getTipo(entorno)

        if tipo_actual.esError():
            return None

        valorI = self.expresionI.getValor(entorno)
        valorD = self.expresionD.getValor(entorno) 

        if tipo_actual.esDinamico():
            tipoI = entorno.obtenerTipo(valorI)
            tipoD = entorno.obtenerTipo(valorD)

            if tipoI.esFloat() or tipoD.esFloat():
                self.valor = float(valorI) - float(valorD)
                return self.valor             
            if tipoI.esEntero() and tipoD.esEntero():
                self.valor = int(valorI) - int(valorD)
                return self.valor   
            global_utils.registrySemanticError('-',' No es posible realizar la operación ' + tipoI.getNombre() + " - " + tipoD.getNombre(), self.linea, self.columna)                           
            return None
            
        if tipo_actual.esFloat():            
            self.valor = float(valorI) - float(valorD)
            return self.valor
            
        if tipo_actual.esEntero():                        
            self.valor = int(valorI) - int(valorD)
            return self.valor
        
        return None  


class Multiplicacion(Expresion):
    def __init__(self, expresionI, expresionD, linea, columna):
        self.expresionI = expresionI
        self.expresionD = expresionD
        self.linea = linea
        self.columna = columna

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self)) 
        grafo.node(id, 'multiplicacion')  
        grafo.edge(padre,id)
        self.expresionI.graficar(id,grafo)
        self.expresionD.graficar(id,grafo)                 
    
    def getTipo(self, entorno):
        tipoI = self.expresionI.getTipo(entorno)
        tipoD = self.expresionD.getTipo(entorno)
        
        if tipoI== None or tipoD == None:
            global_utils.registrySemanticError('*','Se ha recibido una variable no declarada.' , self.linea, self.columna)  
            return Tipo(TipoPrimitivo.ERROR)            

        if tipoI.esDinamico() or tipoD.esDinamico():
            return Tipo(TipoPrimitivo.DINAMICO)
        
        if(tipoI.esCadena() and tipoD.esCadena()):
            return Tipo(TipoPrimitivo.STRING)

        if (tipoI.esNumerico() and tipoD.esNumerico()):
            if (tipoI.esFloat() or tipoD.esFloat()):
                return Tipo(TipoPrimitivo.FLOAT)
            return Tipo(TipoPrimitivo.ENTERO)

        global_utils.registrySemanticError('*',' No es posible realizar la operación ' + tipoI.getNombre() + " * " + tipoD.getNombre() , self.linea, self.columna)
        return Tipo(TipoPrimitivo.ERROR)        
    
    def getValor(self, entorno):
        tipo_actual = self.getTipo(entorno)

        if tipo_actual.esError():
            return None
            
        valorI = self.expresionI.getValor(entorno)
        valorD = self.expresionD.getValor(entorno)            

        if tipo_actual.esDinamico():
            tipoI = entorno.obtenerTipo(valorI)
            tipoD = entorno.obtenerTipo(valorD)
            if tipoI.esCadena() or tipoD.esCadena():
                self.valor = str(valorI) + str(valorD)
                return self.valor
            if tipoI.esFloat() or tipoD.esFloat():
                self.valor = float(valorI) * float(valorD)
                return self.valor                
            if tipoI.esEntero() and tipoD.esEntero():
                self.valor = int(valorI) * int(valorD)
                return self.valor   
            global_utils.registrySemanticError('*',' No es posible realizar la operación ' + tipoI.getNombre() + " * " + tipoD.getNombre() , self.linea, self.columna)                             
            return None

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

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self))
        grafo.node(id, 'division')  
        grafo.edge(padre,id)
        self.expresionI.graficar(id,grafo)
        self.expresionD.graficar(id,grafo)                 
    
    def getTipo(self, entorno):
        tipoI = self.expresionI.getTipo(entorno)
        tipoD = self.expresionD.getTipo(entorno)

        if tipoI== None or tipoD == None:
            global_utils.registrySemanticError('/','Se ha recibido una variable no declarada.' , self.linea, self.columna)  
            return Tipo(TipoPrimitivo.ERROR)         

        if tipoI.esDinamico() or tipoD.esDinamico():
            return Tipo(TipoPrimitivo.DINAMICO)
                
        if (tipoI.esNumerico() and tipoD.esNumerico()):
            return Tipo(TipoPrimitivo.FLOAT)

        global_utils.registrySemanticError('/',' No es posible realizar la operación ' + tipoI.getNombre() + " / " + tipoD.getNombre() , self.linea, self.columna)
        return Tipo(TipoPrimitivo.ERROR)        
    
    def getValor(self, entorno):
        tipo_actual = self.getTipo(entorno)
        valorI = self.expresionI.getValor(entorno)
        valorD = self.expresionD.getValor(entorno)        

        if tipo_actual.esError():
            return None

        if tipo_actual.esDinamico():
            tipoI = entorno.obtenerTipo(valorI)
            tipoD = entorno.obtenerTipo(valorD)

            if tipoI.esFloat() or tipoD.esFloat():
                self.valor = float(valorI) / float(valorD)
                return self.valor     

            if tipoI.esEntero() and tipoD.esEntero():
                self.valor = int(valorI) / int(valorD)
                return self.valor  
            global_utils.registrySemanticError('/',' No es posible realizar la operación ' + tipoI.getNombre() + " / " + tipoD.getNombre() , self.linea, self.columna)                              
            return None            
            
        if tipo_actual.esFloat():
            self.valor = float(valorI) / float(valorD)
            return self.valor
            
        if tipo_actual.esEntero():            
            self.valor = int(valorI) / int(valorD)
            return self.valor
        
        return None  

class Potencia(Expresion):
    def __init__(self, expresionI, expresionD, linea, columna):
        self.expresionI = expresionI
        self.expresionD = expresionD
        self.linea = linea
        self.columna = columna

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self)) 
        grafo.node(id, 'potencia')  
        grafo.edge(padre,id)
        self.expresionI.graficar(id,grafo)
        self.expresionD.graficar(id,grafo)                
    
    def getTipo(self, entorno):
        tipoI = self.expresionI.getTipo(entorno)
        tipoD = self.expresionD.getTipo(entorno)

        if tipoI== None or tipoD == None:
            global_utils.registrySemanticError('^','Se ha recibido una variable no declarada.' , self.linea, self.columna)  
            return Tipo(TipoPrimitivo.ERROR)    

        if tipoI.esDinamico() or tipoD.esDinamico():
            return Tipo(TipoPrimitivo.DINAMICO)                 

        if (tipoI.esNumerico() and tipoD.esNumerico()):
            if(tipoI.esFloat() or tipoD.esFloat()):
                return Tipo(TipoPrimitivo.FLOAT)
            else:
                return Tipo(TipoPrimitivo.ENTERO)

        if (tipoI.esCadena() and tipoD.esEntero()):
            return Tipo(TipoPrimitivo.STRING)

        global_utils.registrySemanticError('^',' No es posible realizar la operación ' + tipoI.getNombre() + " ^ " + tipoD.getNombre() , self.linea, self.columna)
        return Tipo(TipoPrimitivo.ERROR)        
    
    def getValor(self, entorno):
        tipo_actual = self.getTipo(entorno)
        valorI = self.expresionI.getValor(entorno)
        valorD = self.expresionD.getValor(entorno)
        if tipo_actual.esError():
            return None

        if tipo_actual.esDinamico():
            tipoI = entorno.obtenerTipo(valorI)
            tipoD = entorno.obtenerTipo(valorD)

            if tipoI.esFloat() or tipoD.esFloat():
                self.valor = float(pow(valorI, valorD))
                return self.valor     

            if tipoI.esEntero() and tipoD.esEntero():
                self.valor = int(pow(valorI,valorD))
                return self.valor                
            
            if tipoI.esCadena() and tipoD.esEntero():
                self.valor = '' 
                contador = 0 
                while ( contador < valorD):
                    self.valor = self.valor + str(valorI)
                    contador = contador + 1
                return self.valor                
            global_utils.registrySemanticError('^',' No es posible realizar la operación ' + tipoI.getNombre() + " ^ " + tipoD.getNombre() , self.linea, self.columna)
            return None        
            
        if tipo_actual.esFloat():
            self.valor = float(pow(valorI, valorD))
            return self.valor
            
        if tipo_actual.esEntero():            
            self.valor = int(pow(valorI,valorD))
            return self.valor

        if tipo_actual.esCadena():
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

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self))  
        grafo.node(id, 'modulo')  
        grafo.edge(padre,id)
        self.expresionI.graficar(id,grafo)
        self.expresionD.graficar(id,grafo)              
    
    def getTipo(self, entorno):
        tipoI = self.expresionI.getTipo(entorno)
        tipoD = self.expresionD.getTipo(entorno)

        if tipoI== None or tipoD == None:
            global_utils.registrySemanticError('%','Se ha recibido una variable no declarada.' , self.linea, self.columna)  
            return Tipo(TipoPrimitivo.ERROR) 

        if tipoI.esDinamico() or tipoD.esDinamico():
            return Tipo(TipoPrimitivo.DINAMICO)               

        if (tipoI.esNumerico() and tipoD.esNumerico()):
            if (tipoI.esFloat() or tipoD.esFloat()):
                return Tipo(TipoPrimitivo.FLOAT)
            return Tipo(TipoPrimitivo.ENTERO)

        global_utils.registrySemanticError('%',' No es posible realizar la operación ' + tipoI.getNombre() + " % " + tipoD.getNombre() , self.linea, self.columna)
        return Tipo(TipoPrimitivo.ERROR)        
    
    def getValor(self, entorno):
        tipo_actual = self.getTipo(entorno)

        if tipo_actual.esError():
            return None
            
        valorI = self.expresionI.getValor(entorno)
        valorD = self.expresionD.getValor(entorno)


        if tipo_actual.esDinamico():
            tipoI = entorno.obtenerTipo(valorI)
            tipoD = entorno.obtenerTipo(valorD)

            if tipoI.esFloat() or tipoD.esFloat():
                self.valor = float(valorI) % float(valorD)
                return self.valor     

            if tipoI.esEntero() and tipoD.esEntero():
                self.valor = int(valorI) % int(valorD)
                return self.valor  
            global_utils.registrySemanticError('%',' No es posible realizar la operación ' + tipoI.getNombre() + " % " + tipoD.getNombre() , self.linea, self.columna)                                                                  
            return None          

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

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self))  
        grafo.node(id, 'negativo')  
        grafo.edge(padre,id)
        self.expresion.graficar(id,grafo)                       
    
    def getTipo(self, entorno):
        tipo = self.expresion.getTipo(entorno)  

        if tipo== None:
            global_utils.registrySemanticError('-','Se ha recibido una variable no declarada.' , self.linea, self.columna)  
            return Tipo(TipoPrimitivo.ERROR)   
            
        if tipo.esDinamico():
            return tipo               

        if tipo.esNumerico():
            if tipo.esFloat():
                return Tipo(TipoPrimitivo.FLOAT)
            return Tipo(TipoPrimitivo.ENTERO)

        global_utils.registrySemanticError('-',' No es posible realizar la operación (-) ' + tipo.getNombre() , self.linea, self.columna)
        return Tipo(TipoPrimitivo.ERROR)        
    
    def getValor(self, entorno):
        tipo_actual = self.getTipo(entorno)

        if tipo_actual.esError():
            return None
        
        if tipo_actual.esDinamico():
            valor = self.expresion.getValor(entorno)
            tipo_real = entorno.obtenerTipo(valor)    
            if tipo_real.esFloat():                        
                self.valor = float(valor) * -1 
                return self.valor
                
            if tipo_real.esEntero():                                            
                self.valor = int(valor) * -1 
                return self.valor   
            global_utils.registrySemanticError('-',' No es posible realizar la operación (-) ' + tipo_real.getNombre() , self.linea, self.columna)
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

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self))
        grafo.node(id, '[Exp] Nulo')  
        grafo.edge(padre,id)                        
    
    def getValor(self, entorno):
        return self.valor
    
    def getTipo(self, entorno):
        return self.tipo

class Variable(Expresion):
    def __init__(self, id, linea, columna):
        self.id = id 
        self.linea = linea 
        self.columna = columna

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self)) 
        grafo.node(id, '[Exp] Variable' + self.id)  
        grafo.edge(padre,id)                 
    
    def getTipo(self, entorno):
        tmp_simbolo = entorno.getSimbolo(self.id)
        if tmp_simbolo is None:
            global_utils.registrySemanticError(self.id,'No se ha encontrado la variable solicitada ' +self.id , self.linea, self.columna)
            return None
        return tmp_simbolo.tipo

    def getValor(self, entorno):
        tmp_simbolo = entorno.getSimbolo(self.id)
        if tmp_simbolo is None:
            global_utils.registrySemanticError(self.id,'No se ha encontrado la variable solicitada ' +self.id , self.linea, self.columna)
            return None
        return tmp_simbolo.valor

class Entero(Expresion):
    def __init__(self, valor, linea, columna):
        self.valor = valor
        self.linea = linea
        self.columna = columna
        self.tipo = Tipo(TipoPrimitivo.ENTERO,'')

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self))  
        grafo.node(id, '[Exp] Entero' + str(self.valor))  
        grafo.edge(padre,id)                
    
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
    

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self))
        grafo.node(id, '[Exp] Float' + str(self.valor))  
        grafo.edge(padre,id)         

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
        
    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self)) 
        grafo.node(id, '[Exp] Bool' + str(self.valor))  
        grafo.edge(padre,id)                   
    
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

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self)) 
        grafo.node(id, '[Exp] Char' + str(self.valor))  
        grafo.edge(padre,id)                     
    
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

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self))
        grafo.node(id, '[Exp] String' + str(self.valor))  
        grafo.edge(padre,id)                    
    
    def getValor(self, entorno):
        return self.valor
    
    def getTipo(self, entorno):
        return self.tipo        

class Uppercase(Expresion):
    def __init__(self, expresion, linea, columna):
        self.expresion = expresion
        self.linea = linea
        self.columna = columna

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self))  
        grafo.node(id, 'uppercase')  
        grafo.edge(padre,id)      
        self.expresion.graficar(id, grafo)          
    
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

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self)) 
        grafo.node(id, 'lowercase')  
        grafo.edge(padre,id)      
        self.expresion.graficar(id, grafo)                  
    
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

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self))   
        grafo.node(id, 'log10')  
        grafo.edge(padre,id)      
        self.expresion.graficar(id, grafo)              
    
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

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self))  
        grafo.node(id, 'log')  
        grafo.edge(padre,id)      
        self.expresion.graficar(id, grafo)              
    
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

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self))        
                
class Sin(Expresion):
    def __init__(self, expresion, linea, columna):
        self.expresion = expresion        
        self.linea = linea
        self.columan = columna

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self))
        grafo.node(id, 'sin')  
        grafo.edge(padre,id)      
        self.expresion.graficar(id, grafo)                 
    
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

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self)) 
        grafo.node(id, 'cos')  
        grafo.edge(padre,id)      
        self.expresion.graficar(id, grafo)                 
    
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

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self)) 
        grafo.node(id, 'tan')  
        grafo.edge(padre,id)      
        self.expresion.graficar(id, grafo)               
    
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

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self))
        grafo.node(id, 'sqrt')  
        grafo.edge(padre,id)      
        self.expresion.graficar(id, grafo)                
    
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

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self))  
        grafo.node(id, 'mayor')  
        grafo.edge(padre,id)      
        self.expresionI.graficar(id, grafo)               
        self.expresionD.graficar(id, grafo) 
    
    def getTipo(self, entorno):
        tipoI = self.expresionI.getTipo(entorno)
        tipoD = self.expresionI.getTipo(entorno)
        if tipoI.esNumerico() and tipoD.esNumerico():
            return Tipo(TipoPrimitivo.BOOL)
        if tipoI.esCadena() and tipoD.esCadena():
            return Tipo(TipoPrimitivo.BOOL)
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
        if tipo_tmp.esBool():
            self.valor = valorI > valorD
            return self.valor               

class MayorIgual(Expresion):
    def __init__(self, expresionI, expresionD, linea, columna):
        self.expresionI = expresionI
        self.expresionD = expresionD
        self.linea = linea
        self.columna = columna

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self)) 
        grafo.node(id, 'mayor-igual')  
        grafo.edge(padre,id)      
        self.expresionI.graficar(id, grafo)               
        self.expresionD.graficar(id, grafo)                
    
    def getTipo(self, entorno):
        tipoI = self.expresionI.getTipo(entorno)
        tipoD = self.expresionI.getTipo(entorno)
        if tipoI.esNumerico() and tipoD.esNumerico():
            return Tipo(TipoPrimitivo.BOOL)
        if tipoI.esCadena() and tipoD.esCadena():
            return Tipo(TipoPrimitivo.BOOL)
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
        if tipo_tmp.esBool():
            self.valor = valorI >= valorD
            return self.valor                          

class Menor(Expresion):
    def __init__(self, expresionI, expresionD, linea, columna):
        self.expresionI = expresionI
        self.expresionD = expresionD
        self.linea = linea
        self.columna = columna

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self)) 
        grafo.node(id, 'menor')  
        grafo.edge(padre,id)      
        self.expresionI.graficar(id, grafo)               
        self.expresionD.graficar(id, grafo)                
    
    def getTipo(self, entorno):
        tipoI = self.expresionI.getTipo(entorno)
        tipoD = self.expresionI.getTipo(entorno)
        if tipoI.esNumerico() and tipoD.esNumerico():
            return Tipo(TipoPrimitivo.BOOL)
        if tipoI.esCadena() and tipoD.esCadena():
            return Tipo(TipoPrimitivo.BOOL)
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
        if tipo_tmp.esBool():
            self.valor = valorI < valorD
            return self.valor              


class MenorIgual(Expresion):
    def __init__(self, expresionI, expresionD, linea, columna):
        self.expresionI = expresionI
        self.expresionD = expresionD
        self.linea = linea
        self.columna = columna

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self)) 
        grafo.node(id, 'menor-igual')  
        grafo.edge(padre,id)      
        self.expresionI.graficar(id, grafo)               
        self.expresionD.graficar(id, grafo)                
    
    def getTipo(self, entorno):
        tipoI = self.expresionI.getTipo(entorno)
        tipoD = self.expresionI.getTipo(entorno)
        if tipoI.esNumerico() and tipoD.esNumerico():
            return Tipo(TipoPrimitivo.BOOL)
        if tipoI.esCadena() and tipoD.esCadena():
            return Tipo(TipoPrimitivo.BOOL)            
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
        if tipo_tmp.esBool():
            self.valor = valorI <= valorD
            return self.valor               

class Igualigual(Expresion):
    def __init__(self, expresionI, expresionD, linea, columna):
        self.expresionI = expresionI
        self.expresionD = expresionD
        self.linea = linea
        self.columna = columna

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self)) 
        grafo.node(id, 'igual')  
        grafo.edge(padre,id)      
        self.expresionI.graficar(id, grafo)               
        self.expresionD.graficar(id, grafo)                
    
    def getTipo(self, entorno):
        tipoI = self.expresionI.getTipo(entorno)
        tipoD = self.expresionI.getTipo(entorno)
        if tipoI == None or tipoD == None:
            return Tipo(TipoPrimitivo.ERROR)    
        if tipoI.esNumerico() and tipoD.esNumerico():
            return Tipo(TipoPrimitivo.BOOL)
        if tipoI.esCadena() and tipoD.esCadena():
            return Tipo(TipoPrimitivo.BOOL)
        if tipoI.compararTipo(tipoD):
            return Tipo(TipoPrimitivo.BOOL)
        global_utils.registrySemanticError('==','No es posible realizar la operación ' + tipoI.getNombre() + ' == '+ tipoD.getNombre() , self.linea, self.columna)
        return Tipo(TipoPrimitivo.ERROR)

    def getValor(self, entorno):
        tipo_tmp = self.getTipo(entorno)
        if tipo_tmp.esError():
            return None
        valorI = self.expresionI.getValor(entorno)
        valorD = self.expresionD.getValor(entorno)
        if tipo_tmp.esNumerico():        
            self.valor = valorI == valorD
            return self.valor
        if tipo_tmp.esCadena():
            self.valor = str(valorI) == str(valorD)
            return self.valor 
        if tipo_tmp.esBool():
            self.valor = valorI == valorD
            return self.valor            
        return False 


class Diferente(Expresion):
    def __init__(self, expresionI, expresionD, linea, columna):
        self.expresionI = expresionI
        self.expresionD = expresionD
        self.linea = linea
        self.columna = columna

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self))  
        grafo.node(id, 'diferente')  
        grafo.edge(padre,id)      
        self.expresionI.graficar(id, grafo)               
        self.expresionD.graficar(id, grafo)              
    
    def getTipo(self, entorno):
        tipoI = self.expresionI.getTipo(entorno)
        tipoD = self.expresionI.getTipo(entorno)
        if tipoI.esNumerico() and tipoD.esNumerico():
            return Tipo(TipoPrimitivo.BOOL)
        if tipoI.esCadena() and tipoD.esCadena():
            return Tipo(TipoPrimitivo.BOOL)
        if tipoI.compararTipo(tipoD):
            return Tipo(TipoPrimitivo.BOOL)            
        global_utils.registrySemanticError('!=','No es posible realizar la operación ' + tipoI.getNombre() + ' != '+ tipoD.getNombre() , self.linea, self.columna)
        return Tipo(TipoPrimitivo.ERROR)

    def getValor(self, entorno):
        tipo_tmp = self.getTipo(entorno)
        if tipo_tmp.esError():
            return None
        valorI = self.expresionI.getValor(entorno)
        valorD = self.expresionD.getValor(entorno)
        if tipo_tmp.esNumerico():        
            self.valor = valorI != valorD
            return self.valor
        if tipo_tmp.esCadena():
            self.valor = str(valorI) != str(valorD)
            return self.valor 
        if tipo_tmp.esBool():
            self.valor = valorI != valorD
            return self.valor                
        return False            

class Or(Expresion):
    def __init__(self, expresionI, expresionD, linea, columna):
        self.expresionI = expresionI 
        self.expresionD = expresionD
        self.linea = linea
        self.columna = columna

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self))  
        grafo.node(id, 'OR')  
        grafo.edge(padre,id)      
        self.expresionI.graficar(id, grafo)               
        self.expresionD.graficar(id, grafo)              
    
    def getTipo(self, entorno):
        tipoI = self.expresionI.getTipo(entorno)
        tipoD = self.expresionD.getTipo(entorno)
        if tipoI.esBool() and tipoD.esBool():
            return Tipo(TipoPrimitivo.BOOL)
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

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self)) 
        grafo.node(id, 'AND')  
        grafo.edge(padre,id)      
        self.expresionI.graficar(id, grafo)               
        self.expresionD.graficar(id, grafo)             
    
    def getTipo(self, entorno):
        tipoI = self.expresionI.getTipo(entorno)
        tipoD = self.expresionD.getTipo(entorno)
        if tipoI.esBool() and tipoD.esBool():
            return Tipo(TipoPrimitivo.BOOL)
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

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self)) 
        grafo.node(id, 'NOT')  
        grafo.edge(padre,id)      
        self.expresion.graficar(id, grafo)        
    
    def getTipo(self, entorno):
        tipo = self.expresion.getTipo(entorno)
        if tipo.esBool():
            return Tipo(TipoPrimitivo.BOOL)
        return Tipo(TipoPrimitivo.ERROR)
    
    def getValor(self, entorno):
        tipo_tmp = self.getTipo(entorno)
        if tipo_tmp.esBool():
            valor = self.expresion.getValor(entorno)
            self.valor = not valor
            return self.valor
        return None

class Rango(Expresion):
    def __init__(self, expresionInicio, expresionFinal, linea, columna):
        self.expresionInicio = expresionInicio
        self.expresionFinal = expresionFinal
        self.linea = linea
        self.columna = columna

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self)) 
        grafo.node(id, 'rango')  
        grafo.edge(padre,id)      
        self.expresionInicio.graficar(id, grafo)               
        self.expresionFinal.graficar(id, grafo)               
    
    def getTipo(self, entorno):
        tipoI = self.expresionInicio.getTipo(entorno)
        tipoD = self.expresionFinal.getTipo(entorno)

        if (tipoI is None) or (tipoD is None):
            global_utils.registrySemanticError('rango for','Variable no definida.' , self.linea, self.columna)
            return Tipo(TipoPrimitivo.ERROR)

        if tipoI.esNumerico() and tipoD.esNumerico():
            return Tipo(TipoPrimitivo.ENTERO)
        global_utils.registrySemanticError('rango for','Valor inválido para rangos en ciclo for' , self.linea, self.columna)
        return Tipo(TipoPrimitivo.ERROR)
    
    def getValor(self, entorno):
        tipo = self.getTipo(entorno)
        if not tipo.esError():
            valorI = self.expresionInicio.getValor(entorno)
            valorD = self.expresionFinal.getValor(entorno)
            return range(int(valorI), int(valorD)+1)

class Arreglo(Expresion):
    def __init__(self, lista_expresiones, linea, columna):
        self.lista = lista_expresiones
        self.linea = linea
        self.columna = columna

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self)) 
        grafo.node(id, 'arreglo')  
        grafo.edge(padre,id)   
        for exp in self.lista:   
            exp.graficar(id, grafo)        
    
    def getTipo(self, entorno):
        return Tipo(TipoPrimitivo.ARREGLO)
    
    def getValor(self, entorno):
        arreglo_simbolos = []
        for exp in self.lista:
            tipo_actual = exp.getTipo(entorno)
            if tipo_actual is None:
                global_utils.registrySemanticError('elemento arreglo','Valor inválido, variable no declarada.' , self.linea, self.columna)
            elif tipo_actual.esError():
                global_utils.registrySemanticError('elemento arreglo','Valor inválido, variable no declarada.' , self.linea, self.columna)
            else:
                valor = exp.getValor(entorno)
                simbolo = Simbolo('', tipo_actual, valor, self.linea, self.columna)
                arreglo_simbolos.append(simbolo)
        return arreglo_simbolos

class Ternario(Expresion):
    def __init__(self, condicion , expV, expF , linea, columna):
        self.condicion = condicion
        self.expV = expV 
        self.expF = expF 
        self.linea = linea 
        self.columna = columna 

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self)) 
        grafo.node(id, 'ternario')  
        grafo.edge(padre,id)    
        self.condicion.graficar(id, grafo)
        self.expV.graficar(id, grafo)
        self.expF.graficar(id, grafo)

    def getTipo(self, entorno):
        tipo_valor = self.condicion.getTipo(entorno)
        if tipo_valor is None:
           global_utils.registrySemanticError('Ternario','Valor erroneo condición.' , self.linea, self.columna) 
           return Tipo(TipoPrimitivo.ERROR)
        if not tipo_valor.esBool():
           global_utils.registrySemanticError('Ternario','Valor erroneo condición.' , self.linea, self.columna) 
           return Tipo(TipoPrimitivo.ERROR)        
        valor = self.condicion.getValor(entorno)
        if valor:
            return self.expV.getTipo(entorno)
        else:
            return self.expF.getTipo(entorno)

    def getValor(self, entorno):
        tipo_valor = self.condicion.getTipo(entorno)
        if tipo_valor is None:
           global_utils.registrySemanticError('Ternario','Valor erroneo condición.' , self.linea, self.columna) 
           return Tipo(TipoPrimitivo.ERROR)
        if not tipo_valor.esBool():
           global_utils.registrySemanticError('Ternario','Valor erroneo condición.' , self.linea, self.columna) 
           return Tipo(TipoPrimitivo.ERROR)        
        valor = self.condicion.getValor(entorno)
        if valor:
            return self.expV.getValor(entorno)
        else:
            return self.expF.getValor(entorno)      

class Llamada(Expresion):
    def __init__(self, id, parametros_actuales, linea, columna):
        self.id = id
        self.parametros = parametros_actuales 
        self.linea = linea
        self.columna = columna

    def graficar(self, padre, grafo):
        id = 'Nodo'+ str(hash(self)) 
        grafo.node(id, 'llamada [ID] ' +self.id)  
        grafo.edge(padre,id)
        if self.parametros is not None:
            for i in self.parametros:
                i.graficar(id, grafo)



    def getTipo(self, entorno):
        return Tipo(TipoPrimitivo.DINAMICO)
    
    def getValor(self, entorno):
        nuevoEntorno = Entorno(entorno)
        #Creamos las nuevas variables. 
        nombre_funcion_buscada = self.id 
        if self.parametros is not None:
            for i in self.parametros:
                nombre_funcion_buscada = nombre_funcion_buscada +'$var'
        #buscamos la funcion
        funcion_a_llamar = entorno.getSimbolo(nombre_funcion_buscada)
        if funcion_a_llamar is not None:
            if funcion_a_llamar.parametros is  not None:
                indice = 0
                for param in funcion_a_llamar.parametros:
                    #Pasamos los valores de los parametros actuales 
                    tipo_tmp = self.parametros[indice].getTipo(entorno)
                    if tipo_tmp is None:
                        global_utils.registrySemanticError('Llamada','Parámetro ' + str(indice) + ' erroneo.', self.linea, self.columna) 
                        return 
                    elif not tipo_tmp.esError():
                        valor_tmp = self.parametros[indice].getValor(entorno)
                        simbolo = Simbolo(param.id, tipo_tmp, valor_tmp, self.linea, self.columna)
                        nuevoEntorno.insertSimbolo(simbolo)                    
                    indice +=1
            valor = funcion_a_llamar.instrucciones.ejecutar(nuevoEntorno) 
            return valor
        else:
            global_utils.registrySemanticError('llamada','función ' +self.id + ' no declarada.' , self.linea, self.columna) 
        
    

    


