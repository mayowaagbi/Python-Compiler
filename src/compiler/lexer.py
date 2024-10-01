import re
import keyword
import ply.lex as lex
from PyQt5.Qsci import QsciLexerCustom, QsciScintilla
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow

# Step 1: Create your lexer with PLY
tokens = (
    "NUMBER", "STRING", "ID", 
    "PLUS", "MINUS", "TIMES", "DIVIDE",
    "LPAREN", "RPAREN", "EQUALS", 
    "GREATER", "COLON", 
    "SEMICOLON", "LBRACE", "RBRACE",  
    "COMMENT", "NEWLINE", "OPERATOR", 
    "TRUE", "FALSE"  ,"KEYWORD"  
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUALS = r'='
t_GREATER = r'>'
t_COLON = r':'
t_SEMICOLON = r';'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_OPERATOR = r'==|!=|<=|>=|&&|\|\|'  

# Identifier or reserved word (e.g., if, while)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in keyword.kwlist:
        t.type = 'KEYWORD'  # Classify as keyword
    elif t.value == "true":
        t.type = "TRUE"  # Classify as boolean true
    elif t.value == "false":
        t.type = "FALSE"  # Classify as boolean false
    return t

# Number (e.g., 123)
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# String (e.g., "hello")
def t_STRING(t):
    r'\"([^\\\"]|\\.)*\"'
    return t

# Comment (e.g., // comment)
def t_COMMENT(t):
    r'//.*'
    pass  # Ignore comments

# Newline
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignore spaces and tabs
t_ignore = ' \t'

# Error handling
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Step 2: Build the PLY lexer
lexer = lex.lex()

# Step 3: Create your PyQt5 custom lexer (QsciLexer)
class CombinedLexer(QsciLexerCustom):
    """Custom lexer integrating PLY and Qsci"""
    
    def __init__(self, editor):
        super(CombinedLexer, self).__init__(editor)
        self.editor = editor
        self.setDefaultColor(QColor("#FFFFFF"))
        self.setDefaultPaper(QColor("#282c34"))
        self.setDefaultFont(QFont("Consolas", 14))

        # Token to style mappings
        self.TOKENS_MAP = {
            "KEYWORD": self.KEYWORD,
            "NUMBER": self.NUMBER,
            "STRING": self.STRING,
            "COMMENT": self.COMMENT,
            "ID": self.DEFAULT
        }
        
        self.keywords_list = keyword.kwlist

    # Style definitions
    DEFAULT = 0
    KEYWORD = 1
    STRING = 2
    COMMENT = 3
    NUMBER = 4
    
    def styleText(self, start, end):
        self.startStyling(start)
        text = self.editor.text()[start:end]
        
        # Tokenize using PLY lexer
        lexer.input(text)
        while True:
            tok = lexer.token()
            if not tok:
                break
            
            tok_type = tok.type
            tok_value = tok.value
            
            # Determine the length based on the type of token value
            if isinstance(tok_value, str):
                tok_len = len(tok_value)
            else:
                # If it's not a string, set tok_len to 1 for single character tokens
                tok_len = 1
            
            # Apply styling based on token type
            style = self.TOKENS_MAP.get(tok_type, self.DEFAULT)
            self.setStyling(tok_len, style)
            
            # Print token type and value for analysis
            print(f'Type: {tok.type}, Value: {tok.value}')
        
    def description(self, style):
        if style == self.DEFAULT:
            return "Default"
        elif style == self.KEYWORD:
            return "Keyword"
        elif style == self.STRING:
            return "String"
        elif style == self.COMMENT:
            return "Comment"
        elif style == self.NUMBER:
            return "Number"
        return ""

# Step 4: Use the combined lexer in your PyQt5 editor
class CodeEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.editor = QsciScintilla()
        self.setCentralWidget(self.editor)
        self.lexer = CombinedLexer(self.editor)
        self.editor.setLexer(self.lexer)
        self.editor.setText("""\
x = 42
if x > 10:
    print("Greater than 10")  // This is a comment
""")
        self.setWindowTitle("Lexer Test")
        self.resize(800, 600)
        self.show()

if __name__ == "__main__":
    app = QApplication([])
    window = CodeEditor()
    app.exec_()
