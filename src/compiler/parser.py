# import ply.yacc as yacc
# from lexer import tokens, lexer  # Import tokens and lexer

# # Symbol table as a stack for handling scope
# symbol_stack = [{}]

# def enter_new_scope():
#     symbol_stack.append({})  # Push a new symbol table for a new scope

# def exit_scope():
#     symbol_stack.pop()  # Pop the symbol table when exiting the scope

# def get_current_scope():
#     return symbol_stack[-1]  # Get the current symbol table

# def assign_symbol(name, value):
#     current_scope = get_current_scope()
#     current_scope[name] = value

# def lookup_symbol(name):
#     for scope in reversed(symbol_stack):
#         if name in scope:
#             return scope[name]
#     return None

# def execute_statement(statement):
#     if isinstance(statement, tuple):
#         statement_type = statement[0]
#         if statement_type == 'assignment':
#             _, var_name, value = statement
#             assign_symbol(var_name, value)
#         elif statement_type == 'function_call':
#             _, function_name, arguments = statement
#             function_def = lookup_symbol(function_name)
#             if function_def:
#                 params, body = function_def
#                 new_scope = dict(zip(params, arguments))
#                 symbol_stack.append(new_scope)
#                 execute_function(body)
#                 symbol_stack.pop()
#             else:
#                 print(f"Error: Function {function_name} is not defined")
#         elif statement_type == 'return':
#             return statement[1]
#         # Add more execution cases for different statement types

# def execute_function(body):
#     for statement in body:
#         execute_statement(statement)

# def instantiate_object(class_name):
#     class_def = lookup_symbol(class_name)
#     if class_def:
#         return class_def  # Create an instance here if needed
#     print(f"Error: Class {class_name} is not defined")
#     return None

# # Parsing rules
# def p_program(p):
#     '''program : statement_list'''
#     p[0] = ('program', p[1])
#     print("Program parsed successfully")

# def p_statement_list(p):
#     '''statement_list : statement_list statement
#                       | statement'''
#     p[0] = p[1] + [p[2]] if len(p) == 3 else [p[1]]

# def p_statement(p):
#     '''statement : assignment_statement
#                  | if_statement
#                  | while_statement
#                  | for_statement
#                  | function_definition
#                  | block_statement
#                  | return_statement
#                  | COMMENT
#                  | NEWLINE'''
#     p[0] = p[1]

# # Assignment
# def p_assignment_statement(p):
#     '''assignment_statement : ID EQUALS expression SEMICOLON'''
#     p[0] = ('assignment', p[1], p[3])
#     print(f"Assigned {p[3]} to {p[1]}")

# # Function Definition
# def p_function_definition(p):
#     '''function_definition : DEF ID LPAREN parameters RPAREN COLON block_statement'''
#     function_name = p[2]
#     parameters = p[4]
#     body = p[8]
#     assign_symbol(function_name, (parameters, body))

# def p_parameters(p):
#     '''parameters : parameter_list
#                   | empty'''
#     p[0] = p[1]

# def p_parameter_list(p):
#     '''parameter_list : parameter_list COMMA ID
#                       | ID'''
#     p[0] = p[1] + [p[3]] if len(p) == 4 else [p[1]]

# # Function Call
# def p_function_call(p):
#     '''function_call : ID LPAREN argument_list RPAREN'''
#     p[0] = ('function_call', p[1], p[3])

# def p_argument_list(p):
#     '''argument_list : expression_list
#                      | empty'''
#     p[0] = p[1]

# # Return Statement
# def p_return_statement(p):
#     '''return_statement : RETURN expression SEMICOLON'''
#     p[0] = ('return', p[2])

# # If-Else Statement
# def p_if_statement(p):
#     '''if_statement : IF LPAREN expression RPAREN block_statement ELSE block_statement
#                     | IF LPAREN expression RPAREN block_statement'''
#     if len(p) == 8:  # if-else case
#         if p[3]:  # condition
#             execute_function(p[5])  # Execute the else block
#         else:
#             execute_function(p[7])
#     else:  # if case
#         if p[3]:
#             execute_function(p[5])  # Execute the block

