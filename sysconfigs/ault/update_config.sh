#!/bin/bash

# for the love of god, run this in this path.

envroot=/user-environment
cp $envroot/config/compilers.yaml .

rm -rf ../../repos/alps
mkdir -p ../../repos/alps
cp -Rv /user-environment/repo/* ../../repos/alps
