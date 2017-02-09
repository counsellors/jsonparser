#!/usr/bin/env python
#-*- coding: utf-8 -*-


from ply import lex,yacc
import networkx as nx
import logging
import json

FORMAT = '[%(asctime)s] %(filename)s:%(lineno)s-%(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


parser = None
lexer = None
tokens = (
    'LSBRACKET',
    'RSBRACKET',
    'LBRACE',
    'RBRACE',
    'COLON',
    'NORMSTRING',
    'CONSTANT',
    'VARIABLE',
    'COMMA',
    'KEYWORDS',
    )

t_ignore = ' \t\r'
t_LSBRACKET  = r'\['
t_RSBRACKET  = r'\]'
t_LBRACE  = r'\{'
t_RBRACE   = r'\}'
t_COLON  = r':' 
t_COMMA  = r',' 

KEYWORDS = [
    r'null',
]


keyword = '|'.join(keyword.replace(' ', '\s+') for keyword in KEYWORDS)

def t_error(t):
    raise Exception('Error {} at line {}'.format(t.value[0], t.lineno))


@lex.TOKEN(keyword)
def t_KEYWORDS(t):
    # todo: to support false,true
    t.value = None
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno +=len(t.value)

def t_NORMSTRING(t):
    r'"([^"\n]|(\\"))*"'
    logging.debug("String: '%s'" % t.value)
    t.value = str(t.value[1:-1])
    return t

def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z_0-9\.]*'
    return t

def t_CONSTANT(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t

literals = '+-;='



def p_root_block_1(p):
    """ root_block : LSBRACKET block_item_list RSBRACKET
    """
    p[0] = list(p[2]) if not isinstance( p[2],list) else p[2]

def p_root_block_2(p):
    """ root_block : LBRACE block_item_list RBRACE
    """
    p[0] = {}
    if not isinstance( p[2],dict ):
        if isinstance( p[2],list ):
            for value in p[2]:
                p[0].update(value)
        elif p[2] is None:
            p[0].update(p[2])
        else:
            p[0] = dict(p[2])
    else:
        p[0] = p[2]

def p_root_block_3(p):
    """ root_block : CONSTANT
                   | NORMSTRING COLON root_block
                   | NORMSTRING
                   | KEYWORDS
    """
    if len(p) == 4:
        p[0] = {p[1]:p[3]}
    else:
        p[0] = p[1] 

def p_block_item_list(p):
    """ block_item_list : block_item_list COMMA root_block
                        | root_block
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_empty(p):
    'empty : '
    p[0] = None

def p_error(p):
    global lexer,parser
    # If error recovery is added here in the future, make sure
    # _get_yacc_lookahead_token still works!
    #
    # get formatted representation of stack
    stack_state_str = ' '.join([symbol.type for symbol in parser.symstack][1:])

    print('Syntax error in input! Parser State:{} {} . {}'
          .format(parser.statestack,
                  stack_state_str,
                  p))
    if p:
        last_cr = lexer.lexdata.rfind('\n', 0, p.lexpos)
        column = p.lexpos - last_cr
        logging.error(
            'before: %s ,line %s column %s' % (repr(p.value),p.lineno,column ) )
        parser.errok()

    else:
        logging.error('At end of input')

if __name__ == '__main__':
    global lexer,parser
    filename = 'test/exp2.json'
    lexer = lex.lex(debug=1)
    with open(filename, 'r') as inputfile:
        contents = inputfile.read()
        lexer.input(contents)
        # for token in lexer: #for this part, the file is read correctly
        #     logging.debug("line %d : %s (%s) " % (token.lineno, token.type, token.value))
        parser = yacc.yacc(debug=1)
        s = parser.parse(contents)
        print s
        print json.dumps(s)
