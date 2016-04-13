#!/usr/bin/env python3

from argparse import ArgumentParser
from argparse import FileType

from tokenizer import Tokenizer

parser = ArgumentParser(description="Compile Kaleidoscope files.")
parser.add_argument('source', metavar='source', type=FileType('r'),
                    help="The input source file to compile.")
args = parser.parse_args()

tokenizer = Tokenizer(args.source)

for token in tokenizer:
    print(token, end=' ')
