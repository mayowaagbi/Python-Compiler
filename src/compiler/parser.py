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
        indent = '  ' * level
        result = f"{indent}ASTNode(type={self.node_type}, value={self.value})\n"
        for child in self.children:
            result += child.pretty_print(level + 1)
        return result

    def constant_folding(self):
        for i in range(len(self.children)):
            self.children[i] = self.children[i].constant_folding()
        
        if self.node_type == 'binary_op' and len(self.children) == 2:
            left = self.children[0]
            right = self.children[1]
            if isinstance(left, NumberNode) and isinstance(right, NumberNode):
                if self.value == '+':
                    return NumberNode(left.value + right.value)
                elif self.value == '-':
                    return NumberNode(left.value - right.value)
                elif self.value == '*':
                    return NumberNode(left.value * right.value)
                elif self.value == '/':
                    return NumberNode(left.value / right.value)
        
        return self

class ProgramNode(ASTNode):
    def __init__(self, children):
        super().__init__('program', children)

class BlockNode(ASTNode):
    def __init__(self, children):
        super().__init__('block', children)

    def constant_folding(self):
        for i, child in enumerate(self.children):
            self.children[i] = child.constant_folding()
        return self

class AssignmentNode(ASTNode):
    def __init__(self, var_name, value):
        super().__init__('assignment', [IdentifierNode(var_name), value])

    def constant_folding(self):
        self.children[1] = self.children[1].constant_folding()
        return self

class IfStatementNode(ASTNode):
    def __init__(self, condition, true_block, false_block=None):
        super().__init__('if_statement', [condition, true_block, false_block])

    def constant_folding(self):
        self.children[0] = self.children[0].constant_folding()
        self.children[1] = self.children[1].constant_folding()
        if self.children[2]:
            self.children[2] = self.children[2].constant_folding()
        return self

class NumberNode(ASTNode):
    def __init__(self, value):
        super().__init__('number', [])
        self.value = value

    def constant_folding(self):
        return self

class IdentifierNode(ASTNode):
    def __init__(self, value):
        super().__init__('identifier', value=value)

class BinaryOpNode(ASTNode):
    def __init__(self, left, op, right):
        super().__init__('binary_op', [left, right], value=op)

class ComparisonNode(ASTNode):
    def __init__(self, left, op, right):
        super().__init__('comparison', [left, right], value=op)

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
    if len(p) == 4:
        p[0] = BlockNode(p[2])
    else:
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

# from lexer import tokens
# import ply.yacc as yacc
# import llvmlite.ir as ir
# import llvmlite.binding as llvm

# # Setting up the LLVM module and builder
# llvm_module = ir.Module(name="my_module")
# llvm_builder = None
# llvm_function = None

# # The ASTNode class
# class ASTNode:
#     def __init__(self, node_type, children=None, value=None):
#         self.node_type = node_type
#         self.children = children if children is not None else []
#         self.value = value

#     def __repr__(self):
#         return f"ASTNode(type={self.node_type}, value={self.value})"

#     def pretty_print(self, level=0):
#         indent = '  ' * level
#         result = f"{indent}ASTNode(type={self.node_type}, value={self.value})\n"
#         for child in self.children:
#             result += child.pretty_print(level + 1)
#         return result
    
#     def constant_folding(self):
#         for i in range(len(self.children)):
#             self.children[i] = self.children[i].constant_folding()
        
#         if self.node_type == 'binary_op' and len(self.children) == 2:
#             left = self.children[0]
#             right = self.children[1]
#             if isinstance(left, NumberNode) and isinstance(right, NumberNode):
#                 if self.value == '+':
#                     return NumberNode(left.value + right.value)
#                 elif self.value == '-':
#                     return NumberNode(left.value - right.value)
#                 elif self.value == '*':
#                     return NumberNode(left.value * right.value)
#                 elif self.value == '/':
#                     return NumberNode(left.value / right.value)
        
#         return self
    
#     def llvm_ir(self):
#         raise NotImplementedError(f"LLVM IR generation not implemented for node type {self.node_type}")

# class ProgramNode(ASTNode):
#     def __init__(self, children):
#         super().__init__('program', children)

#     def llvm_ir(self):
#         for statement in self.children:
#             statement.llvm_ir()
#         return llvm_module

# class BlockNode(ASTNode):
#     def __init__(self, children):
#         super().__init__('block', children)

#     def llvm_ir(self):
#         for statement in self.children:
#             statement.llvm_ir()

#     def constant_folding(self):
#         for i, child in enumerate(self.children):
#             self.children[i] = child.constant_folding()
#         return self

# class AssignmentNode(ASTNode):
#     def __init__(self, var_name, value):
#         super().__init__('assignment', [IdentifierNode(var_name), value])

#     def llvm_ir(self):
#         var_name = self.children[0].value
#         value = self.children[1].llvm_ir()
#         ptr = llvm_builder.alloca(ir.IntType(32), name=var_name)
#         llvm_builder.store(value, ptr)

#     def constant_folding(self):
#         self.children[1] = self.children[1].constant_folding()
#         return self

# class IfStatementNode(ASTNode):
#     def __init__(self, condition, true_block, false_block=None):
#         super().__init__('if_statement', [condition, true_block, false_block])

