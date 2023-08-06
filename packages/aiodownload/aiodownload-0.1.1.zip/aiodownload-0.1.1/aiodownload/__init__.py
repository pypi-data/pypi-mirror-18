# -*- coding: utf-8 -*-
"""aiodownload API
"""

from .aiodownload import AioDownload, AioDownloadBundle
from .api import one, swarm
from .strategy import BackOff, Lenient, RequestStrategy


__all__ = (
    'AioDownload',
    'AioDownloadBundle'
    'BackOff',
    'Lenient',
    'RequestStrategy',
    'one',
    'swarm'
)
