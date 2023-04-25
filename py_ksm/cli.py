import argparse
import logging
import os
import sys

from py_ksm.acls import KsmAcls, LintError

logging.basicConfig(format='%(name)s:%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def is_valid_file(parser, arg):
    if not os.path.isfile(arg):
        parser.error('The file {} does not exist!'.format(arg))
    else:
        # File exists so return the filename
        return arg


def lint_cli():
    parser = argparse.ArgumentParser(
        prog='lint_cli',
        description='Lint csv file with Kafka ACL for KSM')
    parser.add_argument("filename",
                        help="Path to file with KSM ACLs", metavar="FILE",
                        type=lambda x: is_valid_file(parser, x))
    args = parser.parse_args()
    try:
        KsmAcls().load(args.filename, lint_only=True)
    except LintError as e:
        logger.error(f"{e}")
        logger.error(e.error)
        if e.detail is not None:
            logger.error(f"Error details:\n{e.detail}")
        return 1


if __name__ == '__main__':
    sys.exit(lint_cli())
