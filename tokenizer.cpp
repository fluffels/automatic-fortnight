#include <string>

using namespace std;

enum Token {
    token_eof = -1,
    token_def = -2,
    token_extern = -3,
    token_identifier = -4,
    token_number = -5,
    token_comment = -6,
};

string identifier;
double value;
char last_char = ' ';

int tokenize_comment() {
    while ((last_char != EOF) && (last_char != '\n') && (last_char != '\r')) {
        last_char = getchar();
    }
    if (last_char != EOF) last_char = getchar();
    return token_comment;
}

int tokenize_identifier() {
    identifier = last_char;
    while (isalnum(last_char)) {
        identifier += last_char;
        last_char = getchar();
    }
    if (identifier == "def") return token_def;
    else if (identifier == "extern") return token_extern;
    else return token_identifier;
}

int tokenize_number() {
    string number;
    while (isdigit(last_char)) {
        number += last_char;
        last_char = getchar();
    }
    value = strtod(number.c_str(), 0);
    return token_number;
}

int tokenizer_eat_whitespace() {
    while (last_char == ' ') last_char = getchar();
}

int tokenizer_next() {
    tokenizer_eat_whitespace();
    if (last_char == '#') return tokenize_comment();
    if (isalpha(last_char)) return tokenize_identifier();
    if (isdigit(last_char) || last_char == '.') return tokenize_number();
    if (last_char == EOF) return token_eof;
    int result = last_char;
    last_char = getchar();
    return result;
}
