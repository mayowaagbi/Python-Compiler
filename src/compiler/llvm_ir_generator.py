from llvmlite import ir
from parser import ASTNode, ProgramNode, BlockNode, AssignmentNode, IfStatementNode, NumberNode, IdentifierNode, BinaryOpNode, ComparisonNode

class LLVMGenerator:
    def __init__(self):
        # Initialize an LLVM module to contain functions and global variables
        self.module = ir.Module(name="main_module")
        # Builder will manage instructions within a function
        self.builder = None
        # Current function context in LLVM IR
        self.function = None
        # Dictionary to keep track of variable allocations in the current scope
        self.named_values = {}

    def generate_code(self, ast):
        # Define a main function as an entry point in the IR
        func_type = ir.FunctionType(ir.VoidType(), [])
        self.function = ir.Function(self.module, func_type, name="main")
        # Create a basic block named "entry" for the function
        block = self.function.append_basic_block(name="entry")
        # Start the builder at the entry block
        self.builder = ir.IRBuilder(block)

        # Recursively generate code from AST nodes
        self._generate_code_from_node(ast)
        
        # Complete function with a return statement for void type
        self.builder.ret_void()
        return str(self.module)

    def _generate_code_from_node(self, node):
        if isinstance(node, ProgramNode):
            # For a ProgramNode, process each child node in sequence
            for child in node.children:
                self._generate_code_from_node(child)

        elif isinstance(node, BlockNode):
            # For BlockNode, execute each statement in sequence
            for statement in node.children:
                self._generate_code_from_node(statement)

        elif isinstance(node, AssignmentNode):
            # Extract the variable name and value to assign
            var_name = node.children[0].value
            value = self._generate_code_from_node(node.children[1])
            # Allocate storage in memory for the variable
            var = self.builder.alloca(value.type, name=var_name)
            # Store the computed value in the allocated memory
            self.builder.store(value, var)
            # Register variable in the symbol table
            self.named_values[var_name] = var

        elif isinstance(node, IfStatementNode):
            # Evaluate the condition for the 'if' statement
            condition_val = self._generate_code_from_node(node.children[0])
            zero = ir.Constant(condition_val.type, 0)
            # Compare condition to zero to decide branching
            cond = self.builder.icmp_signed("!=", condition_val, zero)

            # Create basic blocks for then, else, and merge points
            then_block = self.function.append_basic_block(name="then")
            else_block = self.function.append_basic_block(name="else")
            merge_block = self.function.append_basic_block(name="ifcont")

            # Conditional branch based on evaluation result
            self.builder.cbranch(cond, then_block, else_block)

            # Generate code for the 'then' block
            self.builder.position_at_end(then_block)
            self._generate_code_from_node(node.children[1])
            self.builder.branch(merge_block)

            # Generate code for the 'else' block, if it exists
            self.builder.position_at_end(else_block)
            if len(node.children) > 2:
                self._generate_code_from_node(node.children[2])
            self.builder.branch(merge_block)

            # Re-position builder at the merge block for further code
            self.builder.position_at_end(merge_block)

        elif isinstance(node, BinaryOpNode):
            # Process left and right operands for binary operations
            left = self._generate_code_from_node(node.children[0])
            right = self._generate_code_from_node(node.children[1])
            # Perform the corresponding operation based on the node's operator
            if node.value == '+':
                return self.builder.add(left, right, name="addtmp")
            elif node.value == '-':
                return self.builder.sub(left, right, name="subtmp")
            elif node.value == '*':
                return self.builder.mul(left, right, name="multmp")
            elif node.value == '/':
                return self.builder.sdiv(left, right, name="divtmp")

        elif isinstance(node, ComparisonNode):
            # Process left and right operands for comparison operations
            left = self._generate_code_from_node(node.children[0])
            right = self._generate_code_from_node(node.children[1])
            # Perform the corresponding comparison based on the node's operator
            if node.value == '==':
                return self.builder.icmp_signed('==', left, right, name="eqtmp")
            elif node.value == '!=':
                return self.builder.icmp_signed('!=', left, right, name="netmp")
            elif node.value == '<':
                return self.builder.icmp_signed('<', left, right, name="lttmp")
            elif node.value == '<=':
                return self.builder.icmp_signed('<=', left, right, name="letmp")
            elif node.value == '>':
                return self.builder.icmp_signed('>', left, right, name="gttmp")
            elif node.value == '>=':
                return self.builder.icmp_signed('>=', left, right, name="getmp")

        elif isinstance(node, NumberNode):
            # Return constant integer for a NumberNode
            return ir.Constant(ir.IntType(32), node.value)

        elif isinstance(node, IdentifierNode):
            # Load variable from memory by name, raising an error if undefined
            var = self.named_values.get(node.value)
            if var is None:
                raise ValueError(f"Undefined variable: {node.value}")
            return self.builder.load(var, name=node.value)

        else:
            # Handle unexpected node types with an error
            raise TypeError(f"Unknown AST node type: {type(node)}")

# Usage Example:
# Assuming you have an AST instance named `ast_root`, you can generate LLVM code with:
# generator = LLVMGenerator()
# llvm_code = generator.generate_code(ast_root)
# print(llvm_code)
