#!/usr/bin/python3

import sys
import ply.lex as lex
import ply.yacc as yacc


tokens = (
        'NAME', 'NUMBER',
        'PLUS', 'MINUS', 'EXP', 'TIMES', 'DIVIDE', 'EQUALS',
        'LPAREN', 'RPAREN','plus','minus','exp','times','divide','equals','singlenumber','teennumber','doublenumber','hundred','thousand'
)


t_ignore = " \t\n"
t_PLUS = r'\+'
t_MINUS = r'-'
t_EXP = r'\*\*'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

singlenumberdic = {'One':1,'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9}
teennumberdic = {'Ten':10,'Eleven':11,'Twelve':12,'Thirteen':13,'Fourteen':14,'Fifteen':15,'Sixteen':16,'Seventeen':17,'Eighteen':18,'Nineteen':19,'ten':10,'eleven':11,'twelve':12,'thirteen':13,'fourteen':14,'fifteen':15,'sixteen':16,'seventeen':17,'eighteen':18,'nineteen':19}
doublenumberdic = {'Twenty':20,'Thirty':30,'Forty':40,'Fifty':50,'Sixty':60,'Seventy':70,'Eighty':80,'Ninety':90,'twenty':20,'thirty':30,'forty':40,'fifty':50,'sixty':60,'seventy':70,'eighty':80,'ninety':90}
hundreddic = {'Hundred':100,'hundred':100}
thousanddic = {'Thousand':1000,'thousand':1000}

def t_plus(t):
	r'plus'
	t.value = '+'
	return t

def t_minus(t):
	r'minus'
	t.value = '-'
	return t

def t_exp(t):
	r'exp'
	t.value = '**'
	return t

def t_times(t):
	r'times'
	t.value = '*'
	return t

def t_divide(t):
	r'divide'
	t.value = '/'
	return t

def t_equals(t):
	r'equals'
	t.value = '='
	return t

def t_teennumber(t):
	r'Ten|Eleven|Twelve|Thirteen|Fourteen|Fifteen|Sixteen|Seventeen|Eighteen|Nineteen|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen'
	t.value = teennumberdic[t.value]
	return t

def t_doublenumber(t):
	r'Twenty|Thirty|Forty|Fifty|Sixty|Seventy|Eighty|Ninety|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety'
	t.value = doublenumberdic[t.value]
	return t

def t_singlenumber(t):
	r'One|Two|Three|Four|Five|Six|Seven|Eight|Nine|one|two|three|four|five|six|seven|eight|nine'
	t.value = singlenumberdic[t.value]
	return t

def t_hundred(t):
	r'Hundred|hundred'
	t.value = hundreddic[t.value]
	return t

def t_thousand(t):
	r'Thousand|thousand'
	t.value = thousanddic[t.value]
	return t

def t_error(t): 
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

# Parsing rules
precedence = (
	('left', 'PLUS', 'plus', 'MINUS', 'minus'),
        ('left', 'TIMES', 'times', 'DIVIDE', 'divide'),
        ('left', 'EXP', 'exp'),
        ('right', 'UMINUS'),
)

def p_statement_assign(p):
	"""
	statement : NAME EQUALS expression
			 | NAME equals expression
	"""
	p[1]=p[3]

def p_statement_expr(p):
        'statement : expression'
        print(p[1])

def p_char_singlenumber(p):
	'expression : singlenumber'
	p[0]=p[1]

def p_char_teennumber(p):
	'expression : teennumber'
	p[0]=p[1]

def p_char_double_number(p):
		"""
		expression : doublenumber
				  | doublenumber singlenumber
		"""
		if len(p) == 2:
			p[0] = p[1]
		elif len(p) == 3 :
			p[0] = p[1] + p[2]

def p_char_hundred(p):
		"""
		expression : singlenumber hundred
				  | singlenumber hundred doublenumber
				  | singlenumber hundred doublenumber singlenumber
				  | singlenumber hundred teennumber
				  | singlenumber hundred singlenumber
				  | teennumber hundred
				  | teennumber hundred doublenumber
				  | teennumber hundred doublenumber singlenumber
				  | teennumber hundred teennumber
				  | teennumber hundred singlenumber
				  | doublenumber hundred
				  | doublenumber hundred doublenumber
				  | doublenumber hundred doublenumber singlenumber
				  | doublenumber hundred teennumber
				  | doublenumber hundred singlenumber
				  | doublenumber singlenumber hundred
				  | doublenumber singlenumber hundred doublenumber
				  | doublenumber singlenumber hundred doublenumber singlenumber
				  | doublenumber singlenumber hundred teennumber
				  | doublenumber singlenumber hundred singlenumber
		"""
		if len(p) == 3:
			p[0] = p[1]*p[2]
		elif len(p) == 4:
			if p[2] == 100:
				p[0] = p[1]*p[2] + p[3]
			else:
				p[0] = (p[1] + p[2])*p[3]
		elif len(p) == 5:
			if p[2] == 100:
				p[0] = p[1]*p[2] + p[3] + p[4]
			else:
				p[0] = (p[1] + p[2])*p[3] + p[4]
		else:
			p[0] = (p[1] + p[2])*p[3] + p[4] + p[5]

def p_char_thousand(p):
		"""
		expression : singlenumber thousand
				  | singlenumber thousand singlenumber hundred
				  | singlenumber thousand singlenumber hundred doublenumber 														
				  | singlenumber thousand singlenumber hundred doublenumber singlenumber 										
				  | singlenumber thousand singlenumber hundred teennumber 															
				  | singlenumber thousand singlenumber hundred singlenumber 														
				  | singlenumber thousand doublenumber
				  | singlenumber thousand doublenumber singlenumber
				  | singlenumber thousand teennumber
				  | singlenumber thousand singlenumber
				  | teennumber thousand
				  | teennumber thousand singlenumber hundred
				  | teennumber thousand singlenumber hundred doublenumber 															
				  | teennumber thousand singlenumber hundred doublenumber singlenumber 											
				  | teennumber thousand singlenumber hundred teennumber 															
				  | teennumber thousand singlenumber hundred singlenumber 															
				  | teennumber thousand teennumber
				  | teennumber thousand singlenumber
				  | doublenumber thousand
				  | doublenumber thousand singlenumber hundred
				  | doublenumber thousand singlenumber hundred doublenumber 														
				  | doublenumber thousand singlenumber hundred doublenumber singlenumber 										
				  | doublenumber thousand singlenumber hundred teennumber 															
				  | doublenumber thousand singlenumber hundred singlenumber             											
				  | doublenumber thousand teennumber
				  | doublenumber thousand singlenumber
				  | singlenumber hundred thousand
				  | singlenumber hundred singlenumber thousand
				  | singlenumber hundred singlenumber thousand singlenumber hundred 											
				  | singlenumber hundred singlenumber thousand singlenumber hundred doublenumber 							
				  | singlenumber hundred singlenumber thousand singlenumber hundred doublenumber singlenumber 			
				  | singlenumber hundred singlenumber thousand singlenumber hundred teennumber 								
				  | singlenumber hundred singlenumber thousand singlenumber hundred singlenumber 							
				  | singlenumber hundred singlenumber thousand doublenumber 														
				  | singlenumber hundred singlenumber thousand doublenumber singlenumber 										
				  | singlenumber hundred singlenumber thousand teennumber 															
				  | singlenumber hundred singlenumber thousand singlenumber  														
				  | singlenumber hundred teennumber thousand
				  | singlenumber hundred teennumber thousand singlenumber hundred 												
				  | singlenumber hundred teennumber thousand singlenumber hundred doublenumber 								
				  | singlenumber hundred teennumber thousand singlenumber hundred doublenumber singlenumber 			
				  | singlenumber hundred teennumber thousand singlenumber hundred teennumber 								
				  | singlenumber hundred teennumber thousand singlenumber hundred singlenumber 								
				  | singlenumber hundred teennumber thousand teennumber 															
				  | singlenumber hundred teennumber thousand singlenumber 															
				  | singlenumber hundred doublenumber thousand
				  | singlenumber hundred doublenumber thousand singlenumber hundred 											
				  | singlenumber hundred doublenumber thousand singlenumber hundred doublenumber 							
				  | singlenumber hundred doublenumber thousand singlenumber hundred doublenumber singlenumber 			
				  | singlenumber hundred doublenumber thousand singlenumber hundred teennumber 								
				  | singlenumber hundred doublenumber thousand singlenumber hundred singlenumber 							
				  | singlenumber hundred doublenumber thousand teennumber 															
				  | singlenumber hundred doublenumber thousand singlenumber 														
				  |	singlenumber hundred doublenumber singlenumber thousand 														
				  | singlenumber hundred doublenumber singlenumber thousand singlenumber hundred 										
				  | singlenumber hundred doublenumber singlenumber thousand singlenumber hundred doublenumber 							
				  | singlenumber hundred doublenumber singlenumber thousand singlenumber hundred doublenumber singlenumber 			
				  | singlenumber hundred doublenumber singlenumber thousand singlenumber hundred teennumber 								
				  | singlenumber hundred doublenumber singlenumber thousand singlenumber hundred singlenumber 							
				  | singlenumber hundred doublenumber singlenumber thousand teennumber 														
				  | singlenumber hundred doublenumber singlenumber thousand singlenumber 										
		"""
		if len(p) == 3:
			p[0] = p[1]*p[2]
		elif len(p) == 4:
			if p[2] == 100:
				p[0] = p[1]*p[2]*p[3]
			else:
				p[0] = p[1]*p[2] + p[3]
		elif len(p) == 5:
			if p[4] == 100:
				p[0] = p[1]*p[2] + p[3]*p[4]
			elif p[4] == 1000:
				p[0] = p[1]*p[2]*p[4]+p[3]*p[4]
			else:
				p[0] = p[1]*p[2] + p[3] + p[4]
		elif len(p) == 6:
			if p[4] == 100:
				p[0] = p[1]*p[2] + p[3] * p[4] + p[5]
			elif p[4] == 1000:
				p[0] = p[1]*p[2]*p[4]+p[3]*p[4] + p[5]
			else:
				p[0] = p[1]*p[2]*p[5] + (p[3] + p[4])*p[5]
		elif len(p) == 7:
			if p[4] == 100:
				p[0] = p[1]*p[2] + p[3] * p[4] + p[5] + p[6]
			elif p[4] == 1000:
				if p[6] == 100:
					p[0] = p[1]*p[2]*p[4]+p[3]*p[4] + p[5]*p[6]
				else:
					p[0] = p[1]*p[2]*p[4]+p[3]*p[4] + p[5] + p[6] 
			else:
				p[0] = p[1]*p[2]*p[5] + (p[3] + p[4])*p[5] + p[6]
		elif len(p) == 8:
			if p[4] == 1000:
				p[0] = p[1]*p[2]*p[4]+p[3]*p[4] + p[5]*p[6] + p[7]
			else:
				p[0] = p[1]*p[2]*p[5] + (p[3] + p[4])*p[5] + p[6]*p[7] 								
		elif len(p) == 9:
			if p[4] == 1000:
				p[0] = p[1]*p[2]*p[4]+p[3]*p[4] + p[5]*p[6] + p[7] + p[8]
			else:
				p[0] = p[1]*p[2]*p[5] + (p[3] + p[4])*p[5] + p[6]*p[7] + p[8]
		else:
			p[0] = p[1]*p[2]*p[5] + (p[3] + p[4])*p[5] + p[6]*p[7] + p[8] + p[9]


def p_expression_binop(p):
        """
        expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression EXP expression
                  | expression plus expression
                  | expression minus expression
                  | expression times expression
                  | expression divide expression
                  | expression exp expression
        """
        # print [repr(p[i]) for i in range(0,4)]
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]
        elif p[2] == '**':
            p[0] = p[1] ** p[3]

def p_expression_uminus(p):
        'expression : MINUS expression %prec UMINUS'
        p[0] = -p[2]

def p_expression_group(p):
        'expression : LPAREN expression RPAREN'
        p[0] = p[2]

def p_expression_number(p):
        'expression : NUMBER'
        p[0] = p[1]

def p_expression_name(p):
        'expression : NAME'
        try:
            p[0] = p[1]
        except LookupError:
            print("Undefined name '%s'" % p[1])
            p[0] = 0

def p_error(p):
	if p:
		print("syntax error at {0}".format(p.value))
	else:
		print("syntax error at EOF")		

def process(data):
	lex.lex()
	yacc.yacc()
	yacc.parse(data)

if __name__ == "__main__":
	print("Enter the Equation")
	data = sys.stdin.readline()
	process(data)
