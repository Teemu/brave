import argparse
import sys

from ast import parse_code, InvalidSyntax


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    try:
        with open(args.filename) as fp:
            code = fp.read()
    except IOError:
        print "Reading file %r failed." % args.filename
        sys.exit(1)

    print code
    try:
        print parse_code(code)
    except InvalidSyntax, e:
        print e
        sys.exit(1)