#!/usr/bin/env python3

import logging
from logging import config

import settings

from argparse import ArgumentParser
from argparse import FileType

from parser import Parser
from tokenizer import Tokenizer

logging.config.dictConfig(settings.LOGGING)

parser = ArgumentParser(description="Compile Kaleidoscope files.")
parser.add_argument('source', metavar='source', type=FileType('r'),
                    help="The input source file to compile.")
args = parser.parse_args()

logging.info('Compiling "{}"'.format(args.source.name))

tokenizer = Tokenizer(args.source)
parser = Parser(tokenizer)
ir = parser.parse()

for item in ir:
    print(item, end=' ')
