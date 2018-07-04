import csv
import os

import click
import vcf

from cli.cli import pass_context
from pprint import pprint as pp
from cli.lib.pbopen import pbopen


@click.command('intersect', short_help='Intersect SNPs with a CSV file.')
@click.argument('vcffiles', nargs=-1, type=click.Path(exists=True))
@click.argument('csvfile', type=click.Path(exists=True))
@pass_context
def cli(ctx, vcffiles, csvfile):
    """VCF snp intersect tool (CSV file).

       This tools compares CSV snps to the VCF snps
       This is to establish whether the discovered (VCF snps)
       have been discovered in the pass. This will potential be
       extended to include verification using other external source
       such as databases/api.

       \b
       CSV File passed should be in the following format (Example):
       position in H37Rv	gene	short name	snp_type	Reference	Sample1   Sample2	Sample3
       1285	dnaA	dnaA1285	nsSNP	G	G	G	G
       4013	recF	recF4013	nsSNP	T	C	C	C

       Report bugs to: combattb-help@sanbi.ac.za
       CombatTB home page: <http://www.combattb.org/software/tools/>
       General help using CombatTB software: <http://www.combattb.org/gethelp/>
       """

    # The files involved as input to the program.
    for vcffile in vcffiles:
        ctx.log('Input VCF FILE: ' + click.format_filename(vcffile))
    ctx.log('Input CSV FILE: ' + click.format_filename(csvfile))

    # Get the Reference - Rows (list of dicts)
    ref_rows = get_ref_rows(csvfile)
    vcf_rows = get_vcf_rows(vcffiles)

    # group by position - intersects
    result = [dict(vcf=[fil for fil in filter(lambda sect_dict: sect_dict['pos'] == int(ref_dict['H37Rv_POS']), vcf_rows)],
                   csv=ref_dict) for ref_dict in ref_rows]

    #Sample Names in the CSV
    sampleNameList = [k for k,v in ref_rows[0].items() if k not in ['H37Rv', 'H37Rv_POS', 'gene', 'snp_type', 'short_name', 'gene']]

    res = f_results(result, sampleNameList)

    pp(result)


def get_ref_rows(csvfile):
    with pbopen(csvfile) as f:
        file_rows = csv.DictReader(f)
        rows = [r for r in file_rows]
    return rows


def get_vcf_rows(vcffiles):
    for vcffile in vcffiles:
        with pbopen(click.format_filename(vcffile)) as f:
            vcf_rows = vcf.Reader(f)
            vcf_dict_list = [dict(pos=vcf_row.POS, ref=vcf_row.REF, snp=vcf_row.ALT, filename=os.path.basename(vcffile),
                                  samples=[s.sample for s in vcf_row.samples],
                                  snp_status=vcf_row.is_snp, indel_status=vcf_row.is_indel) for vcf_row in vcf_rows]
    return vcf_dict_list


def f_results(result, samples):
    r_l = []
    for r in result:
        f_dict = dict(pos=r['csv']['H37Rv_POS'])
        for sample in samples:
            f_dict[sample] = True if r['csv'].get(sample) else False
        for num, rl in enumerate(r['vcf']):
            if rl['ref'] == r['csv']['H37Rv']:
                f_dict['{0}_{1}'.format(rl['filename'], num)] = True if str(rl['snp']) != [] else False
        r_l.append(f_dict)
    return r_l

#
# [{'h37rv': 'G', 'indel': False, 'pos': 1285, 'snp': False, 'vcf': [A, <*>]},
#  {'h37rv': 'G', 'indel': False, 'pos': 1285, 'snp': False, 'vcf': [A, T, <*>]},
#  {'h37rv': 'G', 'indel': False, 'pos': 1285, 'snp': False, 'vcf': [T, A, <*>]},
#  {'h37rv': 'T', 'indel': False, 'pos': 4013, 'snp': True, 'vcf': [C]},
#  {'h37rv': 'T', 'indel': False, 'pos': 4013, 'snp': False, 'vcf': [C, <*>]},
#  {'h37rv': 'G', 'indel': False, 'pos': 15890, 'snp': 7, 'vcf': [A, <*>]},
#  {'h37rv': 'A', 'indel': False, 'pos': 37334, 'snp': True, 'vcf': [T]},
#  {'h37rv': 'A', 'indel': False, 'pos': 37334, 'snp': False, 'vcf': [T, <*>]},
#  {'h37rv': 'T', 'indel': False, 'pos': 43347, 'snp': False, 'vcf': [G, <*>]},
#  {'h37rv': 'T', 'indel': False, 'pos': 45753, 'snp': False, 'vcf': [<*>]},
#  {'h37rv': 'A', 'indel': False, 'pos': 66604, 'snp': False, 'vcf': [<*>]},
#  {'h37rv': 'G', 'indel': False, 'pos': 109192, 'snp': False, 'vcf': [<*>]},
#  {'h37rv': 'C', 'indel': False, 'pos': 128357, 'snp': False, 'vcf': [<*>]},
#  {'h37rv': 'G', 'indel': False, 'pos': 138419, 'snp': False, 'vcf': [<*>]},
#  {'h37rv': 'G', 'indel': False, 'pos': 141623, 'snp': True, 'vcf': [A]},