import logging
import tokenizer

logger = logging.getLogger('parser')

class Expression:
    pass


class Number(Expression):
    def __init__(self, token):
        self.token = token


class Variable(Expression):
    def __init__(self, identifier):
        self.identifier = identifier


class BinaryExpression(Expression):
    def __init__(self, operator, lhs, rhs):
        self.operation = operator
        self.lhs = lhs
        self.rhs = rhs


class Call(Expression):
    def __init__(self, callee, argc):
        self.callee = callee
        self.args = argc


class FunctionPrototype:
    def __init__(self, name, argc):
        self.name = name
        self.args = argc


class FunctionDefinition:
    def __init__(self, prototype, body):
        self.prototype = prototype
        self.body = body


class Parser:
    def __init__(self, tokenizer):
        self.token = None
        self.tokenizer = tokenizer

    def _advance(self):
        self.token = next(self.tokenizer)

    def _parse_expression(self):
        pass

    def _parse_identifier(self):
        """
        identifierexpr ::= identifier
                       ::= identifier '(' expression* ')'
        :return:
        """
        identifier = self.token
        self._advance()
        if self.token != '(':
            # Simple variable reference.
            return Variable(identifier)
        else:
            # Function call.
            self._advance()  # Eat (
            arguments = []
            if self.token != ')':
                while True:
                    argument = self._parse_expression()
                    if argument:
                        arguments.append(argument)
                    else:
                        logger.error("Could not parse expression.")
                        return None
                    if self.token == ')':
                        break
                    if self.token != ',':
                        logger.error("Expected ')', or ',' in argument list.")
                    self._advance()
            self._advance()  # Eat ')'.
            return Call(identifier, len(arguments))

    def _parse_number(self):
        result = Number(self.token)
        self._advance()
        return result

    def _parse_paren(self):
        self._advance()  # Eat (
        result = self._parse_expresion()
        if self.token != ')':
            logger.error("Expected ')'")
            return None
        self._advance()
        return result
