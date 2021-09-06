def p_expresion_decimal(t):
    '''e    : DECIMAL'''
    t[0] = new Decimal(t[t1], t.lineno, t.lexpos)

def p_expresion_nulo(t):
    '''e    : NULO '''
    t[0] = new Nulo(t.lineno, t.lexpos)

def p_expresion_bool(t):
    '''e    : TRUE
            | FALSE'''
    t[0] = new Bool(t[1], t.lineno, t.lexpos)

def p_expresion_caracter(t):
    '''e    : CARACTER'''
    t[0] = new Caracter(t[1], t.lineno, t.lexpos )

def p_expresion_cadena(t):
    '''e    : CADENA ''' 
    t[0] = new Cadena(t[1], t.lineno, t.lexpos)


def p_expresion_binaria_suma(t):
    '''e  :     e   MAS     e'''
    t[0] = new Suma(t[1], t[3], t.lineno, t.lexpos)


def p_expresion_unaria(t):
    '''e  :     MENOS   e   %prec   UMENOS'''    
    t[0]= new Menos(t[2], t.lineno, t.lexpos)    


def p_instruccion_imprimir(t):
    '''imprimir : IMPRIMIR PARIZQ lista_expresion PARDER '''
    t[0]= Imprimir(t[3], t.lineno, t.lexpos)

def p_expresion_lista_expresiones(t):
    '''lista_expresion : lista_expresion COMA e '''
    t[1].addExpresion(t[4])
    t[0] = t[1]

def p_expresion_lista_expresion_init(t):
    '''lista_expresion : e '''
    t[0] =  Lista_expresiones(t.lineno, t.lexpos)
    t[0].addExpresion(t[1])    