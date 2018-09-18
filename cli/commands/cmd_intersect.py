import csv
import os
from subprocess import call, PIPE

import click
import time
import vcf
from pathlib import Path

try:
    from cli.cli import pass_context
    from cli.commands.util import pbopen
    from cli.commands.report import generate_report
except (ImportError, ValueError):
    from cli.cli import pass_context
    from cli.commands.util import pbopen
    from cli.commands.report import generate_report

from pprint import pprint as pp


@click.command('intersect', short_help='Intersect SNPs with a CSV file.')
@click.argument('vcffiles', nargs=-1, type=click.Path(exists=True))
@click.argument('csvfile', type=click.Path(exists=True))
@click.option('--outdir', default="/tmp/vcf_snps_utils_output",
              help='set the output directory, default is "/tmp/vcf_snps_utils_output/"')
@pass_context
def cli(ctx, outdir, vcffiles, csvfile):
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
    ref_samples = set(ref_rows[0].keys()).difference(set(['gene', 'short_name', 'snp_type', 'H37Rv', 'H37Rv_POS']))

    # Do it for multiple VCF files
    for vcffile in vcffiles:
        vcf_rows = get_vcf_rows(vcffile)

        # Group by positions and get intersects
        intersect_result = [
            dict(
                vcf=[fil for fil in filter(lambda sect_dict: sect_dict['pos'] == int(ref_dict['H37Rv_POS']), vcf_rows)],
                csv=ref_dict) for ref_dict in ref_rows]

        # Refine results
        results = f_results(intersect_result, [k for k, v in ref_rows[0].items() if
                                               k not in ['H37Rv', 'H37Rv_POS', 'gene', 'snp_type', 'short_name',
                                                         'gene']])

        # Create output files
        if not os.path.exists(outdir + '/vcf'):
            os.makedirs(outdir + '/vcf')
        create_output_files(results, outdir, ref_samples)

    # For each sample create an output
    for ref_sample in ref_samples:
        sample_output_dir = outdir + '/' + ref_sample
        if not os.path.exists(sample_output_dir):
            os.makedirs(sample_output_dir)

        # Trigger the VISUALISATION / PLOTTING output
        ctx.log("## Create Visualisation")
        call('intervene upset -i {0}/{1}.txt {0}/vcf/*.txt --type list --output {2}'.format(outdir, ref_sample,
                                                                                            sample_output_dir),
             shell=True, stdout=PIPE)
        ctx.log("## End")

    # @TODO: Generate Pandas for Stats on the results

    # Generate the report
    report = generate_report(file_name='vcf_intesect_report', data=ref_samples)


def get_ref_rows(csvfile):
    with pbopen(csvfile) as f:
        file_rows = csv.DictReader(f)
        rows = [r for r in file_rows]
    return rows


def get_vcf_rows(vcffile):
    with pbopen(click.format_filename(vcffile)) as f:
        vcf_rows = vcf.Reader(f)
        vcf_dict_list = [
            dict(pos=int(vcf_row.POS), ref=vcf_row.REF, snp=vcf_row.ALT, filename=os.path.basename(vcffile),
                 samples=[s.sample for s in vcf_row.samples],
                 snp_status=vcf_row.is_snp, indel_status=vcf_row.is_indel) for vcf_row in vcf_rows]
    return vcf_dict_list


def f_results(result, samples):
    result_list = list()
    for r in result:
        f_dict = dict(pos=int(r['csv']['H37Rv_POS']))
        for sample in samples:
            f_dict[sample] = "POS_{}_FALSE".format(r['csv']['H37Rv_POS']) if (
                r['csv'].get(sample) == r['csv']['H37Rv']) else "POS_{}_TRUE".format(r['csv']['H37Rv_POS'])
        for i in range(max([len(v['vcf']) for v in result])):
            if r['vcf']:
                try:
                    record = r['vcf'][i]
                    f_dict['{0}_pos_picked_{1}'.format(record['filename'], i)] = "POS_{}_{}".format(record['pos'],
                                                                                                    str(record[
                                                                                                            'snp_status']).upper())
                except IndexError:
                    # @TODO: nothing was found - might need revision
                    record = r['vcf'][0]
                    f_dict['{0}_pos_picked_{1}'.format(record['filename'], i)] = 'N/A'
            else:
                # @TODO: nothing was found - might need revision
                f_dict['{0}_pos_picked_{1}'.format(get_vcf_file_name(result), i)] = 'N/A'
        result_list.append(f_dict)
    return result_list


def create_output_files(results, out_dir, ref_samples):
    output_files = [k for k, v in results[0].items() if k not in ['pos']]
    for o in output_files:
        if o in ref_samples:
            output_filename = "{}/{}.txt".format(out_dir, o)
        else:
            output_filename = "{}/vcf/{}.txt".format(out_dir, o)
        current_file = open(output_filename, 'w+')
        for r in results:
            if str(r[o]) != "N/A":
                current_file.write("{}\n".format(str(r[o])))
            else:
                current_file.write("")
        current_file.close()


def get_vcf_file_name(result):
    for r in result:
        if r['vcf']:
            return r['vcf'][0]['filename']
    return None