# # While Loop
# def p_while_statement(p):
#     '''while_statement : WHILE LPAREN expression RPAREN block_statement'''
#     while p[3]:
#         execute_function(p[5])  # Execute block while the condition is true

# # For Loop (implementing basic structure)
# def p_for_statement(p):
#     '''for_statement : FOR LPAREN assignment_statement SEMICOLON expression SEMICOLON assignment_statement RPAREN block_statement'''
#     # Implement loop execution
#     # Unpacking loop statements (initialization, condition, increment)
#     p[0] = ('for', p[3], p[5], p[7], p[9])  # To be executed

# # Block Statement
# def p_block_statement(p):
#     '''block_statement : LBRACE statement_list RBRACE
#                        | empty'''  # Allow empty blocks
#     p[0] = p[2] if len(p) == 4 else []

# # Expression (with Operator Precedence)
# precedence = (
#     ('left', 'PLUS', 'MINUS'),
#     ('left', 'TIMES', 'DIVIDE'),
# )

# def p_expression_binop(p):
#     '''expression : expression PLUS expression
#                   | expression MINUS expression
#                   | expression TIMES expression
#                   | expression DIVIDE expression'''
#     if p[2] == '+':
#         p[0] = p[1] + p[3]
#     elif p[2] == '-':
#         p[0] = p[1] - p[3]
#     elif p[2] == '*':
#         p[0] = p[1] * p[3]
#     elif p[2] == '/':
#         p[0] = p[1] / p[3]

# # Grouping
# def p_expression_group(p):
#     '''expression : LPAREN expression RPAREN'''
#     p[0] = p[2]

# # Numbers and Strings
# def p_expression_number(p):
#     '''expression : NUMBER'''
#     p[0] = p[1]

# def p_expression_string(p):
#     '''expression : STRING'''
#     p[0] = p[1]

# # Variables
# def p_expression_id(p):
#     '''expression : ID'''
#     p[0] = lookup_symbol(p[1])
#     if p[0] is None:
#         print(f"Error: Undefined variable {p[1]}")

# def p_expression_list(p):
#     '''expression_list : expression
#                        | expression COMMA expression_list'''
#     p[0] = [p[1]] + p[3] if len(p) == 4 else [p[1]]

# def p_variable_declaration(p):
#     '''variable_declaration : TYPE ID EQUALS expression SEMICOLON
#                             | TYPE ID SEMICOLON'''
#     # Handle initialization and declaration
#     if len(p) == 5:
#         assign_symbol(p[2], p[4])
#     else:
#         assign_symbol(p[2], None)

# # Arrays
# def p_array_definition(p):
#     '''array_definition : ID EQUALS LBRACKET element_list RBRACKET SEMICOLON'''
#     assign_symbol(p[1], p[4])

# def p_element_list(p):
#     '''element_list : element_list COMMA expression
#                     | expression'''
#     p[0] = p[1] + [p[3]] if len(p) == 4 else [p[1]]

# def p_array_access(p):
#     '''array_access : ID LBRACKET expression RBRACKET'''
#     array = lookup_symbol(p[1])
#     index = p[3]
#     if isinstance(array, list):
#         if 0 <= index < len(array):
#             p[0] = array[index]
#         else:
#             print(f"Error: Index {index} out of bounds for array {p[1]}")
#     else:
#         print(f"Error: {p[1]} is not an array")

# # Classes and Object-Oriented Support
# def p_class_definition(p):
#     '''class_definition : CLASS ID LBRACE class_body RBRACE'''
#     assign_symbol(p[2], p[4])

# def p_class_body(p):
#     '''class_body : class_member class_body
#                   | empty'''  # Allow empty class bodies
#     p[0] = [p[1]] + p[2] if len(p) == 3 else []

