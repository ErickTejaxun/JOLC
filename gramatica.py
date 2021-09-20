# --------------------
# Erick Tejaxún
# USAC 2021
# --------------------
from singlenton import global_utils
linea = 0 
columa = 0
input_ANY_init = ''
string_cadena_impresion = '' 
bandera_estado_cadena = 0
final_cadena = False

#Estados 
states = (
    ('cadena', 'exclusive'),
    ('impresion', 'exclusive'),
    ('expresion', 'exclusive')
)


# tokens definition
tokens = (
    'PARIZQ',
    'PARDER',
    'MAS',
    'MENOS',
    'POR',
    'DIV',
    'POW',
    'MODULO',
    'AND',
    'OR',
    'NOT',
    'IGIG',
    'DIFDE',
    'MAY',
    'MEN',
    'MAYIG',
    'MENIG',
    'IGUAL',
    'DPUNTOS',
    #-------PRIMITIVAS
    'NULO',
    'FLOAT',
    'ENTERO',
    'RTRUE',
    'RFALSE',
    'CHAR',
    'STRING',
    'IMPRIMIR',
    'IMPRIMIRLN',
    'UPPERCASE',
    'LOWERCASE',
    'LOG10',
    'LOG',  
    'SIN',
    'COS',
    'TAN',
    'SQRT',
    #----------->
    'PUNTOCOMA',
    'COMA',
    'COMILLA',
    'DOLAR',
    #...........>
    'ID',
    #----Tipos
    'TINT64',
    'TFLOAT64',
    'TBOOL',
    'TCHAR',
    'TSTRING'

)

#tipos primitivos
#t_INITIAL_TINT64 = r'Int64'
#t_INITIAL_TFLOAT64 = r'Float64'
#t_INITIAL_TBOOL = r'Bool'
#t_INITIAL_TCHAR = r'Char'
#t_INITIAL_TSTRING = r'String'
t_ANY_PUNTOCOMA=r';'
t_ANY_COMA=r','
t_INITIAL_cadena_impresion_PARIZQ = r'\('
t_INITIAL_cadena_impresion_PARDER = r'\)'
t_ANY_MAS = r'\+'
t_ANY_MENOS = r'-'
t_ANY_POR = r'\*'
t_ANY_DIV = r'/'
t_ANY_AND = r'&&'
t_ANY_OR = r'\|\|'
t_ANY_NOT = r'!'
t_INITIAL_IGUAL = r'='
t_ANY_IGIG = r'=='
t_ANY_DIFDE = r'!='
t_ANY_MENIG = r'<='
t_ANY_MAYIG = r'>='
t_ANY_MAY = r'>'
t_ANY_MEN = r'<'
t_ANY_POW = r'\^'
t_ANY_MODULO = r'%'
t_ANY_UPPERCASE = r'uppercase'
t_ANY_LOWERCASE = r'lowercase'
t_ANY_LOG = r'log'
t_ANY_LOG10 = r'log10'
t_ANY_SIN = r'sin'
t_ANY_COS = r'cos'
t_ANY_TAN = r'tan'
t_ANY_SQRT= r'sqrt'
t_INITIAL_DPUNTOS = r'::'



# ignored characters, tab and space
t_INITIAL_impresion_ignore = " \t"

def t_ANY_comment(t):
     r'(\#=(.|\n)*?=\#)|(\#.*)'
     saltos = str(t.value).count('\n')
     if saltos > 0 :
        t.lexer.lineno += saltos
     #print(t.value)     
     pass

def t_INITIAL_TINT64(t):
    r'Int64'
    return t

def t_INITIAL_TFLOAT64(t):
    r'Float64'
    return t 

def t_INITIAL_TBOOL(t):
    r'Bool'
    return t

def t_INITIAL_TCHAR(t):
    r'Char'
    return t

def t_INITIAL_TSTRING(t):
    r'String'
    return t

def t_INITIAL_IMPRIMIRLN(t):
    r'println'
    global final_cadena 
    final_cadena = False    
    t.lexer.begin('impresion')
    return t    

def t_INITIAL_IMPRIMIR(t):
    r'print'
    global final_cadena 
    final_cadena = False
    t.lexer.begin('impresion')
    return t

def t_INITIAL_expresion_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     #t.type = reserved.get(t.value,'ID')    # Check for reserved words
     return t

