#/usr/bin/env python

# based on examples/feffit/doc_feffit1.lar
'''
Testing groups and parameters for EXAFS fitting
'''
import sys
from numpy import loadtxt
larchpath = '/usr/share/larch/plugins'

if all(path != larchpath for path in sys.path):
    sys.path.append(larchpath)

import larch
from larch import Group as group
from larch import Parameter as param
from larch_plugins.io import read_ascii
from larch_plugins.std import * #group2dict, show
from larch_plugins.xafs.feffdat import feffpath
from larch_plugins.xafs.feffit import feffit, feffit_transform, feffit_dataset, feffit_report

# declaring session
session = larch.Interpreter(with_plugins=False)

# read data
cu_data = read_ascii('cu.chi', labels='k chi', _larch=session)

# showing the data properties --comment out to continue
# show(cu_data, _larch=session)

# define fitting parameter group
pars = group(amp    = param(1, vary=True),
             del_e0 = param(0.1, vary=True),
             sig2   = param(0.002, vary=True),
             del_r  = param(0., vary=True) )

# define a Feff Path, give expressions for Path Parameters
path1 = feffpath('feff0001.dat',
                 s02    = 'amp',
                 e0     = 'del_e0',
                 sigma2 = 'sig2',
                 deltar = 'del_r')

# set tranform / fit ranges
trans = feffit_transform(kmin=3, kmax=17, kw=2, dk=4, window='kaiser', rmin=1.4, rmax=3.0, _larch=session)

# define dataset to include data, pathlist, transform
dset  = feffit_dataset(data=cu_data, pathlist=[path1], transform=trans, _larch=session)

# perform fit!
out = feffit(pars, dset, _larch=session)
