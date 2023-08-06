"""
morinkit.process
~~~~~~~~~~~~~~~~

This module contains top-level functions that processes files without changing
the file format.
"""


from .vcf import iter_vcfs, OutputVCF


def ensemble_vcf(vcf_filenames, output_file, is_sorted, min_support):
    """Integrate the variant calls from multiple VCF files and output an
    ensemble VCF file.

    ensemble_vcf is primarily meant for ensemble SNV calling. In other words,
    this function creates a VCF file where each variant is supported by at
    least `min_support` methods.

    Args:
        vcf_files: List of VCF file paths.
        output: Opened writeable file.
        is_sorted: Boolean indicating whether the input VCF files are sorted.
        min_support: Integer or fraction indicating the minimum number of
            methods supporting each variant.

    Returns:
        None
    """
    overwrite = {'ID': '.', 'QUAL': '.', 'FILTER': '.', 'INFO': '.'}
    num_methods = len(vcf_filenames)
    with OutputVCF(file=output_file) as ovcf:
        for all_records in iter_vcfs(vcf_filenames, is_sorted=is_sorted):
            # filter(None, records) removes items that evaluate to False (incl. None)
            # Because the records represent the same variant, we take the first one
            records = list(filter(None, all_records))
            num_called = len(records)
            # If min_support is less than 1, consider the fraction of methods
            # supporting the variant.
            if min_support < 1 and num_called / num_methods < min_support:
                continue
            # If the min_support is greater or equal to one, consider the
            # absolute number of methods supporting the variant.
            elif min_support >= 1 and num_called < min_support:
                continue
            # Write out record while overwritting unnecessary VCF fields.
            ovcf.write_record(records[0], **overwrite)
