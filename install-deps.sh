#!/bin/sh

wget -O - https://github.com/mozilla/DeepSpeech/releases/download/v0.1.1/deepspeech-0.1.1-models.tar.gz | tar xvfz -
rm deepspeech-0.1.1-models.tar.gz
pip install deepspeech

mkdir openmpi && cd openmpi
wget https://download.open-mpi.org/release/open-mpi/v2.0/openmpi-2.0.4.tar.gz
tar zxvf openmpi-2.0.4.tar.gz
cd openmpi-2.0.4
./configure --prefix=$HOME/opt/usr/local
make all
make install
sudo echo "# For OpenMP binary files" >> ~/.bash_profile
sudo echo "export PATH="$PATH:$HOME/opt/usr/local/bin"" >> ~/.bash_profile
source ~/.bash_profile
pip install mpi4py --upgrade
