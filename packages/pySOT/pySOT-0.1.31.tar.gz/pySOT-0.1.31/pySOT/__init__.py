try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from pySOT.experimental_design import *
from pySOT.rbf import *
from pySOT.rs_wrappers import RSCapped, RSUnitbox
from pySOT.adaptive_sampling import *
from pySOT.test_problems import *
from pySOT.sot_sync_strategies import *
from pySOT.ensemble_surrogate import EnsembleSurrogate
from pySOT.poly_regression import *
from pySOT.merit_functions import *
from pySOT.utils import *

try:
    from pySOT.mars_interpolant import MARSInterpolant
    __with_mars__ = True
except ImportError:
    __with_mars__ = False

__version__ = '0.1.31'
__author__ = 'David Eriksson, David Bindel, Christine Shoemaker'
