#/usr/bin/env python

"""
evm_vm_tests.py

This runs the amalgamation of all json tests in VMTests provided 
by github.com/ethereum/ethereum-test.
"""

import argparse
import binascii
import gzip
import json
import sys

from manticore.platforms import evm
from manticore.core import state
from manticore.core.smtlib import Operators, ConstraintSet

def hex2bin(s):
    if s.startswith('0x'):
        s = s[2:]
    return binascii.unhexlify(s)

def hex2val(s):
    return int(s,0)

def run_test(test_desc):
    cs = ConstraintSet()
    world = evm.EVMWorld(cs)

    header = {
            'coinbase': hex2val(test_desc['env']['currentCoinbase']),
            'timestamp': hex2val(test_desc['env']['currentTimestamp']),
            'gaslimit': hex2val(test_desc['env']['currentGasLimit']),
            'difficulty': hex2val(test_desc['env']['currentDifficulty']),
            'number': hex2val(test_desc['env']['currentNumber']),
            }

    params = {
            'address': hex2val(test_desc['exec']['address']),
            'origin': hex2val(test_desc['exec']['origin']),
            'price': hex2val(test_desc['exec']['gasPrice']),
            'data': hex2bin(test_desc['exec']['data']),
            'code': hex2bin(test_desc['exec']['code']),
            'caller': hex2val(test_desc['exec']['caller']),
            'gas': hex2val(test_desc['exec']['gas']),
            'value': hex2val(test_desc['exec']['value']),
            'global_storage': world.storage,
        }

    for address, fields in test_desc['pre'].items():
        addr = hex2val(address)
        world.create_account(
                    address = addr,
                    balance = hex2val(fields['balance']),
                    code = hex2bin(fields['code']),
                    storage = fields['storage'], 
                )
        world.storage[addr]['nonce'] = hex2val(fields['nonce'])

    new_evm = evm.EVM(constraints=cs, header=header, **params)

    try:
        new_evm.execute()
    except evm.EVMException as e:
        print("Ignoring exceptional instructions for now.")
    except:
        print("Other exception")
    else:
        if 'post' not in test_desc:
            return

        for address, fields in test_desc['post'].items():
            addr = hex2val(address)

            if addr not in world.storage:
                print("Account not found! ({})".format(addr))
                continue

            print("balances: {} {}".format(hex2val(fields['balance']), world.get_balance(addr)))
            assert hex2val(fields['balance']) == world.get_balance(addr)
            print("code: {} {}".format(hex2bin(fields['code']), world.get_code(addr)))
            assert hex2bin(fields['code']) == world.get_code(addr)

            print(fields['storage'], world.get_storage_items(addr))
            print(world.storage[addr])



def main(args):
    json_path = args.json

    if json_path.endswith('.gz') or json_path.endswith('.gzip'):
        opener = gzip.open
    else:
        opener = open

    with opener(args.json, 'r') as tests:
        test_descs = json.load(tests)

        for test_desc in test_descs:
            for test, desc in test_desc.items():
                print("Running {}".format(test))
                run_test(desc)


if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Run the test amalgamation")
    parser.add_argument('json', help="The json file that stores all tests")
    args = parser.parse_args()

    main(args)
