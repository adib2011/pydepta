from past import autotranslate
autotranslate('pydepta')

from glob import glob
from pydepta import Depta

depta = Depta()
for fname in glob('pydepta/tests/resources/*.html'):
    with open(fname, 'rt') as fhandle:
        html = fhandle.read()
        depta.extract(html)

