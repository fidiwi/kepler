import re

p = re.compile('(?<=_)(\d*?)\.(\d*?)(?=_)')
print(float(p.search("Probedaten/Beispiesamples/Mail_lutz_3/Luecken/5_percent/10000_3.0_05_.67500,.72500_pos.csv").group()))
