from unittest import TestCase
from parser import Parser
from parser import Expression
from parser import Variable
from tokenizer import EOF
from tokenizer import Identifier


class TestParser(TestCase):
    def testSimpleExpression(self):
        tokens = iter([Identifier('x'), '+', Identifier('y'), EOF()])
        parser = Parser(tokens)
        parser._advance()
        expression = parser._parse_expression()
        self.assertIsInstance(expression, Expression)
        self.assertIsInstance(expression.lhs, Variable)
        self.assertEquals(expression.lhs.identifier.identifier, 'x')
        self.assertIsInstance(expression.rhs, Variable)
        self.assertEquals(expression.rhs.identifier.identifier, 'y')
        self.assertEquals('+', expression.operator)

    def testComplexExpression(self):
        tokens = iter([Identifier('x'), '+', Identifier('y'), '*',
                       Identifier('z'), EOF()])
        parser = Parser(tokens)
        parser._advance()
        expression = parser._parse_expression()
        self.assertIsInstance(expression, Expression)
        self.assertIsInstance(expression.lhs, Variable)
        self.assertEquals(expression.lhs.identifier.identifier, 'x')
        self.assertEquals('+', expression.operator)
        self.assertIsInstance(expression.rhs, Expression)
        self.assertIsInstance(expression.rhs.lhs, Expression)
        self.assertEquals(expression.rhs.operator, '*')
        self.assertIsInstance(expression.rhs.rhs, Variable)
        self.assertEquals(expression.rhs.rhs.identifier.identifier, 'z')
