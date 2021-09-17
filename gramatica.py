# --------------------
# Erick Tejaxún
# USAC 2021
# --------------------
from singlenton import global_utils

# tokens definition
tokens = (
    'PARIZQ',
    'PARDER',
    'MAS',
    'MENOS',
    'POR',
    'DIV',
    'AND',
    'OR',
    'IGIG',
    'DIFDE',
    'MAY',
    'MEN',
    #-------PRIMITIVAS
    'NULO',
    'FLOAT',
    'ENTERO',
    'RTRUE',
    'RFALSE',
    'CHAR',
    'STRING',
    'IMPRIMIR',
    #----------->
    'PUNTOCOMA'

)

t_PUNTOCOMA=r';'
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIV = r'/'
t_AND = r'&'
t_OR = r'\|'
t_IGIG = r'=='
t_DIFDE = r'!='
t_MAY = r'>'
t_MEN = r'<'
t_IMPRIMIR = 'println'



# ignored characters, tab and space
t_ignore = " \t"


def t_COMMENT(t):
    r'\#.*'
    print("Comentario  " + t.value)
    pass

#def t_COMMENT_MULTI(t):
#    r'(?s)\#=.*?=\#'
#    print("Comentario multilinea: " + t.value)
#    pass

def t_CHAR(t):
    r'\'([^\\\n]|(\\.))*?\''
    string = str(t.value)
    if len(string) == 2 :
        t.value = ''
    else:
        t.value = string[1]
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t

def t_NULO(t):
    r'nothing'    
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        # log error         
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        # log error         
        #print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_RTRUE(t):
    r'true'
    t.value = True    
    return t

def t_RFALSE(t):
    r'false'
    t.value = False    
    return t
    

def t_line(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):    
    global_utils.registryLexicalError(t.value[0],'Caracter ilegal.', t.lexer.lineno, t.lexer.lineno)    
    t.lexer.skip(1)



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
    #('right','UMENOS'),
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

def p_lista_instrucciones(t):
    '''lista_instrucciones : lista_instrucciones imprimir'''    
    t[1].agregarInstruccion(t[2])
    t[0] = t[1]

def p_lista_instrucciones_init(t):
    '''lista_instrucciones : imprimir'''
    t[0] = AST.Bloque(t.lineno, t.lexpos)
    t[0].agregarInstruccion(t[1])

# Definicion de la gramática
def p_instruccion_imprimir(t):
    '''imprimir : IMPRIMIR PARIZQ e PARDER PUNTOCOMA '''
    t[0]= AST.Imprimir(t[3], t.lineno, t.lexpos)


def p_expresion_parentesis(t):
    'e : PARIZQ e PARDER'
    t[0]=t[2]

## Valores literales
def p_expresion_nulo(t):
    '''e : NULO'''
    t[0]=  AST.Nulo(t.lineno, t.lexpos)

def p_expresion_entero(t):
    '''e : ENTERO'''
    t[0]=  AST.Entero(t[1], t.lineno, t.lexpos)

def p_expresion_float(t):
    '''e : FLOAT'''
    t[0]=  AST.Float(t[1], t.lineno, t.lexpos)

def p_expresion_bool_true(t):
    '''e : RTRUE'''
    t[0]=  AST.Bool(t[1], t.lineno, t.lexpos)    

def p_expresion_bool_false(t):
    '''e : RFALSE'''
    t[0]=  AST.Bool(t[1], t.lineno, t.lexpos)    

def p_expresion_char(t):
    '''e : CHAR'''
    t[0] = AST.Char(t[1], t.lineno, t.lexpos)

def p_expresion_string(t):
    '''e : STRING'''
    t[0] = AST.String(t[1], t.lineno, t.lexpos)


def p_error(t):     
    #print("Error sintáctico en "+str(t)+" linea: ")
    global_utils.registrySyntaxError(str(t),'Error de sintaxis', t.lineno, t.lexpos)    

import ply.yacc as yacc
parser = yacc.yacc()

def parse(input):
    return parser.parse(input)