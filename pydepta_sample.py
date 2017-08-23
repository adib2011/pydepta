from past import autotranslate
autotranslate('pydepta')

from glob import glob
from pydepta import Depta

REPEATS = 5

depta = Depta()
for fname in glob('pydepta/tests/resources/*.html'):
    with open(fname, 'rt') as fhandle:
        html = fhandle.read()
        for _ in range(REPEATS):
            depta.extract(html)