# def p_class_member(p):
#     '''class_member : function_definition
#                     | variable_declaration'''
#     p[0] = p[1]

# def p_object_instantiation(p):
#     '''object_instantiation : NEW ID LPAREN RPAREN'''
#     class_name = p[2]
#     if class_name in get_current_scope():
#         p[0] = instantiate_object(class_name)
#     else:
#         print(f"Error: Class {class_name} is not defined")

# # Error Handling
# def p_error(p):
#     if p:
#         print(f"Syntax error at token {p.type}, value {p.value}, line {p.lineno}")
#         parser.errok()  # Recover from error
#     else:
#         print("Syntax error at EOF")

# # Empty Rule
# def p_empty(p):
#     'empty :'
#     pass

# # Build the parser
# parser = yacc.yacc()

# # Test the parser
# def test_parser():
#     test_code = """
#     x = 5;
#     y = 10;
#     sum = x + y;
#     print(sum);
#     """
#     parser.parse(test_code)

# if __name__ == "__main__":
#     test_parser()
import ply.yacc as yacc
from lexer import tokens, lexer  # Import tokens and lexer

# Symbol table as a stack for handling scope
symbol_stack = [{}]

def enter_new_scope():
    symbol_stack.append({})  # Push a new symbol table for a new scope

def exit_scope():
    symbol_stack.pop()  # Pop the symbol table when exiting the scope

def get_current_scope():
    return symbol_stack[-1]  # Get the current symbol table

def assign_symbol(name, value):
    current_scope = get_current_scope()
    current_scope[name] = value

def lookup_symbol(name):
    for scope in reversed(symbol_stack):
        if name in scope:
            return scope[name]
    return None

def type_check(operation, left_type, right_type):
    if operation in ('+', '-', '*', '/'):
        if left_type == right_type:
            return left_type  # Return the type of the operation
        else:
            print(f"Type Error: Cannot perform '{operation}' on {left_type} and {right_type}")
            return None
    return None  # Other operations can be handled as needed

# Empty rule
def p_empty(p):
    'empty :'
    pass

# Parsing rules
def p_program(p):
    '''program : statement_list'''
    p[0] = ('program', p[1])
    print("Program parsed successfully")

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    p[0] = p[1] + [p[2]] if len(p) == 3 else [p[1]]

def p_statement(p):
    '''statement : assignment_statement
                 | if_statement
                 | while_statement
                 | for_statement
                 | function_definition
                 | block_statement
                 | return_statement
                 | COMMENT
                 | NEWLINE'''
    p[0] = p[1]

# Assignment
def p_assignment_statement(p):
    '''assignment_statement : ID EQUALS expression SEMICOLON'''
    p[0] = ('assignment', p[1], p[3])
    print(f"Assigned {p[3]} to {p[1]}")

# Function Definition
def p_function_definition(p):
    '''function_definition : DEF ID LPAREN parameters RPAREN COLON block_statement'''
    function_name = p[2]
    parameters = p[4]
    body = p[8]
    assign_symbol(function_name, (parameters, body))

def p_parameters(p):
    '''parameters : parameter_list
                  | empty'''
    p[0] = p[1]

def p_parameter_list(p):
    '''parameter_list : parameter_list COMMA ID
                      | ID'''
    p[0] = p[1] + [p[3]] if len(p) == 4 else [p[1]]

# Function Call
def p_function_call(p):
    '''function_call : ID LPAREN argument_list RPAREN'''
    p[0] = ('function_call', p[1], p[3])

def p_argument_list(p):
    '''argument_list : expression_list
                     | empty'''
    p[0] = p[1]

# Return Statement
def p_return_statement(p):
    '''return_statement : RETURN expression SEMICOLON'''
    p[0] = ('return', p[2])

