#include <iostream>

#include <fcntl.h>
#include <unistd.h>

#include "tokenizer.cpp"

using namespace std;

void print_usage(char* name) {
    cout << name << " <input-file>" << endl << endl;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        print_usage(argv[0]);
        return 1;
    }

    close(0);
    int handle = open(argv[1], O_RDONLY);
    if (handle == -1) {
        perror(argv[1]);
        return 2;
    }

    int token = tokenizer_next();
    while (token != token_eof) {
        cout << token << " ";
        token = tokenizer_next();
    }
    cout << endl;
    return 0;
}