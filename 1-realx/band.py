from pymatgen.io.vasp import Vasprun
v = Vasprun("vasprun.xml")
gap_info = v.get_band_structure().get_band_gap()
print(gap_info)
