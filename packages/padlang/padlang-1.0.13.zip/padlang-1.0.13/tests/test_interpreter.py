import unittest

import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

class LexerTestCase(unittest.TestCase):
    def makeLexer(self, text):
        from pad.lexer import Lexer
        lexer = Lexer(text)
        return lexer

    def test_tokens(self):
        from pad.lexer import (
            INTEGER_CONST, REAL_CONST, MUL, INTEGER_DIV, FLOAT_DIV, PLUS, MINUS, LPAREN, RPAREN,
            ASSIGN, DOT, ID, SEMI, BEGIN, END
        )
        records = (
            ('234', INTEGER_CONST, 234),
            ('3.14', REAL_CONST, 3.14),
            ('*', MUL, '*'),
            ('DIV', INTEGER_DIV, 'DIV'),
            ('/', FLOAT_DIV, '/'),
            ('+', PLUS, '+'),
            ('-', MINUS, '-'),
            ('(', LPAREN, '('),
            (')', RPAREN, ')'),
            ('=', ASSIGN, ':='),
            ('.', DOT, '.'),
            ('number', ID, 'number'),
            (';', SEMI, ';'),
            ('BEGIN', BEGIN, 'BEGIN'),
            ('END', END, 'END'),
        )
        for text, tok_type, tok_val in records:
            lexer = self.makeLexer(text)
            token = lexer.get_next_token()
            self.assertEqual(token.type, tok_type)
            self.assertEqual(token.value, tok_val)


class InterpreterTestCase(unittest.TestCase):
    def makeInterpreter(self, text):
        from pad.interpreter import Interpreter
        from pad.lexer import Lexer
        from pad.parse import Parser
        lexer = Lexer(text)
        parser = Parser(lexer)
        tree = parser.parse()


        interpreter = Interpreter(tree)
        return interpreter

    def test_integer_arithmetic_expressions(self):
        for expr, result in (
            ('3', 3),
            ('2 + 7 * 4', 30),
            ('7 - 8 DIV 4', 5),
            ('14 + 2 * 3 - 6 DIV 2', 17),
            ('7 + 3 * (10 DIV (12 DIV (3 + 1) - 1))', 22),
            ('7 + 3 * (10 DIV (12 DIV (3 + 1) - 1)) DIV (2 + 3) - 5 - 3 + (8)', 10),
            ('7 + (((3 + 2)))', 12),
            ('- 3', -3),
            ('+ 3', 3),
            ('5 - - - + - 3', 8),
            ('5 - - - + - (3 + 4) - +2', 10),
        ):
            interpreter = self.makeInterpreter(
                """PROGRAM Test;
                   VAR
                       a;
                   BEGIN
                       a := %s
                   END.
                """ % expr
            )
            interpreter.interpret()
            globals = interpreter.GLOBAL_MEMORY
            self.assertEqual(globals['a'], result)

    def test_float_arithmetic_expressions(self):
        for expr, result in (
            ('3.14', 3.14),
            ('2.14 + 7 * 4', 30.14),
            ('7.14 - 8 / 4', 5.14),
        ):
            interpreter = self.makeInterpreter(
                """PROGRAM Test;
                   VAR
                       a;
                   BEGIN
                       a := %s
                   END.
                """ % expr
            )
            interpreter.interpret()
            globals = interpreter.GLOBAL_MEMORY
            self.assertEqual(globals['a'], result)

    def test_inline_variables(self):
        for expr, result in (
                ('42', 42),
                ('89', 89),
        ):
            interpreter = self.makeInterpreter(
                """PROGRAM Test;
                BEGIN
                    var a := %s;
                END.
                """ % expr
            )
            interpreter.interpret()
            globals = interpreter.GLOBAL_MEMORY
            self.assertEqual(globals['a'], result)

    def test_procedure_declaration(self):
        for expr, result in (
                ('42', 84),
                ('2 * 4', 16),
        ):
            interpreter = self.makeInterpreter(
                """PROGRAM Test;
                VAR
                    a;
                PROCEDURE MultiplyTwo(x);
                BEGIN
                    a := 2 * x;
                END;

                BEGIN
                    MultiplyTwo(%s);
                END.
                """ % expr
            )
            interpreter.interpret()
            globals = interpreter.GLOBAL_MEMORY
            self.assertEqual(globals['a'], result)

    def test_list_declaration_and_comprehension(self):
        for expr, result in (
                ('var l = [1, 2, 3, 4, 5];\n'
                 'a = l;', [1, 2, 3, 4, 5]),
                ('a = q[0];', 10),
                ('a = q[0,1];', [10, 20]),
                ('a = q[0,2,2];', [10, 30])
        ):
            interpreter = self.makeInterpreter(
                """PROGRAM Test;
                VAR
                    a;
                BEGIN
                    var q = [10, 20, 30, 40, 50, 60];
                    %s
                END.
                """ % expr
            )
            interpreter.interpret()
            globals = interpreter.GLOBAL_MEMORY
            self.assertEqual(globals['a'], result)

    def test_condition(self):
        for expr, result in (
                ('0', 1),
                ('2 * 2 + 1', 1),
                ('100 / 10', 0),
        ):
            interpreter = self.makeInterpreter(
                """PROGRAM Test;
                VAR
                    a, b;
                BEGIN
                    b = 5;
                    IF b >= (%s) {
                        a = 1;
                    } ELSE {
                        a = 0;
                    };
                END.
                """ % expr
            )
            interpreter.interpret()
            globals = interpreter.GLOBAL_MEMORY
            self.assertEqual(globals['a'], result)

    def test_function_declaration(self):
        for expr, result in (
                ('MultiplyTwo(2);', 4),
                ('MultiplyTwo(2) + MultiplyTwo(4) * (MultiplyTwo(4) + MultiplyTwo(2));', 100),
        ):
            interpreter = self.makeInterpreter(
                """PROGRAM Test;
                VAR
                    a;
                FUNCTION MultiplyTwo(x);
                BEGIN
                    RET 2 * x;
                END;

                BEGIN
                    a := %s
                END.
                """ % expr
            )
            interpreter.interpret()
            globals = interpreter.GLOBAL_MEMORY
            self.assertEqual(globals['a'], result)

    def test_expression_invalid_syntax_01(self):
        with self.assertRaises(Exception):
            self.makeInterpreter(
            """
            PROGRAM Test;
            VAR
                a;
            BEGIN
               a := 10 * ;  $Invalid syntax$
            END.
            """
            )

    def test_expression_invalid_syntax_02(self):
        with self.assertRaises(Exception):
            self.makeInterpreter(
            """
            PROGRAM Test;
            VAR
                a;
            BEGIN
               a := 1 (1 + 2); $Invalid syntax$
            END.
            """
            )

    def test_program(self):
        text = """\
PROGRAM Part11;
VAR
   number;
   a, b;
   y;

BEGIN $Part11$
   number := 2;
   a := number ;
   b := 10 * a + 10 * number DIV 4;
   y := 20 / 7 + 3.14
END.  $Part11$
"""
        interpreter = self.makeInterpreter(text)
        interpreter.interpret()

        globals = interpreter.GLOBAL_MEMORY
        self.assertEqual(len(globals.keys()), 4)
        self.assertEqual(globals['number'], 2)
        self.assertEqual(globals['a'], 2)
        self.assertEqual(globals['b'], 25)
        self.assertAlmostEqual(globals['y'], float(20) / 7 + 3.14)  # 5.9971...


if __name__ == '__main__':
    unittest.main()
