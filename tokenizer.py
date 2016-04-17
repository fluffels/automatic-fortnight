class Token:
    def __init__(self, string=''):
        self.string = string

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, self.string)


class Comment(Token): pass


class EOF(Token):
    def __str__(self):
        return 'EOF'


class Identifier(Token):
    def __init__(self, identifier):
        self.identifier = identifier

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, self.identifier)


class External(Token):
    def __init__(self):
        super(External, self).__init__("extern")


class Function(Token):
    def __init__(self):
        super(Function, self).__init__("def")


class Number(Token):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, self.value)


class Tokenizer:
    def __init__(self, source):
        self.last_char = ' '
        self.source = source
        self.token = Token()
        self.current_col = 0
        self.current_line = 0
        self.current_context = ''

    def __iter__(self):
        return self

    def __next__(self):
        if self.last_char is None:
            raise StopIteration()
        self._eat_white_space()
        if self.last_char == '#':
            return self._tokenize_comment()
        elif self.last_char.isalpha():
            return self._tokenize_identifier()
        elif self.last_char.isnumeric() or self.last_char == '.':
            return self._tokenize_number()
        elif not self.last_char:
            self.last_char = None
            return EOF()
        else:
            result = self.last_char
            self._advance()
            return result

    def _advance(self):
        self.last_char = self.source.read(1)
        if self.last_char in ['\n', '\r']:
            self.current_context += self.last_char
            self.current_col = 0
            self.current_line += 1
        else:
            self.current_col += 1
            self.current_context += self.last_char
        return self.last_char

    def _eat_white_space(self):
        while self.last_char and (self.last_char in [' ', '\t']):
            self._advance()

    def _tokenize_comment(self):
        while self.last_char and (self.last_char not in ['\n', '\r']):
            self._advance()
        return Comment()

    def _tokenize_identifier(self):
        str = ''
        while self.last_char.isalpha():
            str += self.last_char
            self._advance()
        if str == "def":
            return Function()
        elif str == "extern":
            return External()
        else:
            return Identifier(str)

    def _tokenize_number(self):
        number = ""
        while (self.last_char.isdigit()) or (self.last_char == '.'):
            number += self.last_char
            self._advance()
        value = float(number)
        return Number(value)
