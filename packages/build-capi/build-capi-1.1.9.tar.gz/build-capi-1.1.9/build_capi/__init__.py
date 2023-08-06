from __future__ import absolute_import as _absolute_import

from pkg_resources import get_distribution as _get_distribution
from pkg_resources import DistributionNotFound as _DistributionNotFound

from .ext import CApiLib
from .build import build_capi

try:
    __version__ = _get_distribution('build_capi').version
except _DistributionNotFound:
    __version__ = 'unknown'
