"""
morinkit.vcf
~~~~~~~~~~~~

This module contains utility functions relevant to VCF files.
"""

from collections import defaultdict, OrderedDict
from cyvcf2 import VCF
from cyvcf2.cyvcf2 import INFO as cyvcf2_INFO


def iter_vcfs(vcf_filenames, is_sorted=False):
    """Load VCF files and return an iterator for each variant.

    Args:
        vcf_files: List of VCF file paths.
        is_sorted: Boolean indicating whether the VCF files are sorted by
            chrom, pos, ref and alt.

    Returns:
        Iterator that yields a list of VCF records for each variant in the
        same order as the `vcf_files` argument.
    """
    vcf_readers = [VCF(vcf) for vcf in vcf_filenames]
    if is_sorted:
        iterator = create_vcf_walktogether(vcf_readers)
    else:
        iterator = create_vcf_iterator(vcf_readers)
    return iterator


def get_key(vcf_record):
    """Get unique variant key for a VCF record.

    Args:
        vcf_record: cyvcf2 VCF record.

    Returns:
        Tuple of VCF attributes or None if no ALT alleles are specified.
    """
    if len(vcf_record.ALT) == 0:
        return None
    return (vcf_record.CHROM, vcf_record.POS, vcf_record.REF, vcf_record.ALT[0])


def create_vcf_iterator(vcf_readers):
    """Create a VcfIterator for sorted and unsorted VCF files.

    This function loads entire files into memory.

    Args:
        vcf_readers: List of cyvcf2 VCF readers.

    Yields:
        List of VCF records with the same length as the number of input VCF
        readers. Yields one list per variant.
    """
    index = defaultdict(lambda: [None] * len(vcf_readers))
    for i, vcf in enumerate(vcf_readers):
        for record in vcf:
            key = get_key(record)
            if key is None:
                continue
            index[key][i] = record
    for key, val in index.items():
        yield val


def create_vcf_walktogether(vcf_readers):
    """Create a VCF iterator that efficiently handles sorted VCF files.

    Behaviour on unsorted files is undefined. Adapted from PyVCF walk_together:
    https://github.com/jamescasbon/PyVCF/blob/master/vcf/utils.py

    Args:
        vcf_readers: List of cyvcf2 VCF readers

    Yields:
        List of VCF records with the same length as the number of input VCF
        readers. Yields one list per variant.
    """
    def next_record(vcf_reader):
        try:
            next_record = next(vcf_reader)
        except StopIteration:
            next_record = None
        finally:
            return next_record

    nexts = []
    for vcf in vcf_readers:
        nexts.append(next_record(vcf))

    min_k = (None,)   #
    while any([r is not None for r in nexts]):

        next_idx_to_k = {}
        for i, record in enumerate(nexts):
            if record is not None:
                key = get_key(record)
                if key is None:
                    continue
                else:
                    next_idx_to_k[i] = key

        keys_with_prev_contig = []
        for k in next_idx_to_k.values():
            if k[0] == min_k[0]:
                keys_with_prev_contig.append(k)

        if any(keys_with_prev_contig):
            min_k = min(keys_with_prev_contig)
        else:
            min_k = min(next_idx_to_k.values())

        min_k_idxs = set([i for i, k in next_idx_to_k.items() if k == min_k])

        min_k_idxs = set()
        for i, k in next_idx_to_k.items():
            if k == min_k:
                min_k_idxs.add(i)

        records = []
        for i in range(len(nexts)):
            if i in min_k_idxs:
                records.append(nexts[i])
            else:
                records.append(None)
        yield records

        for i in min_k_idxs:
            nexts[i] = next_record(vcf_readers[i])


class OutputVCF:
    """Utility class for outputting VCF file.

    Limitations:
        Doesn't support FORMAT and sample columns (yet).
    """

    COLS = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO']
    HEADER = '##fileformat=VCFv4.2\n#{}\n'.format('\t'.join(COLS))

    def __init__(self, file=None, filename=None, header=None):
        if file:
            if 'w' not in file.mode:
                raise TypeError('`file` mode not set to writeable.')
            self.file = file
        elif filename:
            self.file = open(filename, 'w')
        else:
            raise TypeError('Both `file` and `filename` arguments are undefined.')
        self.header = header or self.HEADER
        self.write_header()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()

    @classmethod
    def info_to_string(cls, key, val):
        if val is None:
            result = key
        else:
            result = '{}={}'.format(key, cls.to_string(val))
        return result

    @classmethod
    def to_string(cls, field):
        if isinstance(field, str):
            result = field
        elif isinstance(field, bytes):
            result = str(field, 'utf-8')
        elif field is None:
            result = '.'
        elif isinstance(field, cyvcf2_INFO):
            infos = [cls.info_to_string(key, val) for key, val in field]
            result = ';'.join(infos)
        elif isinstance(field, (list, tuple)):
            result = ','.join(str(f) for f in field)
        elif isinstance(field, int):
            result = str(field)
        elif isinstance(field, float):
            result = str(round(field, 2))
        else:
            raise ValueError('Unsupported field: {}'.format(field))
        return result

    def write_header(self):
        """Write header to VCF file.

        Returns:
            None
        """
        self.file.write(self.header)

    def write_record(self, record, **kwargs):
        """Write VCF row to file based on a given VCF record.

        Args:
            record: cyvcf2 VCF record.
            kwargs: Dictionary of VCF columns (keys) to be overwritten with a
                given string (values).

        Returns:
            None
        """
        row = OrderedDict((col, self.to_string(getattr(record, col))) for col in self.COLS)
        # Update any columns based on kwargs
        for col in kwargs.keys() & self.COLS:
            row[col] = kwargs[col]
        line = '\t'.join(row.values()) + '\n'
        self.file.write(line)

    def write_row(self, CHROM, POS, ID, REF, ALT, QUAL, FILTER, INFO):
        cols = [CHROM, POS, ID, REF, ALT, QUAL, FILTER, INFO]
        line = '\t'.join(cols) + '\n'
        self.file.write(line)
