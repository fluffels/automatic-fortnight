using namespace std;

class expression {
public:
    virtual ~expression() {}
};

class expression_binary: public expression {
public:
    char op;
    unique_ptr<expression> lhs;
    unique_ptr<expression> rhs;
    expression_binary(char some_op, unique_ptr<expression> some_lhs,
                      unique_ptr<expression> some_rhs):
            lhs(move(some_lhs)), rhs(move(some_rhs)), op(some_op) {}
};

class call: public expression {
public:
    string callee;
    vector<unique_ptr<expression>> args;
};

class number: public expression {
public:
    number(double some_value): value(some_value) {}
    double value;
};

class variable: public expression {
public:
    variable(string &some_name): name(some_name) {}
    string name;
};