def t_impresion_PARDER(t):
    r'\)'
    t.lexer.begin('INITIAL')
    return t 

def t_ANY_CHAR(t):
    r'\'([^\\\n]|(\\.))*?\''
    string = str(t.value)
    if len(string) == 2 :
        t.value = ''
    else:
        t.value = string[1]
    return t

def t_INITIAL_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t

def t_impresion_STRING(t):
    r'\"'
    global string_cadena_impresion
    global final_cadena     
    if final_cadena == False:
        string_cadena_impresion  = ''        
        final_cadena = True          
        t.lexer.begin('cadena') 
        pass
    else:
        t.value = string_cadena_impresion
        t.lexer.begin('INITIAL')
        final_cadena = False
        return t        

def t_cadena_STRING(t):
    r'\"'     
    global final_cadena 
    if final_cadena is True :
        t.value = string_cadena_impresion
        t.lexer.begin('INITIAL')
        final_cadena = False
        return t
    t.value = string_cadena_impresion    
    t.lexer.begin('impresion')
    pass

def t_cadena_DOLAR(t):
    r'\$'  
    global final_cadena 
    global string_cadena_impresion
    #final_cadena = True        
    t.value = string_cadena_impresion
    t.lexer.begin('expresion')        
    string_cadena_impresion  = '' 
    return t     

def t_cadena_COMILLA(t):
    r'.'
    if t.value == '\n':
        t.lexer.lineno += 1            
    global string_cadena_impresion
    string_cadena_impresion = string_cadena_impresion + str(t.value)    
    pass

contador_parentesis = 0
def t_expresion_PARIZQ(t):
    r'\('
    global contador_parentesis
    contador_parentesis += 1
    return t

def t_expresion_PARDER(t):
    r'\)'
    global contador_parentesis
    contador_parentesis -= 1
    if contador_parentesis == 0:
        t.lexer.begin('cadena')
    return t


def t_ANY_NULO(t):
    r'nothing'    
    return t

def t_ANY_FLOAT(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        # log error         
        t.value = 0
    return t

def t_ANY_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        # log error         
        #print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ANY_RTRUE(t):
    r'true'
    t.value = True    
    return t

def t_ANY_RFALSE(t):
    r'false'
    t.value = False    
    return t
    

def t_ANY_line(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_ANY_error(t):        
    global_utils.registryLexicalError(t.value[0],'Caracter ilegal.', t.lexer.lineno, find_column(t))
    t.lexer.skip(1)



def find_column(token):
    global input_ANY_init
    line_start = input_ANY_init.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1



# Building scanner.
import ply.lex as lex
lexer = lex.lex()
import AST as AST


# Precedence and asociation
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'IGIG', 'DIFDE'),
    ('nonassoc', 'MEN', 'MAY'),
    ('left','MAS','MENOS'),
    ('left','POR','DIV'),
    ('right', 'UMINUS'),
    ('left','PARIZQ', 'PARDER'),    
    )

def p_raiz(t):
    '''root : lista_instrucciones'''          
    t[0] = t[1]

def p_raiz_2(t):
    '''root :  empty '''
    t[0] = None

def p_empty(t):
    'empty :'
    pass

def p_lista_instrucciones_1(t):
    '''lista_instrucciones : lista_instrucciones imprimir'''    
    t[1].agregarInstruccion(t[2])
    t[0] = t[1]

def p_lista_instrucciones_2(t):
    '''lista_instrucciones : lista_instrucciones imprimirln'''    
    t[1].agregarInstruccion(t[2])
    t[0] = t[1]

def p_lista_instrucciones_3(t):
    '''lista_instrucciones : lista_instrucciones declaracion'''
    t[1].agregarInstruccion(t[2])
    t[0] = t[1]

def p_lista_instrucciones_imprimir(t):
    '''lista_instrucciones : imprimir'''
    t[0] = AST.Bloque(t.lineno(1), 0)
    t[0].agregarInstruccion(t[1])

def p_lista_instrucciones_imprimirln(t):
    '''lista_instrucciones : imprimirln'''
    t[0] = AST.Bloque(t.lineno(1), 0)
    t[0].agregarInstruccion(t[1])

def p_lista_instrucciones_declaracion(t):
    '''lista_instrucciones : declaracion'''
    t[0] = AST.Bloque(t.lineno(1), 0)
    t[0].agregarInstruccion(t[1])

