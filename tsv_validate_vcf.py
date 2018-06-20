import csv
import tabby
import pprint
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
                   
with open('vcf_results.csv', 'r') as f:
    rows = csv.reader(f)
    #for row in rows:
    #    print row
    rows = list(StopSchema.process(rows))
    pprint.pprint(rows)
    