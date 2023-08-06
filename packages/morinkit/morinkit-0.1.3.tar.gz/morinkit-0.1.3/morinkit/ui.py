"""
morinkit.ui
~~~~~~~~~~~

This module defines the CLI for calling various top-level functions.
"""

import sys
from argparse import ArgumentParser, FileType


def parse_args():
    """Parse command-line arguments.

    Returns:
        A dict containing the subcommand and all other positional and
        optional arguments.
    """
    # Initialize parser and subparsers
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='subcommand')

    # ensemble_vcf
    ensemble_vcf = subparsers.add_parser('ensemble_vcf')
    ensemble_vcf.add_argument('vcf_filenames', nargs='+', metavar='vcf_file')
    ensemble_vcf.add_argument('--output', '-o', type=FileType('w'), default=sys.stdout,
                              dest='output_file')
    ensemble_vcf.add_argument('--sorted', action='store_true', dest='is_sorted',
                              help='Are all input VCF files sorted in the same order? '
                              'N.B. If not sorted, the entire files are loaded into memory.')
    ensemble_vcf.add_argument('--min_support', type=float, default=0.5,
                              help='Minimum number of supporting methods (one method per input '
                              'VCF). If less than 1, minimum fraction of supporting methods.')

    # Parse arguments and return dict
    args = parser.parse_args()
    return vars(args)
