#!/usr/bin/bash
# get it
wget -qO- http://code.enkre.net/bgen/tarball/release/bgen.tgz | tar xvfz -
mv bgen.tgz bgenix
cd bgenix
# compile it
./waf configure --prefix=${HPC_WORK}
./waf
# test it
./build/test/unit/test_bgen
./build/apps/bgenix -g example/example.16bits.bgen -list