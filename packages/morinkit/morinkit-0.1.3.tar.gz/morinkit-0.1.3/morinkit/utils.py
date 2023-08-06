"""
morinkit.utils
~~~~~~~~~~~~~~

This module contains general-purpose utility functions.
"""

import sys
import logging


def config_logging():
    """Configure logging."""
    log_format = '%(asctime)s - %(levelname)s (%(module)s.%(funcName)s):  %(message)s'
    date_format = '%Y/%m/%d %H:%M:%S'  # 2010/12/12 13:46:36
    logging.basicConfig(format=log_format, level=logging.INFO,
                        datefmt=date_format, stream=sys.stderr)
