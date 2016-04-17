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

    def testCompoundExpression(self):
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

    def testParenExpression(self):
        tokens = iter(['(', Identifier('x'), '+', Identifier('y'), ')', '*',
                       Identifier('z'), EOF()])
        parser = Parser(tokens)
        parser._advance()
        expression = parser._parse_expression()
        self.assertIsInstance(expression, Expression)
        self.assertIsInstance(expression.lhs, Expression)
        self.assertEquals('*', expression.operator)
        self.assertIsInstance(expression.rhs, Variable)
        self.assertEquals(expression.rhs.identifier.identifier, 'z')

    def testComplexExpression(self):
        tokens = iter([Identifier('a'), '+', Identifier('b'), '+', '(',
                       Identifier('c'), '+', Identifier('d'), ')', '*',
                       Identifier('e'), '*', Identifier('f'), '+',
                       Identifier('g'), EOF()])
        parser = Parser(tokens)
        parser._advance()
        expression = parser._parse_expression()
        self.assertIsInstance(expression, Expression)
        self.assertEquals(expression.lhs.lhs.lhs.identifier.identifier, 'a')
        self.assertEquals(expression.lhs.lhs.operator, '+')
        self.assertEquals(expression.lhs.lhs.rhs.identifier.identifier, 'b')
        self.assertEquals(expression.lhs.operator, '+')
        self.assertEquals(expression.lhs.rhs.lhs.lhs.lhs.identifier.identifier, 'c')
        self.assertEquals(expression.lhs.rhs.lhs.lhs.operator, '+')
        self.assertEquals(expression.lhs.rhs.lhs.lhs.rhs.identifier.identifier, 'd')
        self.assertEquals(expression.lhs.rhs.lhs.operator, '*')
        self.assertEquals(expression.lhs.rhs.lhs.rhs.identifier.identifier, 'e')
        self.assertEquals(expression.lhs.rhs.rhs.identifier.identifier, 'f')
        self.assertEquals(expression.rhs.identifier.identifier, 'g')