def p_instruccion_declaracion(t):
    ''' declaracion : ID IGUAL e DPUNTOS tipo PUNTOCOMA'''
    t[0] = AST.Declaracion(t[1], t[3], t[5], t.lineno(1), 0)

def p_instruccion_declaracion_sintipo(t):
    ''' declaracion : ID IGUAL e PUNTOCOMA'''
    t[0] = AST.Declaracion(t[1], t[3], None, t.lineno(1), 0)    

def p_tipo_int64(t):
    ''' tipo : TINT64'''
    t[0] = AST.Tipo(AST.TipoPrimitivo.ENTERO)

def p_tipo_float64(t):
    ''' tipo : TFLOAT64 '''
    t[0] = AST.Tipo(AST.TipoPrimitivo.FLOAT)

def p_tipo_bool(t):
    ''' tipo : TBOOL ''' 
    t[0] = AST.Tipo(AST.TipoPrimitivo.BOOL)

def p_tipo_char(t):
    ''' tipo : TCHAR ''' 
    t[0] = AST.Tipo(AST.TipoPrimitivo.CHAR)

def p_tipo_string(t):
    ''' tipo : TSTRING ''' 
    t[0] = AST.Tipo(AST.TipoPrimitivo.STRING)

def p_instruccion_imprimirln(t):
    '''imprimirln : IMPRIMIRLN PARIZQ lista_e PARDER PUNTOCOMA '''
    t[0]= AST.ImprimirLn(t[3], t.lineno(1), 0)

def p_instruccion_imprimir(t):
    '''imprimir : IMPRIMIR PARIZQ lista_e PARDER PUNTOCOMA '''
    t[0]= AST.Imprimir(t[3], t.lineno(1), 0)

def p_imprimir_operacion(t):
    ''' imprimir_operacion : DOLAR PARIZQ e PARDER'''
    t[0] = t[3]

def p_cadena_impresion_1(t):
    ''' cadena_impresion : cadena_impresion e '''
    t[0] = AST.Concatenacion(t[1], t[2], t.lineno(1), 0 )

def p_cadena_impresion_2(t):
    ''' cadena_impresion : STRING '''
    t[0] = AST.String(t[1], t.lineno(1), 0) 

def p_lista_expresion(t):
    ''' lista_e : lista_e COMA e '''
    t[0] = t[1]
    t[0].append(t[3])

def p_lista_expresion_2(t):
    ''' lista_e : lista_e e '''
    t[0] = t[1]
    t[0].append(t[2])

def p_lista_expresion_base(t):
    ''' lista_e : e '''
    t[0] = []
    t[0].append(t[1])

def p_uppercase(t):
    '''uppercase : UPPERCASE PARIZQ e PARDER  '''
    t[0] = AST.Uppercase(t[3], t.lineno(1), 0)

def p_lowercase(t):
    '''lowercase : LOWERCASE PARIZQ e PARDER  '''
    t[0] = AST.Lowercase(t[3], t.lineno(1), 0)


def p_log10(t):
    '''log10 : LOG10 PARIZQ e PARDER  '''
    t[0] = AST.Log10(t[3], t.lineno(1), 0)

def p_log(t):
    '''log : LOG PARIZQ e COMA e PARDER  '''
    t[0] = AST.Log(t[3], t[5], t.lineno(1), 0)

def p_sin(t):
    '''sin : SIN PARIZQ e PARDER'''
    t[0] = AST.Sin(t[3], t.lineno(1),0)

def p_cos(t):
    '''cos : COS PARIZQ e PARDER'''
    t[0] = AST.Cos(t[3], t.lineno(1),0)

def p_tan(t):
    '''tan : TAN PARIZQ e PARDER'''
    t[0] = AST.Tan(t[3], t.lineno(1),0)

def p_sqrt(t):
    '''sqrt : SQRT PARIZQ e PARDER'''
    t[0] = AST.Sqrt(t[3], t.lineno(1),0)

## Expresion --------------- e --> expresiones
def p_expresion_parentesis(t):
    '''e : PARIZQ e PARDER'''
    t[0]=t[2]

def p_expresion_log10(t):
    '''e : log10'''
    t[0] = t[1]

def p_expresion_log(t):
    '''e : log'''
    t[0] = t[1]

def p_expresion_sin(t):
    '''e : sin'''
    t[0] = t[1]

def p_expresion_cos(t):
    '''e : cos'''
    t[0] = t[1]

