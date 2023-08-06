#!/usr/bin/python
# -*- coding: utf-8 -*-

from .parse_settings import Parser
from .lineranges import change_line

import argparse
import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.ERROR)
logger = logging.getLogger(__name__)


def parse_cli():
    """Return dictionary with CLI options"""
    parser = argparse.ArgumentParser(
        description='Change in bulk lines in text files')
    parser.add_argument('-d', '--default', help='default new value when not specified in the configuration file')
    parser.add_argument('-o', '--out', help='write to this file')
    parser.add_argument('-b', '--begin', help='start counting from this value. Defaults to 1', default=1)
    parser.add_argument('-q', '--quiet', help="Don't print the output to STDOUT. Default to False", action="store_true",
                        default=False)
    parser.add_argument('input', help='the input file to modify')
    parser.add_argument('config', help='the configuration file with the list of line indices to modify')
    return parser.parse_args().__dict__


def read_values_file(filepath):
    """Return a list of lines contained in the file"""
    with open(filepath, 'rt') as f:
        return f.read().splitlines()


def write_out(lines):
    return "\n".join(lines)


def write_file(filepath, lines):
    with open(filepath, 'wt') as f:
        f.write(write_out(lines))


def main():
    config = parse_cli()
    new_values = read_values_file(config['input'])
    p = Parser()
    p.fromFile(config['config'])
    p.parse_all()
    for element in p.out_lines:
        if not element.value:
            if not config['default']:
                logger.error("You didn't specify a default value on the CLI and line number {} \n"
                             "in the configuration file doesn't have a new value set. Exiting."
                             .format(p.out_lines.index(element) + 1))
                sys.exit(1)
            element.value = config['default']
    for element in p.out_lines:
        change_line(new_values, element, count_from=config['begin'])
    if config['out']:
        write_file(config['out'], new_values)
    if not config['quiet']:
        print(write_out(new_values))
