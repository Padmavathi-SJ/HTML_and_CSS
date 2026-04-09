# ====================================
# MINI LANGUAGE (FIBONACCI SUPPORT)
# ====================================

# Token types

FN = "FN"
IF = "IF"
RETURN = "RETURN"
LET = "LET"
PRINT = "PRINT"
IDENT = "IDENT"
INT = "INT"

PLUS = "+"
MINUS = "-"
LTE = "<="
LPAREN = "("
RPAREN = ")"
LBRACE = "{"
RBRACE = "}"
ASSIGN = "="
COMMA = ","


# LEXER (COMPLETELY REWRITTEN)
def tokenize(code):
    """converts source code string into a list of tokens.
    ex: "let x = 5" -> [('LET', 'let'), ('IDENT', 'X'), ('=', '='), ('INT', 5)]
    args: 
        code: String containing source code
    Returns:
        List of tuples: (token_type, token_value)
    """
    
    tokens = []
    i = 0
    length = len(code)
    
    while i < length:
        ch = code[i]
        
        # Skip whitespace
        if ch.isspace():
            i += 1
            continue
        
        # Single character tokens
        if ch == '(':
            tokens.append((LPAREN, ch))
            i += 1
            continue
        elif ch == ')':
            tokens.append((RPAREN, ch))
            i += 1
            continue
        elif ch == '{':
            tokens.append((LBRACE, ch))
            i += 1
            continue
        elif ch == '}':
            tokens.append((RBRACE, ch))
            i += 1
            continue
        elif ch == '+':
            tokens.append((PLUS, ch))
            i += 1
            continue
        elif ch == '-':
            tokens.append((MINUS, ch))
            i += 1
            continue
        elif ch == '=':
            tokens.append((ASSIGN, ch))
            i += 1
            continue
        elif ch == ',':
            tokens.append((COMMA, ch))
            i += 1
            continue
        
        # Two-character operators (check for <=)
        if ch == '<' and i + 1 < length and code[i+1] == '=':
            tokens.append((LTE, '<='))
            i += 2
            continue
        elif ch == '<':
            # Handle single < if needed, but we don't use it
            i += 1
            continue
        
        # Numbers
        if ch.isdigit():
            num = ''
            while i < length and code[i].isdigit():
                num += code[i]
                i += 1
            tokens.append((INT, int(num)))
            continue
        
        # Identifiers and keywords
        if ch.isalpha():
            word = ''
            while i < length and (code[i].isalpha() or code[i].isdigit()):
                word += code[i]
                i += 1
            
            # Check for keywords
            if word == 'fn':
                tokens.append((FN, word))
            elif word == 'if':
                tokens.append((IF, word))
            elif word == 'return':
                tokens.append((RETURN, word))
            elif word == 'let':
                tokens.append((LET, word))
            elif word == 'print':
                tokens.append((PRINT, word))
            else:
                tokens.append((IDENT, word))
            continue
        
        # If we get here, unknown character - skip it
        i += 1
    
    return tokens


# AST NODES (Abstract Syntax Tree)
# Each class represents a different construct in our language
# The AST represents the grammatical structure of the code

class Number:
    """represents a numeric literal"""
    def __init__(self, value):
        self.value = value      # The actual number (eg: 5)
    # ex: Number(10) in AST represents the number 10


class Var:
    """represents a variable reference like n, result, x"""
    def __init__(self, name):
        self.name = name        # variable name (eg: n)
    # ex: Var("n") in AST represents reading variable 'n'


class BinOp:
    """represents binary operations like left + right, n - 1"""
    def __init__(self, left, op, right):
        self.left = left        # left operand (Number, Var, or BinOp)
        self.op = op            # operator (eg: "+", "-", "<=")
        self.right = right      # right operand (Number, Var, or BinOp)
    # ex: BinOp(Var("n"), "-", Number(1)) represents "n - 1"


class IfNode:
    """represents if statement with condition and body"""
    def __init__(self, cond, body):
        self.cond = cond        # condition expression (BinOp)
        self.body = body        # Body statement (ReturnNode usually)
    # ex: IfNode(BinOp(...), ReturnNode(....)) represents "if n <= 1 { return n }"


class ReturnNode:
    """represents return statement that exits function with value"""
    def __init__(self, expr):
        self.expr = expr        # expression to return (Number, Var, BinOp, Call)
    # ex: ReturnNode(Var("n")) represents "return n"