def p_expresion_tan(t):
    '''e : tan'''
    t[0] = t[1]

def p_expresion_sqrt(t):
    '''e : sqrt'''
    t[0] = t[1]

def p_expresion_uppercase(t):
    '''e : uppercase'''
    t[0] = t[1]

def p_expresion_lowercase(t):
    '''e : lowercase'''
    t[0] = t[1]

def p_expresion_negativo(t):
    '''e : MENOS e  %prec UMINUS'''
    t[0] = AST.Negativo(t[2], t.lineno(1), 0)

def p_expresion_suma(t):
    '''e : e MAS e'''
    t[0] = AST.Suma(t[1], t[3], t.lineno(1), 0)

def p_expresion_resta(t):
    '''e : e MENOS e'''
    t[0] = AST.Resta(t[1], t[3], t.lineno(1), 0)  

def p_expresion_multiplicacion(t):
    '''e : e POR e'''
    t[0] = AST.Multiplicacion(t[1], t[3], t.lineno(1), 0) 

def p_expresion_division(t):
    '''e : e DIV e'''
    t[0] = AST.Division(t[1], t[3], t.lineno(1), 0)  

def p_expresion_potencia(t):
    '''e : e POW e'''
    t[0] = AST.Potencia(t[1], t[3], t.lineno(1), 0) 

def p_expresion_modulo(t):
    '''e : e MODULO e'''
    t[0] = AST.Modulo(t[1], t[3], t.lineno(1), 0)                 
   
def p_expresion_mayor(t):
    '''e : e MAY e '''
    t[0] = AST.Mayor(t[1], t[3], t.lineno(1), 0)

def p_expresion_menor(t):
    '''e : e MEN e '''
    t[0] = AST.Menor(t[1], t[3], t.lineno(1), 0)  

def p_expresion_mayor_igual(t):
    '''e : e MAYIG e'''
    t[0] = AST.MayorIgual(t[1], t[3], t.lineno(1), 0)

def p_expresion_menor_igual(t):
    '''e : e MENIG e'''
    t[0] = AST.MenorIgual(t[1], t[3], t.lineno(1), 0)

def p_expresion_or(t):
    '''e : e OR e'''
    t[0] =  AST.Or(t[1], t[3], t.lineno(1),0)

def p_expresion_and(t):
    '''e : e AND e'''
    t[0] =  AST.And(t[1], t[3], t.lineno(1),0)

def p_expresion_not(t):
    '''e : NOT e '''
    t[0] = AST.Not(t[2], t.lineno(1), 0)

## Valores literales -------------------------------------------
def p_expresion_nulo(t):
    '''e : NULO'''
    t[0]=  AST.Nulo(t.lineno(1), 0)

def p_expresion_entero(t):
    '''e : ENTERO'''
    t[0]=  AST.Entero(t[1], t.lineno(1), 0)

def p_expresion_float(t):
    '''e : FLOAT'''
    t[0]=  AST.Float(t[1], t.lineno(1), 0)

def p_expresion_bool_true(t):
    '''e : RTRUE'''
    t[0]=  AST.Bool(t[1], t.lineno(1), 0)  

def p_expresion_bool_false(t):
    '''e : RFALSE'''
    t[0]=  AST.Bool(t[1], t.lineno(1), 0)  

def p_expresion_char(t):
    '''e : CHAR'''
    t[0] = AST.Char(t[1], t.lineno(1), 0)

def p_expresion_string(t):
    '''e : STRING'''
    t[0] = AST.String(t[1], t.lineno(1), 0)

def p_expresion_string_2(t):
    '''e : DOLAR'''
    t[0] = AST.String(t[1], t.lineno(1), 0)    

def p_expresion_variable(t):
    '''e : ID'''
    t[0] = AST.Variable(t[1], t.lineno(1), 0 )


def p_error(t):         
    if t is not None:
        global_utils.registrySyntaxError(t.value,'Error de sintaxis. No se esperaba ' + t.type, t.lineno , find_column(t)) 
    else:
        print ('Error sintactico ' + str(t))

import ply.yacc as yacc
parser = yacc.yacc()

def parse(input):
    global input_ANY_init
    global linea
    global columna    
    global final_cadena
    final_cadena = False
    input_ANY_init = input
    linea = 0 
    columa = 0
    
    return parser.parse(input,tracking=True)