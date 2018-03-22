#!/usr/bin/env python

"""
amalgamate_tests.py

Generate an amalgamation of all json tests for VM testing provided by
github.com/ethereum/ethereum-test.
"""

import argparse
import gzip
import json
import os
import sys

def main(args):
    vmtests = '{}/VMTests'.format(args.tests)
    assert os.path.exists(vmtests)
    all_tests = []
    for root, dirs, files in os.walk(vmtests):
        if dirs: continue
        for name in files:
            path = os.path.join(root, name)
            test = json.load(open(path, 'r'))
            all_tests.append(test)

    if args.compress:
        handle = gzip.open("{}.gz".format(args.output), 'wt')
    else:
        handle = open(args.output, 'w')

    with handle as output:
        json.dump(all_tests, output, indent=2)
            
if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Collect Ethereum VM tests')
    parser.add_argument('tests', type=str, help='Root directory of ethereum tests repository')
    parser.add_argument('--output', '-o', type=str, default='output.json', help='Where to write the output file')
    parser.add_argument('--compress', '-z', action='store_true', help="GZip-compress the output")
    args = parser.parse_args()
    main(args)
