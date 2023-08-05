# -*- coding: utf-8 -*-
"""
    Efesto blueprints script.

    This script will load / dump blueprints.
"""
import argparse
import os

from efesto.Blueprints import dump_blueprint, load_blueprint


def load(file_to_load, mode):
    path = os.path.join(os.getcwd(), file_to_load)
    if os.path.isfile(path):
        load_blueprint(path, mode=mode)
        print('Blueprint loaded successfully!')
    else:
        print('The provided path is not a file.')


def dump(dump_destination):
    path = os.path.join(os.getcwd(), dump_destination)
    dump_blueprint(path)
    print('Blueprint dumped successfully!')


def blueprints():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dump', dest='dump')
    parser.add_argument('--load', dest='load')
    parser.add_argument('--load-mode', dest='load_mode', default='default')
    args = parser.parse_args()
    if args.load:
        load(args.load, args.load_mode)

    if args.dump:
        dump(args.dump)
