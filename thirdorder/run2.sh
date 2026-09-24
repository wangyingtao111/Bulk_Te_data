#!/bin/bash

# mkdir -p vasprun

for i in {17..24};
do
    mkdir -p vasprun/disp-$i
    cp INCAR POTCAR KPOINTS 3RD.POSCAR.$i vasprun/disp-$i
    cd vasprun/disp-$i
    mv 3RD.POSCAR.$i POSCAR
    mpirun -np 32 vasp_std
    cd ../..
done
