import sys
from pathlib import Path

sys.path.insert(0, Path(__file__).parent.parent.__str__())
# print(f'{sys.path=}')

from seolpyo_mplchart import sample


sample()

