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
flag_impresion = False
contador_parentesis = 0

#Estados 
states = (
    ('cadena', 'exclusive'),
    ('impresion', 'exclusive'),
    ('expresion', 'exclusive'),
    ('expresionInicio','exclusive'),
    ('parentesis', 'exclusive')
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
    'DPUNTO',
    'BRACKETI',
    'BRACKETD',
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
    'TSTRING',
    'CARACTER',
    'IF',
    'ELSE',
    'ELSEIF',
    'WHILE',
    'FOR',
    'IN',
    'BREAK',
    'CONTINUE',
    'FUNCTION',
    'END',
    'INTERROGACION'

)

#tipos primitivos
#t_INITIAL_TINT64 = r'Int64'
#t_INITIAL_TFLOAT64 = r'Float64'
#t_INITIAL_TBOOL = r'Bool'
#t_INITIAL_TCHAR = r'Char'
#t_INITIAL_TSTRING = r'String'
def t_INITIAL_impresion_expresion_PUNTOCOMA(t):
    r';'
    t.lexer.begin('INITIAL')
    return t

def t_INITIAL_impresion_expresion_INTERROGACION(t):
    r'\?'
    t.lexer.begin('INITIAL')
    return t    

def t_INITIAL_impresion_expresion_COMA(t):
    r','
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t    

def t_INITIAL_cadena_impresion_PARIZQ(t):
    r'\('
    global contador_parentesis 
    contador_parentesis += 1  
    print('Parentesis ' + str(contador_parentesis) + '\tEstado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))      
    return t

def t_INITIAL_cadena_PARDER(t):
    r'\)'
    global contador_parentesis 
    contador_parentesis -= 1
    print('Parentesis ' + str(contador_parentesis) + '\tEstado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))    
    return t


def t_INITIAL_impresion_expresion_MAS(t):
    r'\+'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t      

def t_INITIAL_impresion_expresion_MENOS(t):
    r'-'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t      


def t_INITIAL_impresion_expresion_DIV(t):
    r'/'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t      

def t_INITIAL_impresion_expresion_AND(t) :
    r'&&'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t      


def t_INITIAL_impresion_expresion_OR(t):
    r'\|\|'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t      

def t_INITIAL_impresion_expresion_DIFDE(t):
    r'!='
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t

def t_INITIAL_impresion_expresion_NOT(t):
    r'!'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t  

def t_INITIAL_impresion_expresion_IGIG(t):
    r'=='
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t    

def t_INITIAL_impresion_expresion_IGUAL(t):
    r'='
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t

def t_INITIAL_impresion_expresion_MENIG(t):
    r'<='
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t    

def t_INITIAL_impresion_expresion_MAYIG(t):
    r'>='
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t    
def t_INITIAL_impresion_expresion_MAY(t):
    r'>'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t

def t_INITIAL_impresion_expresion_MEN(t):
    r'<'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t

def t_INITIAL_impresion_expresion_BRACKETI(t):
    r'\['
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t    

def t_INITIAL_impresion_expresion_BRACKETD(t):
    r'\]'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t    

t_INITIAL_impresion_expresion_POW = r'\^'
t_INITIAL_impresion_expresion_MODULO = r'%'
t_INITIAL_impresion_expresion_DPUNTOS = r'::'
t_INITIAL_impresion_expresion_DPUNTO = r':'

# ignored characters, tab and space
t_INITIAL_impresion_ignore = " \t"

def t_INITIAL_impresion_expresion_FUNCTION(t):
    r'function'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t 

def t_INITIAL_impresion_expresion_CONTINUE(t):
    r'continue'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t 

def t_INITIAL_impresion_expresion_BREAK(t):
    r'break'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t 

def t_INITIAL_impresion_expresion_FOR(t):
    r'for'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t 

def t_INITIAL_impresion_expresion_IN(t):
    r'in'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t 


def t_INITIAL_impresion_expresion_WHILE(t):
    r'while'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t 

def t_INITIAL_impresion_expresion_IF(t):
    r'if'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t 

def t_INITIAL_impresion_expresion_ELSEIF(t):
    r'elseif'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t 

def t_INITIAL_impresion_expresion_ELSE(t):
    r'else'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t      

def t_INITIAL_impresion_expresion_END(t):
    r'end'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t     

def t_INITIAL_impresion_expresion_POR(t):
    r'\*'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t    

def t_impresion_expresion_expresionInicio_parentesis_LOG10(t):
    r'log10'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t   

def t_impresion_expresion_expresionInicio_parentesis_LOG(t):
    r'log'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t   

def t_impresion_expresion_expresionInicio_parentesis_SIN(t):
    r'sin'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t    

def t_impresion_expresion_expresionInicio_parentesis_COS(t):
    r'cos'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t   

def t_impresion_expresion_expresionInicio_parentesis_TAN(t):
    r'tan'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t    

def t_impresion_expresion_expresionInicio_parentesis_SQRT(t):
    r'sqrt'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t  

def t_impresion_expresion_expresionInicio_parentesis_UPPERCASE(t):
    r'uppercase'    
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t

def t_impresion_expresion_expresionInicio_parentesis_LOWERCASE(t):
    r'lowercase'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t 

def t_ANY_comment(t):
     r'(\#=(.|\n)*?=\#)|(\#.*)'
     saltos = str(t.value).count('\n')
     if saltos > 0 :
        t.lexer.lineno += saltos
     #print(t.value)     
     pass

def t_INITIAL_TINT64(t):
    r'Int64'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t

def t_INITIAL_TFLOAT64(t):
    r'Float64'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t 

def t_INITIAL_TBOOL(t):
    r'Bool'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t

def t_INITIAL_TCHAR(t):
    r'Char'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t

def t_INITIAL_TSTRING(t):
    r'String'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t

def t_INITIAL_IMPRIMIRLN(t):
    r'println'
    global final_cadena 
    global flag_impresion
    flag_impresion = True
    final_cadena = False    
    t.lexer.begin('impresion')
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t    

def t_INITIAL_IMPRIMIR(t):
    r'print'
    global final_cadena 
    global flag_impresion
    flag_impresion = True    
    final_cadena = False
    t.lexer.begin('impresion')
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t

def t_ANY_NULO(t):
    r'nothing'    
    return t
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
def t_ANY_RTRUE(t):
    r'true'
    t.value = True 
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))   
    return t

