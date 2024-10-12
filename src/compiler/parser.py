import ply.yacc as yacc
from lexer import tokens

# The ASTNode class
class ASTNode:
    def __init__(self, node_type, children=None, value=None):
        self.node_type = node_type  # Type of node (like, 'assignment', 'if', 'expression')
        self.children = children or []  # Child nodes
        self.value = value  # Value for terminal nodes (constants or identifiers)
        
    def __repr__(self):
        return f"ASTNode(type={self.node_type}, value={self.value})"

    def pretty_print(self, level=0):
        indent = '  ' * level  # Indentation based on the level of the node
        result = f"{indent}ASTNode(type={self.node_type}, value={self.value})\n"
        for child in self.children:
            result += child.pretty_print(level + 1)
        return result

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

def execute_statement(statement):
    if isinstance(statement, ASTNode):
        statement_type = statement.node_type
        print(f"Executing statement: {statement}")  # Log the current statement
        
        if statement_type == 'assignment':
            var_name = statement.children[0].value
            value = statement.children[1].value
            print(f"Assigning value {value} to variable '{var_name}'")  # Debug assignment
            assign_symbol(var_name, value)

        elif statement_type == 'if_statement':
            condition = statement.children[0]
            then_block = statement.children[1]
            else_block = statement.children[2]
            condition_result = evaluate_expression(condition)
            if condition_result:
                execute_block(then_block.children)
            else:
                execute_block(else_block.children)

        elif statement_type == 'block':
            execute_block(statement.children)

        elif statement_type == 'function_call':
            function_name = statement.children[0].value
            arguments = [child.value for child in statement.children[1:]]
            print(f"Calling function '{function_name}' with arguments {arguments}")  # Debug function call
            function_def = lookup_symbol(function_name)
            if function_def:
                params, body = function_def
                # Create a new scope for function parameters
                new_scope = {param: arg for param, arg in zip(params, arguments)}
                symbol_stack.append(new_scope)
                execute_function(body)
                symbol_stack.pop()
            else:
                print(f"Error: Function '{function_name}' is not defined")

        elif statement_type == 'return':
            return_value = statement.children[0].value
            print(f"Returning value: {return_value}")  # Debug return statement
            return return_value
    else:
        print(f"Error: Statement is not an ASTNode: {statement}")  # Log if the statement is not an ASTNode

def execute_block(block):
    for statement in block:
        execute_statement(statement)

def evaluate_expression(expression):
    # This function should evaluate the expression and return the result
    # For simplicity, let's assume it returns True for now
    return True

def execute_function(body):
    for statement in body:
        execute_statement(statement)

def instantiate_object(class_name):
    class_def = lookup_symbol(class_name)
    if class_def:
        return class_def  # Create an instance here if needed
    print(f"Error: Class {class_name} is not defined")
    return None

# Parsing rules
def p_program(p):
    '''program : statement_list'''
    p[0] = ASTNode('program', p[1])

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : assignment_statement
                 | if_statement
                 | while_statement
                 | for_statement
                 | return_statement
                 | expression SEMICOLON'''
    p[0] = p[1]

def p_assignment_statement(p):
    '''assignment_statement : ID EQUALS expression SEMICOLON'''
    p[0] = ASTNode('assignment', [ASTNode('identifier', value=p[1]), p[3]])

def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN block_statement
                    | IF LPAREN expression RPAREN block_statement ELSE block_statement'''
    if len(p) == 6:
        p[0] = ASTNode('if_statement', [p[3], p[5], ASTNode('block', [])])
    else:
        p[0] = ASTNode('if_statement', [p[3], p[5], p[7]])

def p_while_statement(p):
    '''while_statement : WHILE LPAREN expression RPAREN block_statement'''
    p[0] = ASTNode('while', [p[3], p[5]])

def p_for_statement(p):
    '''for_statement : FOR LPAREN assignment_statement expression SEMICOLON assignment_statement RPAREN block_statement'''
    p[0] = ASTNode('for', [p[3], p[4], p[6], p[8]])

def p_return_statement(p):
    '''return_statement : RETURN expression SEMICOLON
                        | RETURN SEMICOLON'''
    if len(p) == 3:
        p[0] = ASTNode('return', [ASTNode('empty')])
    else:
        p[0] = ASTNode('return', [p[2]])

def p_block_statement(p):
    '''block_statement : LBRACE statement_list RBRACE
                       | LBRACE RBRACE'''
    p[0] = ASTNode('block', p[2] if len(p) == 3 else [])

def p_expression(p):
    '''expression : term
                  | expression PLUS term
                  | expression MINUS term
                  | comparison'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ASTNode('binary_op', [p[1], p[3]], p[2])

def p_comparison(p):
    '''comparison : term GREATER term
                  | term LESS term
                  | term EQUAL_EQUAL term
                  | term NOT_EQUAL term
                  | term GREATER_EQUAL term
                  | term LESS_EQUAL term'''
    p[0] = ASTNode('comparison', [p[1], p[3]], p[2])

def p_array_access(p):
    '''array_access : ID LBRACKET expression RBRACKET'''
    p[0] = ASTNode('array_access', value=p[1], children=[p[3]])  # Array name and index expression

def p_unary_expression(p):
    '''unary_expression : MINUS expression
                        | NOT expression'''
    p[0] = ASTNode('unary_op', value=p[1], children=[p[2]])  # Capture the operator and its operand

def p_function_definition(p):
    '''function_definition : DEF ID LPAREN parameter_list RPAREN block_statement'''
    p[0] = ASTNode('function_def', value=p[2], children=[p[4], p[6]])  # Function name, parameters, and block

def p_function_call(p):
    '''function_call : ID LPAREN argument_list RPAREN'''
    p[0] = ASTNode('function_call', value=p[1], children=p[3])  # Function name and argument list


def p_term(p):
    '''term : factor
            | term TIMES factor
            | term DIVIDE factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ASTNode('binary_op', [p[1], p[3]], p[2])

def p_factor(p):
    '''factor : NUMBER
              | ID
              | LPAREN expression RPAREN'''
    if len(p) == 2:
        if isinstance(p[1], int):
            p[0] = ASTNode('number', value=p[1])
        else:
            p[0] = ASTNode('identifier', value=p[1])
    else:
        p[0] = p[2]

def p_error(p):
    print(f"Syntax error at token {p.type}, value {p.value}, line {p.lineno}")

parser = yacc.yacc()
