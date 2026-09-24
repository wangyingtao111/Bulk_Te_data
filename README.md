# Data and Code: Exceptional Thermoelectric Performance in p-Type Bulk Tellurium via Strain-Induced ElectroThermal Decoupling

This repository contains the necessary computational input files, scripts, and raw figure data to support the findings in our manuscript submitted to *Computational Materials Science*.

## Authors
Yingtao Wang, Shengyuan Yang

## Computational Methodology
The dataset supports our investigation of thermal transport, lattice dynamics, and thermoelectric properties using the following software packages:
* **VASP**: Used for structural relaxation, electronic band structure, and density of states calculations.
* **AMSET**: Used for electron transport modeling.
* **ShengBTE**: Used for lattice thermal conductivity and phonon transport calculations.

## Repository Structure
* **`/1_VASP_Inputs/`**: Contains core input files (`INCAR`, `POSCAR`, `KPOINTS`) for un-strained and strained structures. *(Note: POTCAR files are excluded due to licensing)*.
* **`/2_Transport_Inputs/`**:
    * `/AMSET/`: Contains `settings.yaml` and associated transport parameter setups.
    * `/ShengBTE/`: Contains `CONTROL` files and scripts used to process force constants.
* **`/3_Figure_Data/`**: Contains raw numerical data (e.g., .csv, .txt) used to plot the figures in the manuscript:
    * `Fig1_band_structure`[cite: 1]
    * `Fig2_electronic_AMSET`[cite: 1]
    * `Fig3_allstrain600K_P_type`[cite: 1]
    * `Fig4_ZT_Ptype_relax2_2`[cite: 1]
    * `Fig5_strain_comparison_600K`[cite: 1]
    * `Fig6_thermoelectric_params`[cite: 1]
    * `Fig7_phonon_2percent_tensile`[cite: 1]

## Usage Notes
Due to file size constraints, large intermediate files (e.g., `WAVECAR`, `CHGCAR`) are not included. Researchers can reproduce the electronic structure and transport properties by executing VASP, AMSET, and ShengBTE with the provided configuration files.

## Contact
For questions regarding the dataset or computational details, please contact Yingtao Wang at [Your Email Address].
