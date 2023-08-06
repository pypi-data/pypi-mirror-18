import os

import yaml

from pyresample.utils import parse_area_file

old_file = 'areas.def'
new_file = os.path.splitext(old_file) + '.yaml'
regions = parse_area_file(old_file)

res = {'regions': {}}
for a in regions:
    pd = a.proj_dict.copy()
    for key, val in a.proj_dict.items():
        try:
            pd[key] = float(val)
        except ValueError:
            pass
    reg = {'description': a.name, 'area_extent': list(a.area_extent), 'size': [
        a.x_size, a.y_size], 'projection': pd}
    res['regions'][a.area_id] = reg
with open('areas.yaml', 'w') as fd:
    yaml.dump(res, fd)
