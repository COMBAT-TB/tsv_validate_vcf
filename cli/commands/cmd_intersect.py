import csv

import click
import vcf

from cli.cli import pass_context
from tabby import fields, Schema
from pprint import pprint as pp


class CsVFileSchema(Schema):
    pos_h37rv = fields.IntField('position in H37Rv')
    gene_name = fields.StringField('gene')
    short_name = fields.StringField('short name')
    snp_type = fields.StringField('snp_type')
    ref_h37rv = fields.StringField('H37Rv')

    #Sample snps
    sawc_507 = fields.StringField('SAWC-507')
    sawc_5218 = fields.StringField('SAWC-5218')
    sawc_5527 = fields.StringField('SAWC-5527')

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
    reference_rows = get_reference_rows(csvfile)
    vcf_rows = get_vcf_rows(vcffiles)

    # plot the intersects
    intersect_list = []
    for ref_dict in reference_rows:
        #pp(vcf_rows)
        #pp(ref_dict)
        #exit(0)
        intersect_list.append(dict(vcf=filter(lambda intersect_dict: intersect_dict['pos'] == ref_dict['pos_h37rv'], vcf_rows),csv=ref_dict))

    pp(intersect_list)
    #find_intersect(ref_dict['pos_h37rv'], vcf_rows)

def get_reference_rows(csvfile):
    # data structure to store csv snps - reference point
    with open(csvfile, 'r') as f:
        file_rows = csv.reader(f)
        rows = list(CsVFileSchema.process(file_rows))
    return rows

def get_vcf_rows(vcffiles):
    vcf_dict_list = []
    for vcffile in vcffiles:
        with open(click.format_filename(vcffile), 'r') as f:
            vcf_rows = vcf.Reader(f)
            for vcf_row in vcf_rows:
                vcf_dict_list.append(dict(pos=vcf_row.POS, ref=vcf_row.REF, snp=vcf_row.ALT,
                                          snp_status=vcf_row.is_snp, indel_status=vcf_row.is_indel))
    return vcf_dict_list


# Final - Output
# [{
#    'vcf': [{},{}],
#    'csv': {}
# }]
# self.ALT == getattr(other, "ALT", None))