import csv
import numpy as np
import vcf
from tabby import fields, Schema

class StopSchema(Schema):
    pos_h37rv = fields.StringField('position in H37Rv')
    gene_name = fields.StringField('gene')
    short_name = fields.StringField('short name')
    snp_type = fields.StringField('snp_type')
    ref_h37rv = fields.StringField('H37Rv')
    sawc_507 = fields.StringField('SAWC-507')
    sawc_5218 = fields.StringField('SAWC-5218')
    sawc_5527 = fields.StringField('SAWC-5527')

import pprint
with open('vcf_results.csv', 'r') as f:
    rows = csv.reader(f)
    rows = list(StopSchema.process(rows))

print("========== Stell Ref Data ================")
#for row in rows:
#    print("POS:" + row['pos_h37rv'])

print("========== VCF Data ================")
with open('snpeff_vcf_example.vcf', 'r') as f:
    vcf_rows = vcf.Reader(f)
    vcf_dict_list = []
    for vcf_row in vcf_rows:
        vcf_dict_list.append(dict(pos=vcf_row.POS,ref=vcf_row.REF,snp=vcf_row.ALT))
    pprint.pprint(vcf_dict_list)

#List of Pos - Ref - SNP - Stellenbosch_Results_Data
# 1. SNPs produced by the 3 Galaxy pipelines
# 2. We take position from the Stellenbosch_Results_Data and confirm if they are the same
# 3. Highlight the differences.
# 4. List all the missed SNPs by the Stellenbosch_Results_Data
# 5. List all ommitted SNPs by the Stellenbosch_Results_Data