class Function:
    """represents function declaration"""
    def __init__(self, name, param, body):
        self.name = name        # Function name (eg: "fibonacci")
        self.param = param      # Parameter (eg: "n")
        self.body = body        # List of statements in function body
    # ex: Function("fibonacci", "n", [IfNode(...), ReturnNode(...)])


class Call:
    """represents function call like fibonacci(10)"""
    def __init__(self, name, arg):
        self.name = name        # Function name to call (eg: "fibonacci")
        self.arg = arg          # Argument expression (Number, Var, etc.)
    # ex: Call("fibonacci", Number(10)) represents "fibonacci(10)"


class Let:
    """represents variable declaration like let result = fibonacci(10)"""
    def __init__(self, name, expr):
        self.name = name        # Variable name
        self.expr = expr        # Expression to assign
    # ex: Let("result", Call("fibonacci", Number(10)))


class Print:
    """represents print statement like print result"""
    def __init__(self, expr):
        self.expr = expr        # Expression to print
    # ex: Print(Var("result")) represents "print result"


# PARSER
def parse(tokens):
    """Converts token list into Abstract Syntax Tree (AST)
    uses recursive descent parsing - each grammar rule becomes a function
    Args:
        tokens: List of (token_type, token_value) from lexer
    Returns:
        functions: Dictionary mapping function names to Function objects
        program: List of statements (Let, Print) in main program
    """

    # Initialize position pointer (which token we're reading)
    i = 0
    functions = {}
    # store main program statements 
    program = []
    
    # Helper function to check current token
    def peek():
        if i < len(tokens):
            return tokens[i][0]
        return None
    
    # Helper function to consume current token
    def consume(expected=None):
        nonlocal i
        if i < len(tokens):
            if expected is None or tokens[i][0] == expected:
                i += 1
                return True
        return False
    
    # Inner function: Parse an expression (returns AST node)
    def parse_expr():
        nonlocal i
        return parse_comparison()
    
    def parse_comparison():
        nonlocal i
        left = parse_addition()
        
        while i < len(tokens) and tokens[i][0] in [LTE]:
            op = tokens[i][0]
            i += 1
            right = parse_addition()
            left = BinOp(left, op, right)
        
        return left
    
    def parse_addition():
        nonlocal i
        left = parse_term()
        
        while i < len(tokens) and tokens[i][0] in [PLUS, MINUS]:
            op = tokens[i][0]
            i += 1
            right = parse_term()
            left = BinOp(left, op, right)
        
        return left
    
    def parse_term():
        nonlocal i
        
        if i >= len(tokens):
            return None
        
        # Number literal
        if tokens[i][0] == INT:
            node = Number(tokens[i][1])
            i += 1
            return node
        
        # Identifier or function call
        elif tokens[i][0] == IDENT:
            name = tokens[i][1]
            i += 1
            
            # Function call
            if i < len(tokens) and tokens[i][0] == LPAREN:
                i += 1  # Skip '('
                arg = parse_expr()
                if i < len(tokens) and tokens[i][0] == RPAREN:
                    i += 1  # Skip ')'
                return Call(name, arg)
            
            return Var(name)
        
        # Parenthesized expression
        elif tokens[i][0] == LPAREN:
            i += 1
            node = parse_expr()
            if i < len(tokens) and tokens[i][0] == RPAREN:
                i += 1
            return node
        
        return None
    
    # Main parsing loop
    while i < len(tokens):
        t = tokens[i][0]
        
        # Function Declaration
        if t == FN:
            i += 1  # Skip 'fn'
            
            # Get function name
            if i >= len(tokens) or tokens[i][0] != IDENT:
                i += 1
                continue
            name = tokens[i][1]
            i += 1
            
            # Get parameters
            if i >= len(tokens) or tokens[i][0] != LPAREN:
                i += 1
                continue
            i += 1  # Skip '('
            
            if i >= len(tokens) or tokens[i][0] != IDENT:
                i += 1
                continue
            param = tokens[i][1]
            i += 1
            
            if i >= len(tokens) or tokens[i][0] != RPAREN:
                i += 1
                continue
            i += 1  # Skip ')'
            
            # Get function body
            if i >= len(tokens) or tokens[i][0] != LBRACE:
                i += 1
                continue
            i += 1  # Skip '{'
            
            body = []
            
            # Parse function body
            while i < len(tokens) and tokens[i][0] != RBRACE:
                if tokens[i][0] == IF:
                    i += 1  # Skip 'if'
                    cond = parse_comparison()
                    
                    if i < len(tokens) and tokens[i][0] == LBRACE:
                        i += 1  # Skip '{'
                    
                    if i < len(tokens) and tokens[i][0] == RETURN:
                        i += 1  # Skip 'return'
                        ret_expr = parse_expr()
                        body.append(IfNode(cond, ReturnNode(ret_expr)))
                    
                    if i < len(tokens) and tokens[i][0] == RBRACE:
                        i += 1  # Skip '}'
                
                elif tokens[i][0] == RETURN:
                    i += 1  # Skip 'return'
                    ret_expr = parse_expr()
                    body.append(ReturnNode(ret_expr))
                
                else:
                    i += 1
            
            if i < len(tokens) and tokens[i][0] == RBRACE:
                i += 1  # Skip '}'
            
            functions[name] = Function(name, param, body)
        
        # Variable Declaration
        elif t == LET:
            i += 1  # Skip 'let'
            
            if i >= len(tokens) or tokens[i][0] != IDENT:
                i += 1
                continue
            name = tokens[i][1]
            i += 1
            
            if i < len(tokens) and tokens[i][0] == ASSIGN:
                i += 1
            
            expr = parse_expr()
            program.append(Let(name, expr))
        
        # Print Statement
        elif t == PRINT:
            i += 1  # Skip 'print'
            expr = parse_expr()
            program.append(Print(expr))
        
        else:
            i += 1
    
    return functions, program


