--> Compiler: Translate entire program into machine code before execution. (eg: C, C++)

Input: Source code -> output: Executable file
ex: gcc program.c creates a.out

--> Interpreter: Executes program line-by-line without translation (eg: Python, Javascript)

input: source code -> Direct execution
ex: python script.py

-> What we are building: A Tree-Walking Interpreter - reads cource code, converts to AST, then walks the tree to execute.

the three Main Phases:
source code = "Let x=5" 
Lexer = [LET, IDENT, INT]
Tokens = [LET, IDENT, INT]
parser = LetNode
AST 
Interpreter = Object
Output = 5

--> Lexer Example:
-->Input code:
code = "fn fibonacci(n) { return n }"

--> after adding spaces:
code = "fn fibonacci ( n ) { return n }"

--> after split()
words = ['fn', 'fibonacci', '(', 'n', ')', '{', 'return', 'n', '}']

--> after tokenization
tokens = [
    ('FN', 'fn'),
    ('IDENT', 'fibonacci'),
    ('(', '('),
    ('IDENT', 'n'),
    (')', ')'),
    ('{', '{'),
    ('RETURN', 'return'),
    ('IDENT', 'n'),
    ('}', '}')
]

### AST Visual Representation
For code: "let result = fibonacci(10)"

AST Tree:
Let
  name = "result"
  expr = Call
     name = "fibonacci"
     arg = Number(10)

For Code = "return fibonacci(n - 1)"

AST Tree:
ReturnNode
   expr = Call
      name = "fibonacci"
      arg = BinOp
         left = Var("n")
         op = "-"
         right = Number(1)

### WorkFlow:
### Phase 1: Source Code Input
1. user provides source code as a string
2. code contains funtion deifinition and main program
3. code is stored in variable named 'code'

### Phase 2: Lexical Analysis (Tokenization)
1. tokenize() function receive source code string
2. Add space around all symbols (, ), {, }, +,-,<=, =, ,
3. split string by whitespace into list of words
4. initialize empty token list
5. iterat through each word in split list
6. if word is 'fn', append (FN, 'fn') to tokens
7. if word is 'if', append(IF, 'if') to tokens
8. if word is 'return', append(RETURN, 'return') to tokens
9. if word is 'let', append(LET, 'let') to tokens
10. if word is 'print', append(PRINT, 'print') to tokens
11. if word is digit, append(INIT, value) 
12. if word is operator or delimeter, append(word, word)
13. Otherwise, append(IDENT, word)
14. Return complete tokens list

### Phase 3: Parsing (AST(Abstract Syntax Tree) Construction)
1. parse() function receives token list
2. Initialize position counter i = 0
3. Initialize position functions dictionary
4. Initialize empty program list
5. Define inner function parse_expr() fr expressing parsing
6. while i < len(tokens), check current token type
7. if token is FN (function):
  --> Get function name at i+1
  --> get parameter at i+3
  --> Advance i by 6 to skip: FN, IDENT, LPAREN, IDENT, RPAREN, LBRACE
  --> Initialize empty body list
  --> while current token is not RBRACE:
    -> If token is IF:
      -> skip 'if'
      -> Parse condition with parse_expr()
      -> skip '{'
      -> If next token is RETURN:
        -> skip 'return'
        -> parse return expression
        -> Append IfNode(condition, ReturnNode(expression)) to body
      -> Skip '}'
  --> If token is RETURN:
    -> skip 'return'
    -> Parse return expression
    -> Append ReturnNode(expression) to body
  --> skip the closing '}'
  --> Store Function(name, param, body) in function dictionary
8. If token is LET (variable declaration):
   --> get variable name at i+1
   --> advance i by 3 to skip: LET, IDENT, ASSIGN
   --> Parse expression with parse_expr()
   --> Append Let(name, expression) to program list
9. IF token is PRINT:
    --> advance i by 1 skip PRINT
    --> Parse expression with parse_expr()
    Append Print(expression) to program list
10. Return functions dictionary and program list


### Phase 4: Expression Parsing (parse_expr inner function)
1. Check current token type
2. If token is INT:
    -> create number code with token value
    -> Increment i by 1
    -> Return number code
3. If token is IDENT:
 --> get identifier name
 --> check if next token is LPAREN (function call):
   -> increment i by 2 to skip IDENT and LPAREN
   -> Parse argument with parse_expr()
   -> increment i by 1 to skip RPAREN
   -> Return Call(name, argument)
 --> Else (variable reference):
   -> increment i by 1
   -> Return Var(name)

4. If token is LPAREN:
 --> Increment i by 1 to skip LPAREN
 --> Parse inner expression with parse_expr()
 --> increment i by 1 to skip RPAREN
 --> Return inner expression

5. Parse left operand with parse_expr()
6. Check if next token is operator (+, -, <=):
 --> store operator
 --> increment i by 1 to skip operator
 --> Parse right operant with parse_expr()
 --> Return BinOp(left, operator, right)

