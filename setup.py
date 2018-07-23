from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='vcf_snps_utils',
    version='0.0.1',
    author="Zipho Mashologu",
    author_email="zipho@sanbi.ac.za",
    license='Apache License 2.0',
    description="Custom command line utility tools to manipulate vcf files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/COMBAT-TB/vcf_snp_utils",
    packages=['cli', 'cli.commands'],
    include_package_data=True,
    install_requires=[
        'click>=6.7',
        'intervene>=0.6.4',
        'matplotlib',
        'numpy',
        'pandas',
        'pathlib>=1.0.0'
        'pybedtools>=0.7.10',
        'PyVCF>=0.6.8',
        'scipy>=1.1.0',
        'tqdm>=4.23.4'
    ],
    classifiers=[
        'Development Status :: 3 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Bioinformaticians',
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Research'
    ],
    entry_points='''
        [console_scripts]
        vcf_snps_utils=cli.cli:cli
    ''',
)
