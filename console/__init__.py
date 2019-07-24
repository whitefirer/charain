# coding=utf-8
# author=whitefirer

import os

if os.name != 'nt':
    from .console import *
else:
    from .winconsole import *