#!/usr/bin/env python

import argparse
import unittest
import sys
from test_security_group import TestSecurityGroups
from test_encryption import TestEncryption
from test_logging_and_monitoring import TestLoggingAndMonitoring
from test_public_exposure import TestPublicExposure


test_to_class = {
    'encryption': TestEncryption,
    'logging_and_monitoring': TestLoggingAndMonitoring,
    'public_exposure': TestPublicExposure,
    'security_group': TestSecurityGroups
}


def run_test(args):
    # Generating list of tests to run
    if args.tests[0] == 'all':
        tests_to_run = [
            'encryption',
            'logging_and_monitoring',
            'public_exposure',
            'security_group']
    else:
        tests_to_run = args.tests[0].split(',')

    # Executing tests
    exit_status = True
    for test_type in tests_to_run:
        print('\n\nRunning {} Tests'.format(test_type))
        test = test_to_class[test_type]
        test.TERRAFORM_LOCATION = args.location[0]
        runner = unittest.TextTestRunner()
        itersuite = unittest.TestLoader().loadTestsFromTestCase(test)
        result = runner.run(itersuite)
        exit_status = exit_status and not result.wasSuccessful()
    sys.exit(exit_status)


def main(args=None):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-l',
        '--location',
        help='Location of terraform templates to scan',
        nargs=1
    )
    parser.add_argument(
        '-t',
        '--tests',
        help='''Comma separated list of test to run or "all" for all tests
(e.g. encryption,security_group) Valid values include:encription,
logging_and_monitoring, public_exposure, security_group''',
        nargs=1,
        default='all'
    )
    parser.set_defaults(func=run_test)

    args = parser.parse_args(args)
    args.func(args)


if __name__ == "__main__":
    main()