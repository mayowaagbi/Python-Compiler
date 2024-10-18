from lexer import tokens
import ply.yacc as yacc

# The ASTNode class
class ASTNode:
    def __init__(self, node_type, children=None, value=None):
        self.node_type = node_type
        self.children = children if children is not None else []
        self.value = value

    def __repr__(self):
        return f"ASTNode(type={self.node_type}, value={self.value})"

    def pretty_print(self, level=0):
        indent = '  ' * level  # Indentation based on the level of the node
        result = f"{indent}ASTNode(type={self.node_type}, value={self.value})\n"
        for child in self.children:
            result += child.pretty_print(level + 1)
        return result

    def generate_tac(self):
        """Generate TAC instructions for this AST node and its children."""
        raise NotImplementedError(f"TAC generation not implemented for node type {self.node_type}")

class ProgramNode(ASTNode):
    def __init__(self, children):
        super().__init__('program', children)

    def generate_tac(self):
        tac_code = []
        for statement in self.children:
            tac_code.extend(statement.generate_tac())
        return tac_code

class BlockNode(ASTNode):
    def __init__(self, children):
        super().__init__('block', children)

    def generate_tac(self):
        tac_code = []
        print(f"Generating TAC for block with {len(self.children)} statements.")
        for statement in self.children:
            tac_code.extend(statement.generate_tac())
        return tac_code

class AssignmentNode(ASTNode):
    def __init__(self, var_name, value):
        super().__init__('assignment', [IdentifierNode(var_name), value])

    def generate_tac(self):
        var_name = self.children[0].value
        value = self.children[1].generate_tac()[0]
        print(f"Generating TAC for assignment: {var_name} = {value}")
        return [f"{var_name} = {value}"]

class IfStatementNode(ASTNode):
    def __init__(self, condition, true_block, false_block=None):
        super().__init__('if_statement', [condition, true_block, false_block])

    def generate_tac(self):
        condition = self.children[0].generate_tac()[0]
        true_block = self.children[1]
        false_block = self.children[2] if self.children[2] is not None else None
        true_label = new_label()
        end_label = new_label()
        tac_code = [f"if {condition} goto {true_label}"]
        if false_block:
            false_label = new_label()
            tac_code.append(f"goto {false_label}")
            tac_code.append(f"{true_label}:")
            tac_code.extend(true_block.generate_tac())
            tac_code.append(f"goto {end_label}")
            tac_code.append(f"{false_label}:")
            tac_code.extend(false_block.generate_tac())
        else:
            tac_code.append(f"goto {end_label}")
            tac_code.append(f"{true_label}:")
            tac_code.extend(true_block.generate_tac())
        tac_code.append(f"{end_label}:")
        print("TAC for if-statement:")
        for line in tac_code:
            print(line)
        return tac_code

class NumberNode(ASTNode):
    def __init__(self, value):
        super().__init__('number', value=value)

    def generate_tac(self):
        print(f"Generating TAC for number: {self.value}")
        return [str(self.value)]

class IdentifierNode(ASTNode):
    def __init__(self, value):
        super().__init__('identifier', value=value)

    def generate_tac(self):
        print(f"Generating TAC for identifier: {self.value}")
        return [self.value]

class BinaryOpNode(ASTNode):
    def __init__(self, left, op, right):
        super().__init__('binary_op', [left, right], value=op)

    def generate_tac(self):
        left_result = self.children[0].generate_tac()[0]
        right_result = self.children[1].generate_tac()[0]
        temp_var = new_temp()
        print(f"Generating TAC for binary operation: {temp_var} = {left_result} {self.value} {right_result}")
        return [f"{temp_var} = {left_result} {self.value} {right_result}"]

class ComparisonNode(ASTNode):
    def __init__(self, left, op, right):
        super().__init__('comparison', [left, right], value=op)

    def generate_tac(self):
        left_result = self.children[0].generate_tac()[0]
        right_result = self.children[1].generate_tac()[0]
        temp_var = new_temp()
        print(f"Generating TAC for comparison: {temp_var} = {left_result} {self.value} {right_result}")
        return [f"{temp_var} = {left_result} {self.value} {right_result}"]

# TAC generation helpers
temp_counter = 0
label_counter = 0

def new_temp():
    global temp_counter
    temp_counter += 1
    print(f"Generated new temporary variable: t{temp_counter}")
    return f't{temp_counter}'

def new_label():
    global label_counter
    label_counter += 1
    print(f"Generated new label: L{label_counter}")
    return f"L{label_counter}"

# Parsing rules
def p_program(p):
    '''program : statement_list'''
    p[0] = ProgramNode(p[1])

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : assignment_statement
                 | if_statement'''
    p[0] = p[1]

def p_assignment_statement(p):
    '''assignment_statement : ID EQUALS expression SEMICOLON'''
    p[0] = AssignmentNode(p[1], p[3])

def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN block_statement
                    | IF LPAREN expression RPAREN block_statement ELSE block_statement'''
    if len(p) == 6:
        p[0] = IfStatementNode(p[3], p[5])
    else:
        p[0] = IfStatementNode(p[3], p[5], p[7])

def p_block_statement(p):
    '''block_statement : LBRACE statement_list RBRACE
                       | LBRACE RBRACE'''
    if len(p) == 4:  # Non-empty block
        p[0] = BlockNode(p[2])
    else:  # Empty block
        p[0] = BlockNode([])

def p_expression(p):
    '''expression : term
                  | expression PLUS term
                  | expression MINUS term
                  | comparison'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = BinaryOpNode(p[1], p[2], p[3])

def p_comparison(p):
    '''comparison : term GREATER term
                  | term LESS term
                  | term EQUAL_EQUAL term
                  | term NOT_EQUAL term
                  | term GREATER_EQUAL term
                  | term LESS_EQUAL term'''
    p[0] = ComparisonNode(p[1], p[2], p[3])

def p_term(p):
    '''term : factor
            | term TIMES factor
            | term DIVIDE factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = BinaryOpNode(p[1], p[2], p[3])

def p_factor(p):
    '''factor : NUMBER
              | ID
              | LPAREN expression RPAREN'''
    if len(p) == 2:
        if isinstance(p[1], int):
            p[0] = NumberNode(p[1])
        else:
            p[0] = IdentifierNode(p[1])
    else:
        p[0] = p[2]

def p_error(p):
    if p:
        print(f"Syntax error at token {p.type}, value {p.value}, line {p.lineno}")
        p[0] = ASTNode('error', value=f"Syntax error at token {p.type}, value {p.value}, line {p.lineno}")
    else:
        print("Syntax error at EOF")
        p[0] = ASTNode('error', value="Syntax error at EOF")

parser = yacc.yacc()