7. Return left operant (no operator)


### Phase 5: Interpretation (Tree Walking)
1. interpret() function receives functions dict and program list
2. Define inner function eval_expr(node, env):
 --> check node type:
3. If node is Number:
 --> return node value
4. If node is Var:
 --> Return env[node.name] (look up variable)
5. if node is BinOp:
 --> Evaluate left child: left_val = eval_expr(node.left, env)
 --> Evaluate right child: right_val = eval_expr(node.right, env)
 --> If operator is '+', return left_val + right_val
 --> If operatr is '-', return left_val - right_val
 --> If operator is '<=', return left_val <= 
 right value
6. If node is call:
 --> get function from functions dictionary: func = functions[node.name]
 --> Evaluate argument: arg_val = eval_expr(node.arg, env)
 --> create new environment: new_env = {func.param: arg_val}
 --> for each statement in func.body:
  -> if statement if IfNode:
    -> Evaluate condition: if eval_expr(stmt.cond, new_env):
       -> Evaluate and return stmt.body.expr
    -> If statement is ReturnNode:
       -> Evaluate and return stmt.expr

7. Initialize global environment: env = {}
8. For each statement in program:
  --> if statement is Let:
    -> evaluate expression: value = eval_expr(stmt.expr, env)
    -> Store in env: env[stmt.name] = value
  --> If statement is Print:
    -> Evaluate expression: result = eval_expr(stmt.expr, env)
    -> Print result


### Phase 6: Output Generation
1. Source code displayed with formatting
2. Tokens printed as list of tuples
3. AST built internally (not printed in this version)
4. Fibonacci calculation executed recursively
5. Result printed: "Fibonacci(10) = 55"


### Recursive Fibonacci Execution Trace
Call fibonacci(10)
 check: 10 <= 1? False
 compute: fibonacci(9) + fibonacci(8)

Call fibonacci(9)
 check: 9 <= 1? False
 compute: fibonacci(8) + fibonacci(7)

Call fibonacci(8)
 check: 8 <= 1? False
 compute: fibonacci(7) + fibonacci(6)

Call fibonacci(7)
 check: 7 <= 1? False
 compute: fibonacci(6) + fibonacci(5)

Call fibonacci(6)
 check: 6 <= 1? False
 compute: fibonacci(5) + fibonacci(4)

Call fibonacci(5)
 check: 5 <= 1?
 compute: fibonacci(4) + fibonacci(3)

Call fibonacci(4)
 check: 4 <= 1? False
 compute: fibonacci(3) + fibonacci(2)

Call fibonacci(3)
 check: 3 <= 1?
 compute: fibonacci(2) + fibonacci(1)

Call fibonacci(2)
 check: 2 <= 1? False
 compute: fibonacci(1) + fibonacci(0)

Call fiboncci(1)
 check: 1 <= 1? True
 Return: 1

Call fibonacci(0)
 check: 0 <= 1? True
 Return: 0

Return to fibonacci(2): 1 + 0 = 1

Call fibonacci(1)
 check: 1 <= 1? True
 Return: 1
Return to fibonacci(3): 1 + = 2

Call fibonacci(2)
 compute: fibonacci(1) + fibonacci(0) = 1 + 0 =1
 Return: 1
Return to fibonacci(4): 2 + 1 =3

Call fibonacci(3)
 compute: fibonacci(2) + fibonacci(1) = 1 + 1 = 2
 return: 2
Return to fibonacci(5): 3 + 2 = 5

Call fibonacci(4)
 compute: fibonacci(3) + fibonacci(2) = 2 + 1 = 3
 return: 3
Return to fibonacci(6): 5 + 3 = 8

Call fibonacci(5)
 compute: fibonacci(4) +  fibonacci(3) = 3 + 2 =5
 return: 5
Return to fibonacci(7): 8 + 5 = 13

Call fibonacci(6)
 compute: fibonacci(5) + fibonacci(4) = 5 + 3 =8
 return 8
Return to fibonacci(8): 13 + 8 = 21

Call fibonacci(7)
 compute: fibonacci(6) + fibonacci(5) = 8 + 5 =13
 return: 13
Return to fibonacci(9): 21 + 13 = 34

Call fibonacci(8)
 compute: fibonacci(7) + fibonacci(6) = 13 + 8=21
 return 21
Return to fibonacci(10): 34 + 21 = 55

Final result stored in variable 'result'
Print statement outputs: "Fibonacci(10) = 55"

Lexer - Converts text to tokens
Parser - converts tokens to AST
AST - Tree representation of code
Recursive Descent - Parser that calls itself recursively
Environment - stores variable values
Tree-walking - Recursively evaluating AST nodes
Scope - where variables are visible
Recursion - Function that calls itself