#     def llvm_ir(self):
#         condition_value = self.children[0].llvm_ir()
#         true_block = self.children[1]
#         false_block = self.children[2]

#         with llvm_builder.if_then(condition_value):
#             true_block.llvm_ir()
#         if false_block:
#             with llvm_builder.else_then():
#                 false_block.llvm_ir()

#     def constant_folding(self):
#         self.children[0] = self.children[0].constant_folding()
#         self.children[1] = self.children[1].constant_folding()
#         if self.children[2]:
#             self.children[2] = self.children[2].constant_folding()
#         return self

# class NumberNode(ASTNode):
#     def __init__(self, value):
#         super().__init__('number', [])
#         self.value = value

#     def llvm_ir(self):
#         return ir.Constant(ir.IntType(32), self.value)

#     def constant_folding(self):
#         return self

# class IdentifierNode(ASTNode):
#     def __init__(self, value):
#         super().__init__('identifier', value=value)

#     def llvm_ir(self):
#         ptr = llvm_module.globals.get(self.value)
#         return llvm_builder.load(ptr, self.value)

# class BinaryOpNode(ASTNode):
#     def __init__(self, left, op, right):
#         super().__init__('binary_op', [left, right], value=op)

#     def llvm_ir(self):
#         left_value = self.children[0].llvm_ir()
#         right_value = self.children[1].llvm_ir()

#         if self.value == '+':
#             return llvm_builder.add(left_value, right_value, name="addtmp")
#         elif self.value == '-':
#             return llvm_builder.sub(left_value, right_value, name="subtmp")
#         elif self.value == '*':
#             return llvm_builder.mul(left_value, right_value, name="multmp")
#         elif self.value == '/':
#             return llvm_builder.sdiv(left_value, right_value, name="divtmp")

# class ComparisonNode(ASTNode):
#     def __init__(self, left, op, right):
#         super().__init__('comparison', [left, right], value=op)

#     def llvm_ir(self):
#         left_value = self.children[0].llvm_ir()
#         right_value = self.children[1].llvm_ir()

#         if self.value == '>':
#             return llvm_builder.icmp_signed('>', left_value, right_value, name="cmptmp")
#         elif self.value == '<':
#             return llvm_builder.icmp_signed('<', left_value, right_value, name="cmptmp")
#         elif self.value == '==':
#             return llvm_builder.icmp_signed('==', left_value, right_value, name="cmptmp")
#         elif self.value == '!=':
#             return llvm_builder.icmp_signed('!=', left_value, right_value, name="cmptmp")

# # Parsing rules
# def p_program(p):
#     '''program : statement_list'''
#     p[0] = ProgramNode(p[1])

# def p_statement_list(p):
#     '''statement_list : statement
#                       | statement_list statement'''
#     if len(p) == 2:
#         p[0] = [p[1]]
#     else:
#         p[0] = p[1] + [p[2]]

# def p_statement(p):
#     '''statement : assignment_statement
#                  | if_statement'''
#     p[0] = p[1]

# def p_assignment_statement(p):
#     '''assignment_statement : ID EQUALS expression SEMICOLON'''
#     p[0] = AssignmentNode(p[1], p[3])

# def p_if_statement(p):
#     '''if_statement : IF LPAREN expression RPAREN block_statement
#                     | IF LPAREN expression RPAREN block_statement ELSE block_statement'''
#     if len(p) == 6:
#         p[0] = IfStatementNode(p[3], p[5])
#     else:
#         p[0] = IfStatementNode(p[3], p[5], p[7])

# def p_block_statement(p):
#     '''block_statement : LBRACE statement_list RBRACE
#                        | LBRACE RBRACE'''
#     if len(p) == 4:
#         p[0] = BlockNode(p[2])
#     else:
#         p[0] = BlockNode([])

# def p_expression(p):
#     '''expression : term
#                   | expression PLUS term
#                   | expression MINUS term
#                   | comparison'''
#     if len(p) == 2:
#         p[0] = p[1]
#     else:
#         p[0] = BinaryOpNode(p[1], p[2], p[3])

# def p_comparison(p):
#     '''comparison : term GREATER term
#                   | term LESS term
#                   | term EQUAL_EQUAL term
#                   | term NOT_EQUAL term
#                   | term GREATER_EQUAL term
#                   | term LESS_EQUAL term'''
#     p[0] = ComparisonNode(p[1], p[2], p[3])

# def p_term(p):
#     '''term : factor
#             | term TIMES factor
#             | term DIVIDE factor'''
#     if len(p) == 2:
#         p[0] = p[1]
#     else:
#         p[0] = BinaryOpNode(p[1], p[2], p[3])

# def p_factor(p):
#     '''factor : NUMBER
#               | ID
#               | LPAREN expression RPAREN'''
#     if len(p) == 2:
#         if isinstance(p[1], int):
#             p[0] = NumberNode(p[1])
#         else:
#             p[0] = IdentifierNode(p[1])
#     else:
#         p[0] = p[2]

# def p_error(p):
#     if p:
#         print(f"Syntax error at token {p.type}, value {p.value}, line {p.lineno}")
#         p[0] = ASTNode('error', value=f"Syntax error at token {p.type}, value {p.value}, line {p.lineno}")
#     else:
#         print("Syntax error at EOF")
#         p[0] = ASTNode('error', value="Syntax error at EOF")

# parser = yacc.yacc()