# If-Else Statement
def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN block_statement ELSE block_statement
                    | IF LPAREN expression RPAREN block_statement'''
    if len(p) == 8:  # if-else case
        if p[3]:  # condition
            execute_function(p[5])  # Execute the else block
        else:
            execute_function(p[7])
    else:  # if case
        if p[3]:
            execute_function(p[5])  # Execute the block

# While Loop
def p_while_statement(p):
    '''while_statement : WHILE LPAREN expression RPAREN block_statement'''
    while p[3]:
        execute_function(p[5])  # Execute block while the condition is true

# For Loop (implementing basic structure)
def p_for_statement(p):
    '''for_statement : FOR LPAREN assignment_statement SEMICOLON expression SEMICOLON assignment_statement RPAREN block_statement'''
    # Implement loop execution
    # Unpacking loop statements (initialization, condition, increment)
    p[0] = ('for', p[3], p[5], p[7], p[9])  # To be executed

# Block Statement
def p_block_statement(p):
    '''block_statement : LBRACE statement_list RBRACE
                       | empty'''  # Allow empty blocks
    p[0] = p[2] if len(p) == 4 else []

# Expression (with Operator Precedence)
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    left_type = p[1][1] if isinstance(p[1], tuple) else type(p[1]).__name__
    right_type = p[3][1] if isinstance(p[3], tuple) else type(p[3]).__name__
    p[0] = (type_check(p[2], left_type, right_type), left_type, right_type)  # Use the type checking function

# Grouping
def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

# Numbers and Strings
def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = (p[1], 'int')  # Store the value and its type

def p_expression_string(p):
    '''expression : STRING'''
    p[0] = (p[1], 'string')  # Store the value and its type

# Variables
def p_expression_id(p):
    '''expression : ID'''
    var_value = lookup_symbol(p[1])
    if var_value is None:
        print(f"Error: Undefined variable {p[1]}")
        p[0] = (None, 'undefined')  # Return undefined type
    else:
        p[0] = (var_value, type(var_value).__name__)  # Return variable value and its type

def p_expression_list(p):
    '''expression_list : expression
                       | expression COMMA expression_list'''
    p[0] = [p[1]] + p[3] if len(p) == 4 else [p[1]]

def p_variable_declaration(p):
    '''variable_declaration : TYPE ID EQUALS expression SEMICOLON
                            | TYPE ID SEMICOLON'''
    # Handle initialization and declaration
    if len(p) == 5:
        assign_symbol(p[2], p[4])
    else:
        assign_symbol(p[2], None)

# Arrays
def p_array_definition(p):
    '''array_definition : ID EQUALS LBRACKET element_list RBRACKET SEMICOLON'''
    assign_symbol(p[1], p[4])

def p_element_list(p):
    '''element_list : element_list COMMA expression
                    | expression'''
    p[0] = p[1] + [p[3]] if len(p) == 4 else [p[1]]

def p_array_access(p):
    '''array_access : ID LBRACKET expression RBRACKET'''
    p[0] = ('array_access', p[1], p[3])

# Classes and Object-Oriented Support
def p_class_definition(p):
    '''class_definition : CLASS ID LBRACE class_body RBRACE'''
    assign_symbol(p[2], p[4])  # Symbol table assignment

def p_class_body(p):
    '''class_body : class_member class_body
                  | empty'''  # Allow empty class bodies
    if len(p) == 3:
        p[0] = [p[1]] + p[2]  # Non-empty body
    else:
        p[0] = []  # Empty body

def p_class_member(p):
    '''class_member : function_definition
                    | variable_declaration'''
    p[0] = p[1]

# Error Handling
def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

# Build the parser
parser = yacc.yacc()

# Run the parser
def run_parser(data):
    result = parser.parse(data)
    return result

# Test with sample input
if __name__ == "__main__":
    sample_code = '''
    int a = 10;
    string b = "Hello";
    a = a + 20;
    print(a);
    '''
    run_parser(sample_code)
