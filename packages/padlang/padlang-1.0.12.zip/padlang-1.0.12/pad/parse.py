"""
  Copyright 2016 Dominik Madarasz
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
       http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################

from pad.ltypes import *


class AST(object):
    pass


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class Compound(AST):
    """Represents a 'BEGIN ... END' block"""

    def __init__(self):
        self.children = []


class Method(AST):
    def __init__(self, name, decl, code, method_type):
        self.name = name
        self.decl = decl
        self.code = code
        self.type = method_type


class MethodCall(AST):
    def __init__(self, name, args):
        self.name = name
        self.args = args


class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Condition(AST):
    def __init__(self, left, op, right, cons, alt):
        self.left = left
        self.token = self.op = op
        self.right = right
        self.cons = cons
        self.alt = alt


class Case(AST):
    def __init__(self, cond, cons):
        self.cond = cond
        self.cons = cons


class CaseSwitch(AST):
    def __init__(self, test, conds, alt):
        self.test = test
        self.conds = conds
        self.alt = alt


class VarDeclInline(AST):
    def __init__(self, decls):
        self.decls = decls


class Var(AST):
    """The Var node is constructed out of ID token."""

    def __init__(self, token):
        self.token = token
        self.value = token.value


class VarRef(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class NoOp(AST):
    pass


class Program(AST):
    def __init__(self, name, block):
        self.name = name
        self.block = block


class Block(AST):
    def __init__(self, declarations, methods, compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement
        self.methods = methods


class VarDecl(AST):
    def __init__(self, var_node, val_node=None):
        self.var_node = var_node
        self.val_node = val_node


class Type(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class String(AST):
    def __init__(self, text):
        self.text = text

class Parser(object):
    """
    Takes sequence of tokens from Lexical Analyzer (lexer) and constructs an AST (Abstract Syntax Tree).
    """
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax: ' + self.current_token.type)

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def program(self):
        """program : PROGRAM variable SEMI block DOT"""
        self.eat(PROGRAM)
        var_node = self.variable()
        prog_name = var_node.value
        self.eat(SEMI)
        block_node = self.block()
        program_node = Program(prog_name, block_node)
        self.eat(DOT)
        return program_node

    def block(self):
        """block : declarations (procedure | function)* compound_statement"""
        declaration_nodes = self.declarations()
        methods = []

        while self.current_token.type in (PROCEDURE, FUNCTION, FN, SUB):
            if self.current_token.type in (PROCEDURE, SUB):
                methods.append(self.procedure())
            elif self.current_token.type in (FUNCTION, FN):
                methods.append(self.function())

        compound_statement_node = self.compound_statement()
        node = Block(declaration_nodes, methods, compound_statement_node)
        return node

    def procedure(self):
        """
        procedure   : variable (LPAREN declarations RPAREN)* SEMI block
        """
        self.eat(PROCEDURE if self.current_token.type == PROCEDURE else SUB)
        name = self.variable().value
        decl = []

        if self.current_token.type == LPAREN:
            self.eat(LPAREN)
            decl = self.declarations()
            self.eat(RPAREN)

        self.eat(SEMI)
        block = self.block()
        node = Method(name, decl, block, PROCEDURE)

        if self.current_token.type == SEMI:
            self.eat(SEMI)

        return node

    def function(self):
        """
        function    : variable (LPAREN declarations RPAREN)* SEMI block
        """
        self.eat(FUNCTION if self.current_token.type == FUNCTION else FN)
        name = self.variable().value
        decl = []

        if self.current_token.type == LPAREN:
            self.eat(LPAREN)
            decl = self.declarations()
            self.eat(RPAREN)

        self.eat(SEMI)
        block = self.block()
        node = Method(name, decl, block, FUNCTION)

        if self.current_token.type == SEMI:
            self.eat(SEMI)

        return node

    def declarations(self):
        """declarations : VAR (variable_declaration SEMI)+
                        | empty
        """
        declarations = []

        if self.current_token.type == VAR:
            self.eat(VAR)

        while self.current_token.type in (ID, REF):
            var_decl = self.variable_declaration()
            declarations.extend(var_decl)

            if self.current_token.type == SEMI:
                self.eat(SEMI)

        return declarations

    def variable_declaration(self):
        """variable_declaration : ID (COMMA ID)* (ASSIGN expr)*"""
        var_nodes = [Var(self.current_token)]  # first ID
        self.eat(self.current_token.type)

        while self.current_token.type == COMMA:
            self.eat(COMMA)
            var_nodes.append(Var(self.current_token))
            self.eat(ID)

        value = None

        if self.current_token.type == ASSIGN:
            self.eat(ASSIGN)
            value = self.expr()

        var_declarations = [
            VarDecl(var_node, value)
            for var_node in var_nodes
            ]

        return var_declarations

    def type_spec(self):
        """type_spec : INTEGER
                     | REAL
        """
        token = self.current_token
        self.eat(token.type)
        node = Type(token)
        return node

    def compound_statement(self):
        """
        compound_statement: BEGIN statement_list END
        """
        self.eat(BEGIN)
        nodes = self.statement_list()

        self.eat(END)

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root

    def statement_list(self):
        """
        statement_list : statement (SEMI)
                       | statement SEMI statement_list
        """
        node = self.statement()

        results = [node]

        while self.current_token.type == SEMI:
            self.eat(SEMI)
            if self.current_token.type == END:
                break
            results.append(self.statement())

        return results

    def statement(self):
        """
        statement : compound_statement
                  | assignment_statement
                  | condition_statement
                  | case_statement
                  | variable_declaration
                  | expr
                  | empty
        """
        if self.current_token.type == BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == ID:
            node = self.assignment_statement()
        elif self.current_token.type == IF:
            node = self.condition_statement()
        elif self.current_token.type == RET:
            self.eat(RET)
            node = self.expr()
        elif self.current_token.type == VAR:
            self.eat(VAR)
            node = VarDeclInline(self.variable_declaration())
        elif self.current_token.type == CASE:
            node = self.case_statement()
        else:
            node = self.empty()
        return node

    def call_statement(self, name):
        """
        call_statement  : variable LPAREN arguments RPAREN
        """
        self.eat(LPAREN)
        args = self.arguments()
        self.eat(RPAREN)
        node = MethodCall(name, args)
        return node

    def arguments(self):
        """
        arguments   : (factor COMMA)+
        """
        if self.current_token.type == RPAREN:
            return None

        arg = self.expr()
        args = [arg]

        while self.current_token.type == COMMA:
            self.eat(COMMA)
            args.append(self.expr())

        return args

    def assignment_statement(self):
        """
        assignment_statement    : variable ASSIGN (expr | call_statement)
                                | call_statement
        """
        left = self.variable()

        if self.current_token.type == LPAREN:
            return self.call_statement(left)

        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()

        node = Assign(left, token, right)
        return node

    def case_statement(self):
        """
        case_statement : CASE variable OF case_list
        """
        self.eat(CASE)
        var = self.variable()

        if self.current_token.type == OF:
            self.eat(OF)

        conds = self.case_list()
        alt = self.empty()
        if self.current_token.type == ELSE:
            self.eat(ELSE)
            alt = self.statement()
            self.eat(SEMI)
        self.eat(END)
        node = CaseSwitch(var, conds, alt)
        return node

    def case_list(self):
        """
        case_list   : case (SEMI)
                    | case SEMI case_list
        """
        self.eat(BEGIN)
        node = self.case()

        results = [node]

        while self.current_token.type == SEMI:
            self.eat(SEMI)
            if self.current_token.type in (END, ELSE):
                break
            results.append(self.case())

        return results

    def case(self):
        """
        case    : factor (COMMA factor)+ COLON statement
        """
        cond = self.factor()
        conds = [cond]

        while self.current_token.type == COMMA:
            self.eat(COMMA)
            conds.append(self.factor())

        self.eat(COLON)
        cons = self.statement()

        node = Case(conds, cons)
        return node

    def condition_statement(self):
        """
        condition_statement : IF condition (THEN) statement ((ELSE condition_statement) | (ELSE statement))
        """
        self.eat(IF)
        left = self.expr()
        op = None
        if self.current_token.type in (EQUALS, LESSER, GREATER, NOT_EQUALS, GREATER_EQUALS, LESSER_EQUALS):
            op = self.current_token
            self.eat(op.type)
        else:
            self.error()
        right = self.expr()

        if self.current_token.type == THEN:
            self.eat(THEN)
        cons = self.statement()
        if self.current_token.type == ELSE:
            self.eat(ELSE)
            alt = self.statement()
        else:
            alt = self.empty()
        node = Condition(left, op, right, cons, alt)
        return node

    def variable(self):
        """
        variable : ID
        """
        node = Var(self.current_token)

        self.eat(ID)
        return node

    @staticmethod
    def empty():
        """An empty production"""
        return NoOp()

    def expr(self):
        """
        expr : term ((PLUS | MINUS) term)*
        """
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            self.eat(token.type)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def term(self):
        """term : factor ((MUL | INTEGER_DIV | INTEGER_MOD | FLOAT_DIV) factor)*"""
        node = self.factor()

        while self.current_token.type in (MUL, INTEGER_DIV, INTEGER_MOD, FLOAT_DIV):
            token = self.current_token
            self.eat(token.type)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def factor(self):
        """factor : PLUS factor
                  | MINUS factor
                  | INTEGER_CONST
                  | REAL_CONST
                  | LPAREN expr RPAREN
                  | string
                  | variable
                  | reference
                  | call_statement
        """
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == INTEGER_CONST:
            self.eat(INTEGER_CONST)
            return Num(token)
        elif token.type == REAL_CONST:
            self.eat(REAL_CONST)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif token.type == STRING:
            node = self.string()
            return node
        elif token.type == REF:
            node = self.reference()
            return node
        else:
            node = self.variable()
            if self.current_token.type == LPAREN:
                return self.call_statement(node)
            return node

    def string(self):
        node = String(self.current_token.value)
        self.eat(STRING)
        return node

    def reference(self):
        """
        reference   : REF
        """
        node = VarRef(Var(self.current_token))
        self.eat(REF)
        return node

    def parse(self):
        node = self.program()
        if self.current_token.type != EOF:
            self.error()

        return node