# INTERPRETER (FIXED FOR PROPER RECURSION)
def interpret(functions, program):
    """Tree-Walking interpreter: recursively evaluates nodes.
    Args:
        functions: Dictionary of Function objects
        program: List of top-level statements
    """

    # Inner function: Evaluates an expression node and return its value
    def eval_expr(node, env):
        """Recursively evaluates AST nodes.
        Args:
            node: AST node (Number, Var, BinOp, Call)
            env: Environment (dictionary of variable values)
        Returns:
            Evaluated value (int for numbers, bool for conditions)
        """
        
        # CASE 1: Number literal -> return the number
        if isinstance(node, Number):
            return node.value
        
        # CASE 2: Variable reference -> look up in environment
        elif isinstance(node, Var):
            if node.name in env:
                return env[node.name]
            return 0
        
        # CASE 3: Binary operation -> evaluate left and right, apply operator
        elif isinstance(node, BinOp):
            left_val = eval_expr(node.left, env)
            right_val = eval_expr(node.right, env)
            
            # Apply the operator
            if node.op == PLUS or node.op == "+":
                return left_val + right_val
            elif node.op == MINUS or node.op == "-":
                return left_val - right_val
            elif node.op == LTE or node.op == "<=":
                return 1 if left_val <= right_val else 0
        
        # CASE 4: Function call -> execute function with argument
        elif isinstance(node, Call):
            # Get the function definition
            if node.name not in functions:
                return 0
            
            func = functions[node.name]
            
            # Evaluate the argument
            arg_val = eval_expr(node.arg, env)
            
            # Create new environment for function call
            new_env = {func.param: arg_val}
            
            # Execute function body and return result
            result = None
            for stmt in func.body:
                if isinstance(stmt, IfNode):
                    # Evaluate condition
                    cond_val = eval_expr(stmt.cond, new_env)
                    if cond_val:
                        # Execute the return statement inside if
                        result = eval_expr(stmt.body.expr, new_env)
                        break
                elif isinstance(stmt, ReturnNode):
                    result = eval_expr(stmt.expr, new_env)
                    break
            
            return result if result is not None else 0
    
    # Global environment
    env = {}
    
    # Execute program
    for stmt in program:
        if isinstance(stmt, Let):
            env[stmt.name] = eval_expr(stmt.expr, env)
        elif isinstance(stmt, Print):
            result = eval_expr(stmt.expr, env)
            print(f"Fibonacci(10) = {result}")


# =======================
# MAIN EXECUTION
# =======================

# source code to execute
code = """
fn fibonacci(n) {
if n <= 1 { return n }
return fibonacci(n - 1) + fibonacci(n - 2)
}

let result = fibonacci(10)
print result
"""

# display source code
print("=== Source Code ===")
print(code)

# PHASE 1: Lexical Analysis (Tokenization)
tokens = tokenize(code)
print("\n=== Tokens ===")
for token in tokens:
    print(token)

# PHASE 2: Syntactic Analysis (Parsing)
functions, program = parse(tokens)
print(f"\n=== Functions Found: {len(functions)} ===")
for name in functions:
    print(f"  - {name}")

print(f"\n=== Program Statements: {len(program)} ===")

# PHASE 3: Semantic Analysis & Execution (Interpretation)
print("\n=== Output ===")
interpret(functions, program)