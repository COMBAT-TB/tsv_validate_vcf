from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='vcf_snps_utils',
    version='1.0.0',
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
        'backcall>=0.1.0',
        'certifi>=2018.4.16',
        'cycler>=0.10.0',
        'decorator>=4.3.0',
        'idna>=2.7',
        'intervene>=0.6.4',
        'jedi>=0.12.1',
        'matplotlib',
        'numpy',
        'pandas',
        'pathlib>=1.0.0'
        'pybedtools>=0.7.10',
        'Pygments>=2.2.0',
        'pyparsing>=2.2.0',
        'pysam>=0.14.1',
        'python-dateutil>=2.7.3',
        'pytz>=2018.5',
        'PyUpSet>=0.1.1.post7',
        'PyVCF>=0.6.8',
        'PyYAML>=3.12',
        'requests>=2.19.1',
        'requests-toolbelt>=0.8.0',
        'scipy>=1.1.0',
        #'scikit-allel>=1.1.10',
        'seaborn>=0.8.1',
        'simple-settings>=0.13.0',
        'simplegeneric>=0.8.1',
        'six>=1.11.0',
        'tqdm>=4.23.4',
        'traitlets>=4.3.2',
        'twine>=1.11.0',
        'UpSetPlot>=0.1',
        'urllib3>=1.23'
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
