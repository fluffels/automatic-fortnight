import logging
import tokenizer

logger = logging.getLogger('parser')

class Expression:
    pass


class Number(Expression):
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return "({})".format(self.token.value)


class Variable(Expression):
    def __init__(self, identifier):
        self.identifier = identifier

    def __str__(self):
        return "({})".format(self.identifier.identifier)


class BinaryExpression(Expression):
    def __init__(self, operator, lhs, rhs):
        self.operator = operator
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return "({} {} {})".format(self.lhs, self.operator, self.rhs)


class Call(Expression):
    def __init__(self, callee, argc):
        self.callee = callee
        self.args = argc


class FunctionPrototype:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __str__(self):
        return "fn {} ({})".format(
            self.name, ' '.join([arg.identifier for arg in self.args]))


class FunctionDefinition:
    def __init__(self, prototype, body):
        self.prototype = prototype
        self.body = body

    def __str__(self):
        return "definition of {}".format(self.prototype)


class Parser:
    def __init__(self, tokenizer):
        self.token = None
        self.tokenizer = tokenizer
        # Lower numbers indicate lower precedence.
        self.operator_precedence_map = {"<": 10, "+": 20, "-": 20, "*": 40}

    def _advance(self):
        self.token = next(self.tokenizer)

    def _error(self, message):
        logger.error("line {}, col {}: {}".format(
            self.tokenizer.current_line, self.tokenizer.current_col, message))

    def _get_operator_precedence(self, token):
        return self.operator_precedence_map.get(token, -1)

    def _parse_primary(self):
        try:
            if isinstance(self.token, tokenizer.Identifier):
                return self._parse_identifier()
            elif isinstance(self.token, tokenizer.Number):
                return self._parse_number()
            elif self.token == '(':
                return self._parse_paren_expression()
            else:
                self._error("unknown token '{}', expected expression"
                            .format(self.token))
                return None
        except StopIteration:
            return None

    def _parse_expression(self):
        """
        expression ::= primary binop rhs
                   ::= primary
        :return:
        """
        lhs = self._parse_primary()
        if lhs is None:
            return None
        return self._parse_binary_operator_rhs(lhs)

    def _parse_binary_operator_rhs(self, lhs, min_precedence=0):
        while True:
            token_precedence = self._get_operator_precedence(self.token)
            if token_precedence < min_precedence:
                return lhs
            operator = self.token
            self._advance()
            rhs = self._parse_primary()
            if rhs is None:
                return None
            next_precedence = self._get_operator_precedence(self.token)
            if token_precedence < next_precedence:
                rhs = self._parse_binary_operator_rhs(rhs, token_precedence + 1)
            lhs = BinaryExpression(operator, lhs, rhs)

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
                        self._error("Could not parse expression.")
                        return None
                    if self.token == ')':
                        break
                    if self.token != ',':
                        self._error("Expected ')', or ',' in argument list.")
                    self._advance()
            self._advance()  # Eat ')'.
            return Call(identifier, len(arguments))

    def _parse_number(self):
        result = Number(self.token)
        self._advance()
        return result

    def _parse_paren_expression(self):
        self._advance()  # Eat (
        result = self._parse_expression()
        if self.token != ')':
            self._error("Expected ')'")
            return None
        self._advance()
        return result

    def _parse_function_prototype(self):
        """
        prototype ::= identifier '(' identifier* ')'
        """
        if not isinstance(self.token, tokenizer.Identifier):
            self._error("expected function name in prototype")
            return None
        fn_name = self.token.identifier
        self._advance()
        if self.token != '(':
            self._error("expected '(' in function prototype")
            return None
        self._advance()
        arguments = []
        while isinstance(self.token, tokenizer.Identifier):
            arguments.append(self.token)
            self._advance()
        if self.token != ')':
            self._error("expected ')' in function prototype")
            return None
        self._advance()
        return FunctionPrototype(fn_name, arguments)

    def _parse_function_definition(self):
        """
        definition ::= 'def' prototype expression
        """
        self._advance()  # Eat 'def'.
        prototype = self._parse_function_prototype()
        if not prototype:
            return None
        expression = self._parse_expression()
        if not expression:
            return None
        return FunctionDefinition(prototype, expression)

    def _parse_extern(self):
        """
        external ::= 'extern' prototype
        """
        self._advance()  # Eat 'extern'.
        return self._parse_function_prototype()

    def _parse_top_level_expression(self):
        expression = self._parse_expression()
        if expression:
            prototype = FunctionPrototype('', [])
            return FunctionDefinition(prototype, expression)
        else:
            # Attempt to recover.
            self._advance()
            return None

    def parse(self):
        logger.debug("starting parser")
        # Initialize with first token.
        self._advance()
        ast = []
        while not isinstance(self.token, tokenizer.EOF):
            if self.token == '\n':
                self._advance()
            elif isinstance(self.token, tokenizer.Function):
                ast.append(self._parse_function_definition())
            elif isinstance(self.token, tokenizer.Identifier):
                ast.append(self._parse_identifier())
            elif isinstance(self.token, tokenizer.External):
                ast.append(self._parse_extern())
            elif isinstance(self.token, tokenizer.Comment):
                # Might want to do something with these later on, like Python
                # docstrings.
                pass
            else:
                ast.append(self._parse_top_level_expression())
        return ast
