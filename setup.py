from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='vcf_snp_utils',
    version='1.0',
    author="Zipho Mashologu",
    author_email="zipho@sanbi.ac.za",
    description="Custom command line utility tools to manipulate vcf files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/COMBAT-TB/vcf_snp_utils",
    packages=['cli', 'cli.commands'],
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        vcf_snp_utils=cli.cli:cli
    ''',
)