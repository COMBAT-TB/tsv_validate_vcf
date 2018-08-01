# Only need to change these two variables
PKG_NAME=vcf_snps_utils
USER=sanbi-sa

OS=$TRAVIS_OS_NAME-64
mkdir ~/conda-bld
wget https://github.com/COMBAT-TB/vcf_snps_utils/archive/0.0.1.tar.gz
export SHA=$(sha256sum 0.0.1.tar.gz | awk '{print $1}')
conda config --set anaconda_upload no
export CONDA_BLD_PATH=~/conda-bld
export VERSION=0.0.1
conda build .
# anaconda -t $CONDA_UPLOAD_TOKEN upload -u $USER -l nightly $CONDA_BLD_PATH/$OS/$PKG_NAME-$VERSION.tar.bz2 --force