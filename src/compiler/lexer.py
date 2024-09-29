import ply.lex as lex
tokens = (
    "NUMBER", "CHARACTER", "STRING", "ID", 
    "PLUS", "MINUS", "TIMES", "DIVIDE",
    "LPAREN", "RPAREN", "EQUALS", "GREATERTHAN", 
    "CLPAREN", "CRPAREN", "SEMI", 
    "IF", "WHILE", "FOR", "RETURN",
    "BOOLEAN", "TRUE", "FALSE", 
    "COMMENT", "NEWLINE", "OPERATOR"
)

# Regular expression rules for simple tokens
t_PLUS       = r'\+'
t_MINUS      = r'-'
t_TIMES      = r'\*'
t_DIVIDE     = r'/'
t_LPAREN     = r'\('
t_RPAREN     = r'\)'
t_EQUALS     = r'='
t_GREATERTHAN= r'>'
t_CLPAREN    = r'\{'
t_CRPAREN    = r'\}'
t_SEMI       = r';'
t_OPERATOR    = r'==|!=|<=|>=|&&|\|\|'  # Common operators


reserved = {
    'if': 'IF',
    'while': 'WHILE',
    'for': 'FOR',
    'return': 'RETURN',
}

def t_NUMBER(t):
    r'\d+'  # Matches one or more digits 
    t.value = int(t.value)  # Converts the string value (digits) into an integer
    return t  # Returns the modified token

def t_CHARACTER(t):
    r'\'.\''  # Matches a single character enclosed in single quotes
    t.value = t.value[1]  # Extract the character from quotes
    return t

def t_STRING(t):
    r'/"([^\\\"]|\\.)*\"'
    return t 

# Regular expression rule for identifier tokens (e.g., variable names)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Look up the token type in the reserved dictionary
    return t


# Track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignoring spaces and tabs
t_ignore = ' \t'

def t_COMMENT(t):
    r'//.*'
    t.lexer.lineno +=1 #increment lin number for each line in the comment
    pass #Ignore comments



# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)



# Build the lexer
lexer = lex.lex()

# Function to test the lexer
def test_lexer(data):
    lexer.input(data)  # Feed the input data to the lexer
    for token in lexer:
        print(token)  # Print each token

# Example testing
input_data = """
x = 10 + 20;
if (x > 15) {
    return x * 2;
}
// This is a comment
char c = 'a';
string str = "Hello, World!";
bool flag = true;
bool condition = false;
if (condition && flag) {
    return x;
}""" 

# Run the lexer 
if __name__ == "__main__":
    test_lexer(input_data)