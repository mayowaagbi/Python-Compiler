class ASTNode:
    def __init__(self, node_type, value=None):
        self.type = node_type
        self.value = value
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def constant_fold(self):
        if self.type == "number":
            return self.value  # Return the value of number nodes
        
        if self.type in ("addition", "subtraction", "multiplication", "division"):
            left_value = self.children[0].constant_fold()
            right_value = self.children[1].constant_fold()
            
            # Perform constant folding if both children are constants
            if isinstance(left_value, (int, float)) and isinstance(right_value, (int, float)):
                if self.type == "addition":
                    return left_value + right_value
                elif self.type == "subtraction":
                    return left_value - right_value
                elif self.type == "multiplication":
                    return left_value * right_value
                elif self.type == "division":
                    return left_value / right_value

        # Return the current node if no folding was possible
        return self

def fold_constants(ast_node):
    if ast_node:
        for i in range(len(ast_node.children)):
            # Recursively fold constants in child nodes
            ast_node.children[i] = fold_constants(ast_node.children[i])
        # Apply constant folding at the current node
        return ast_node.constant_fold()

# Dead Code Elimination (separate from ASTNode)
def dead_code_elimination(tac_code):
    live_vars = set()
    live_instructions = []
    
    # Traverse TAC in reverse to track live variables
    for instruction in reversed(tac_code):
        if '=' in instruction:  # Look for assignments
            target_var = instruction.split('=')[0].strip()
            if target_var in live_vars:
                # Keep the instruction if target_var is live
                live_instructions.append(instruction)
                # Add any variables used on the right-hand side to live_vars
                rhs_vars = [var for var in instruction.split('=')[1].split() if var.isidentifier()]
                live_vars.update(rhs_vars)
            else:
                print(f"Eliminating dead code: {instruction}")
        else:
            # Keep control flow instructions (e.g., if, goto, labels)
            live_instructions.append(instruction)

            # For conditions, add the variables involved to live_vars
            if 'if' in instruction or 'goto' in instruction:
                condition_vars = [var for var in instruction.split() if var.isidentifier()]
                live_vars.update(condition_vars)

    # Return the reversed list of live instructions
    return list(reversed(live_instructions))
# Example function to parse and generate the AST
# def parse_expression():
#     # For demonstration purposes, manually constructing an AST
#     root = ASTNode("addition")
#     num1 = ASTNode("number", 5)
#     num2 = ASTNode("number", 3)
#     root.add_child(num1)
#     root.add_child(num2)
    
#     return root

# Example usage
# if __name__ == "__main__":
#     root_ast = parse_expression()  # Replace with your actual AST generation
#     folded_result = fold_constants(root_ast)
    
#     if isinstance(folded_result, (int, float)):
#         print("Folded result:", folded_result)
#     else:
#         print("No constant folding applied.")

#     # Example TAC for dead code elimination
#     tac_code = [
#         "x = 5",
#         "y = 10",
#         "z = x + y",
#         "a = 3",  # Dead code
#         "y = 0"
#     ]

#     optimized_tac = dead_code_elimination(tac_code)
#     print("\nOptimized TAC after Dead Code Elimination:")
#     print("\n".join(optimized_tac))
