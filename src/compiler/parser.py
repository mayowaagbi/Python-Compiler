import ply.yacc as yacc
from ply.lex import lex

# Assuming your lexer is already defined and imported
from lexer import tokens  # Replace with your actual lexer file name


# Step 3: Define Parsing Rules
def p_program(p):
    '''program : statement_list'''
    print("Program parsed successfully!")

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    pass  # Placeholder for any actions to perform

def p_statement_expr(p):
    '''statement : expression SEMICOLON
                 | assignment_statement'''
    pass  # Placeholder for any actions to perform

def p_assignment_statement(p):
    '''assignment_statement : ID EQUALS expression SEMICOLON'''
    print(f"Assigned {p[3]} to {p[1]}")

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression OPERATOR expression'''
    p[0] = p[1] + p[3]  # Example action (should actually evaluate)

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = p[1]

def p_expression_string(p):
    '''expression : STRING'''
    p[0] = p[1]

def p_expression_boolean(p):
    '''expression : TRUE
                  | FALSE'''
    p[0] = p[1] == "True"

def p_error(p):
    print("Syntax error at '%s'" % p.value if p else "Syntax error at EOF")

# Step 4: Build the Parser
parser = yacc.yacc()

# Example code to parse
test_code = """
x = 42;
if x > 10 {
    print("Greater than 10");
    if True {
        print("This is true");
    }
}
"""

# Step 5: Running the Parser
if __name__ == "__main__":
    lexer.input(test_code)
    result = parser.parse(lexer=lexer)