def t_ANY_RFALSE(t):
    r'false'
    t.value = False   
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t)) 
    return t

def t_INITIAL_expresion_impresion_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     #t.type = reserved.get(t.value,'ID')    # Check for reserved words
     print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
     return t

def t_impresion_PARDER(t):
    r'\)'
    global flag_impresion
    global contador_parentesis 
    contador_parentesis -= 1       
    if contador_parentesis == 0:
        t.lexer.begin('INITIAL')
        print('Parentesis ' + str(contador_parentesis) + '\tEstado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
        return t 
    print('Parentesis ' + str(contador_parentesis) + '\tEstado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t     
    

def t_ANY_CHAR(t):
    r'\'([^\\\n]|(\\.))*?\''
    string = str(t.value)
    if len(string) == 2 :
        t.value = ''
    else:
        t.value = string[1]
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t

def t_INITIAL_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t

def t_ANY_FLOAT(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        # log error         
        t.value = 0
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t

def t_INITIAL_expresion_impresion_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        # log error         
        #print("Integer value too large %d", t.value)
        t.value = 0
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t

# Inicio de una cadena
def t_impresion_COMILLA(t):
    r'\"'
    global string_cadena_impresion
    global final_cadena         
    string_cadena_impresion  = ''             
    t.lexer.begin('cadena') 
    pass     

def t_expresionInicio_DOLAR(t):
    r'\('
    global string_cadena_impresion 
    global contador_parentesis
    contador_parentesis += 1  
    #t.value = string_cadena_impresion
    t.lexer.begin('expresion')
    string_cadena_impresion  = ''    
    print('Parentesis ' + str(contador_parentesis) + '\tEstado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t

def t_expresion_PARIZQ(t):
    r'\('
    global contador_parentesis
    contador_parentesis += 1
    print('Parentesis ' + str(contador_parentesis) + '\tEstado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t

def t_expresion_PARDER(t):
    r'\)'
    global contador_parentesis
    contador_parentesis -= 1
    print('Parentesis ' + str(contador_parentesis) + '\tEstado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    if contador_parentesis == 1:
        t.type = 'DOLAR'
        t.lexer.begin('cadena')        
        print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
        return t
        #pass    
    else:    
        t.type = 'DOLAR'
        t.lexer.begin('cadena')
        print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
        return t

# Fin de la cadena
def t_cadena_COMILLA(t):
    r'\"'     
    global final_cadena 
    global flag_impresion
    global string_cadena_impresion
    t.value = string_cadena_impresion
    t.lexer.begin('impresion')    
    t.type = 'STRING'
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t    

def t_cadena_STRING(t):
    r'\$'  
    global final_cadena 
    global string_cadena_impresion
    t.value = string_cadena_impresion
    t.lexer.begin('expresionInicio')    
    print('Estado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
    return t   


def t_cadena_CARACTER(t):
    r'.'
    if t.value == '\n':
        t.lexer.lineno += 1            
    global string_cadena_impresion
    string_cadena_impresion = string_cadena_impresion + str(t.value)    
    pass

def t_cadena_DOLAR(t):
    r'\)'
    global contador_parentesis
    contador_parentesis -= 1    
    t.lexer.begin('cadena')
    print('Parentesis ' + str(contador_parentesis) + '\tEstado : ' + str(t.lexer.lexstate)+'  Token : ' + str(t))
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
    ('left', 'MENIG','MAYIG'),
    ('nonassoc', 'MEN', 'MAY'),
    ('left', 'IGIG', 'DIFDE'),    
    ('left','DOLAR'),
    ('left','MAS','MENOS'),
    ('left','POR','DIV'),    
    ('left', 'POW'),
    ('right', 'UMINUS'),
    ('left','PARIZQ', 'PARDER'),  
    ('nonassoc', 'SI_SIMPLE')  
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

def p_lista_instrucciones_4(t):
    '''lista_instrucciones : lista_instrucciones if'''
    t[1].agregarInstruccion(t[2])
    t[0] = t[1]

def p_lista_instrucciones_5(t):
    '''lista_instrucciones : lista_instrucciones while'''
    t[1].agregarInstruccion(t[2])
    t[0] = t[1]

def p_lista_instrucciones_6(t):
    '''lista_instrucciones : lista_instrucciones break'''
    t[1].agregarInstruccion(t[2])
    t[0] = t[1]

def p_lista_instrucciones_7(t):
    '''lista_instrucciones : lista_instrucciones continue'''
    t[1].agregarInstruccion(t[2])
    t[0] = t[1]   

def p_lista_instrucciones_8(t):
    '''lista_instrucciones : lista_instrucciones for'''
    t[1].agregarInstruccion(t[2])
    t[0] = t[1]

def p_lista_instrucciones_9(t):
    '''lista_instrucciones : lista_instrucciones funcion'''
    t[1].agregarInstruccion(t[2])
    t[0] = t[1]   

def p_lista_instrucciones_10(t):
    '''lista_instrucciones : lista_instrucciones llamada PUNTOCOMA'''
    t[1].agregarInstruccion(t[2])
    t[0] = t[1]       

def p_lista_instrucciones_11(t):
    '''lista_instrucciones : lista_instrucciones error'''    
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

def p_lista_instrucciones_if(t):
    '''lista_instrucciones : if'''
    t[0] = AST.Bloque(t.lineno(1), 0)
    t[0].agregarInstruccion(t[1])    

def p_lista_instrucciones_while(t):
    '''lista_instrucciones : while'''
    t[0] = AST.Bloque(t.lineno(1), 0)
    t[0].agregarInstruccion(t[1]) 

def p_lista_instrucciones_for(t):
    '''lista_instrucciones : for'''
    t[0] = AST.Bloque(t.lineno(1), 0)
    t[0].agregarInstruccion(t[1])

def p_lista_instrucciones_break(t):
    '''lista_instrucciones : break'''
    t[0] = AST.Bloque(t.lineno(1), 0)
    t[0].agregarInstruccion(t[1])  

def p_lista_instrucciones_continue(t):
    '''lista_instrucciones : continue'''
    t[0] = AST.Bloque(t.lineno(1), 0)
    t[0].agregarInstruccion(t[1])    

def p_lista_instrucciones_funcion(t):
    '''lista_instrucciones : funcion'''
    t[0] = AST.Bloque(t.lineno(1), 0)
    t[0].agregarInstruccion(t[1])  

def p_lista_instrucciones_llamada(t):
    '''lista_instrucciones : llamada PUNTOCOMA'''
    t[0] = AST.Bloque(t.lineno(1), 0)
    t[0].agregarInstruccion(t[1])            

def p_lista_instrucciones_error(t):
    '''lista_instrucciones : error'''
    t[0] = AST.Bloque(t.lineno(1), 0)    

def p_instruccion_funcion_1(t):
    ''' funcion : FUNCTION ID  PARIZQ lista_parametros PARDER lista_instrucciones END PUNTOCOMA'''
    t[0] = AST.Funcion(t[2], t[4], t[6], t.lineno(1), 0)

def p_instruccion_funcion_2(t):
    ''' funcion : FUNCTION ID  PARIZQ  PARDER lista_instrucciones  END PUNTOCOMA'''
    t[0] = AST.Funcion(t[2], None, t[5], t.lineno(1), 0)

def p_lista_parametros_1(t):
    ''' lista_parametros : lista_parametros COMA parametro'''
    t[0] = t[1]
    t[0].append(t[3])

def p_lista_parametro_2(t):
    ''' lista_parametros : parametro'''
    t[0] = []
    t[0].append(t[1])

def p_parametro_1(t):
    ''' parametro : ID'''
    t[0] = AST.Declaracion(t[1], None , None, t.lineno(1), 0)

def p_parametro_2(t):
    ''' parametro : ID DPUNTOS tipo'''
    t[0] = AST.Declaracion(t[1], t[3], None, t.lineno(1), 0)

def p_instruccion_declaracion(t):
    ''' declaracion : ID IGUAL e DPUNTOS tipo PUNTOCOMA'''
    t[0] = AST.Declaracion(t[1], t[3], t[5], t.lineno(1), 0)

def p_instruccion_declaracion_sintipo(t):
    ''' declaracion : ID IGUAL e PUNTOCOMA'''
    t[0] = AST.Declaracion(t[1], t[3], None, t.lineno(1), 0)    

def p_instruccion_if_1(t):
    ''' if : IF e lista_instrucciones END PUNTOCOMA '''
    t[0] = AST.If(t[2],t[3], None,  t.lineno(1), 0)

def p_instruccion_if_2(t):
    ''' if : IF e lista_instrucciones elseif %prec SI_SIMPLE'''
    t[0] = AST.If(t[2],t[3], t[4], t.lineno(1), 0)

def p_instruccion_elseif_3(t):
    '''elseif : ELSE lista_instrucciones END PUNTOCOMA'''
    t[0] = AST.If(AST.Bool(True,t.lineno(1),0), t[2], None, t.lineno(1), 0)

def p_instruccion_elseif_1(t):
    '''elseif : ELSEIF e lista_instrucciones elseif'''
    t[0] = AST.If(t[2],t[3],t[4], t.lineno(1), 0)

def p_instruccion_elseif_2(t):
    '''elseif : ELSEIF e lista_instrucciones END PUNTOCOMA'''
    t[0] = AST.If(t[2],t[3],None, t.lineno(1), 0)

def p_instruccion_while(t):
    ''' while : WHILE e lista_instrucciones END PUNTOCOMA'''
    t[0] = AST.While(t[2], t[3], t.lineno(1),0)

## For
def p_instruccion_for_1(t):
    ''' for : FOR ID IN e lista_instrucciones END PUNTOCOMA'''
    t[0] = AST.For(t[2], t[4], t[5], t.lineno(1), 0)

def p_instruccion_for_2(t):
    ''' for : FOR ID IN rango lista_instrucciones END PUNTOCOMA'''
    t[0] = AST.For(t[2], t[4], t[5], t.lineno(1), 0)    

def p_rango(t):
    ''' rango : e DPUNTO e '''
    t[0] = AST.Rango(t[1],t[3], t.lineno(1),0)

## Fin For
def p_instruccion_BREAK(t):
    '''break : BREAK PUNTOCOMA'''
    t[0] = AST.Break(t.lineno(1),0)

def p_instruccion_CONTINUE(t):
    '''continue : CONTINUE PUNTOCOMA'''
    t[0] = AST.Continue(t.lineno(1),0)    

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

def p_tipo_id(t):
    ''' tipo : ID ''' 
    t[0] = AST.Tipo(AST.TipoPrimitivo.STRUCT, t[1])

def p_instruccion_imprimirln(t):
    '''imprimirln : IMPRIMIRLN PARIZQ lista_e PARDER PUNTOCOMA '''
    t[0]= AST.ImprimirLn(t[3], t.lineno(1), 0)

def p_instruccion_imprimir(t):
    '''imprimir : IMPRIMIR PARIZQ lista_e PARDER PUNTOCOMA '''
    t[0]= AST.Imprimir(t[3], t.lineno(1), 0)

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


def p_lista_expresion_base(t):
    ''' lista_e : e '''
    t[0] = []
    t[0].append(t[1])

def p_arreglo_elemento(t):
    ''' arreglo : BRACKETI lista_e BRACKETD'''
    t[0] = AST.Arreglo(t[2],t.lineno(1),0)

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

def p_expresion_arreglo(t):
    ''' e : arreglo'''
    t[0] = t[1]

def p_expresion_ternario(t):
    ''' e : ternario '''
    t[0] = t[1]

def p_expresion_llamada(t):
    ''' e : llamada '''

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

def p_expresion_igual_igual(t):
    '''e : e IGIG e'''
    t[0] = AST.Igualigual(t[1], t[3], t.lineno(1), 0)    

def p_expresion_diferente(t):
    '''e : e DIFDE e'''
    t[0] = AST.Diferente(t[1], t[3], t.lineno(1), 0)    

def p_expresion_or(t):
    '''e : e OR e'''
    t[0] =  AST.Or(t[1], t[3], t.lineno(1),0)

def p_expresion_and(t):
    '''e : e AND e'''
    t[0] =  AST.And(t[1], t[3], t.lineno(1),0)

def p_expresion_concatenar(t):
    '''e : e DOLAR e'''
    t[0] =  AST.Concatenacion(t[1], t[3], t.lineno(1),0)    

def p_expresion_ternario_def(t):
    ''' ternario : e INTERROGACION e DPUNTO e '''
    t[0] = AST.Ternario(t[1], t[3], t[5] ,t.lineno(1),0)

def p_llamada_definicion(t):
    ''' llamada : ID PARIZQ lista_e PARDER'''
    t[0] = AST.Llamada(t[1], t[3], t.lineno(1), 0)

def p_llamada_definicion_2(t):
    ''' llamada : ID PARIZQ  PARDER'''
    t[0] = AST.Llamada(t[1], None, t.lineno(1), 0)

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

def p_expresion_variable(t):
    '''e : ID'''
    t[0] = AST.Variable(t[1], t.lineno(1), 0 )

def p_expresion_comilla(t):
    '''e : COMILLA'''
    t[0] = AST.String(t[1], t.lineno(1), 0)



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
    #global columna    
    global final_cadena
    final_cadena = False
    input_ANY_init = input
    linea = 0 
    columa = 0    
    
    return parser.parse(input,tracking=True)