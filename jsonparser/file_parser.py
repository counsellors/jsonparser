#!/usr/bin/env python
#-*- coding: utf-8 -*-


from ply import lex,yacc
import networkx as nx
import logging

FORMAT = '[%(asctime)s] %(filename)s:%(lineno)s-%(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

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
    )

t_ignore = ' \t\r'
t_LSBRACKET  = r'\['
t_RSBRACKET  = r'\]'
t_LBRACE  = r'\{'
t_RBRACE   = r'\}'
t_COLON  = r':' 
t_COMMA  = r',' 

KEYWORDS = [
    r'n/a',
]
keyword = '|'.join(keyword.replace(' ', '\s+') for keyword in KEYWORDS)

def t_error(t):
    raise Exception('Error {} at line {}'.format(t.value[0], t.lineno))


@lex.TOKEN(keyword)
def t_KEYWORD(t):
    # remove spaces
    t.value = ''.join(x for x in t.value if not x.isspace())

def t_newline(t):
    r'\n+'
    t.lexer.lineno +=len(t.value)

def t_NORMSTRING(t):
    r'"([^"\n]|(\\"))*"'
    logging.debug("String: '%s'" % t.value)

def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z_0-9\.]*'
    return t

def t_CONSTANT(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t

literals = '+-;='


def p_root_block(p):
    """ root_block : LSBRACKET block_item_list RSBRACKET
                   | LBRACE block_item_list RBRACE
                   | CONSTANT
                   | NORMSTRING
                   | NORMSTRING COLON root_block
    """
    p[0] = p[1] 

def p_block_item_list(p):
    """ block_item_list : root_block
                        | block_item_list COMMA root_block
    """
    # Empty block items (plain ';') produce [None], so ignore them
    p[0] = p[1] if (len(p) == 2 or p[2] == [None]) else p[1] + p[2]


def p_empty(p):
    'empty : '
    p[0] = None

def p_error(p):
    # If error recovery is added here in the future, make sure
    # _get_yacc_lookahead_token still works!
    #
    if p:
        logging.error(
            'before: %s ,line %s' % (p.value,p.lineno) )
    else:
        logging.error('At end of input')

if __name__ == '__main__':
    filename = 'test/exp1.json'
    # filename = "rules/sd_topics.C"
    lexer = lex.lex(debug=1)
    with open(filename, 'r') as inputfile:
        contents = inputfile.read()
        lexer.input(contents)
        # for token in lexer: #for this part, the file is read correctly
        #     logging.debug("line %d : %s (%s) " % (token.lineno, token.type, token.value))
        parser = yacc.yacc(debug=True)
        s = parser.parse(contents)
        # result = yacc.parse(contents, debug=True)
        # print(result) #Stack immediatly contains . $end and the p_error(p) I've defined confirms EOF was reached
        # tmp = "{{var1 := 'some text' ; var2 := 'some other text' ; var3 := ( 'text', 'text2') ; }}" #Same contents as the input file
        # result = yacc.parse(tmp, debug=True)
        # print(result) #correct results
