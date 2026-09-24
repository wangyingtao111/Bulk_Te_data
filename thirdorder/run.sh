#!/bin/bash

mkdir -p vasprun

for i in {01..24};
do
    mkdir -p vasprun/disp-$i
    cp INCAR POTCAR KPOINTS 3RD.POSCAR.$i vasprun/disp-$i
    cd vasprun/disp-$i
    mv 3RD.POSCAR.$i POSCAR
    mpirun -np 16 vasp_std
    cd ../..
done
/usr/bin/curl -s -X POST "http://www.pushplus.plus/send" -H "Content-Type: application/json" -d '{"token":"d10390c8f7024ab79e19fa00381e1b40", "title":"VASP任务结束", "content":"计算已停止，请进入目录查看结果。"}'
