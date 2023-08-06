# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 17:38:09 2016

@author: hcj
"""

#import sys

#print repr(sys.stderr.encoding)

import time, subprocess
#
from common import CallInNewConsole
#
args = 'python', 'qrcodeserver.py', '8080', '.'
#
print CallInNewConsole(args)
## cmd = '"' + '" "'.join(args) + '"'
#
## subprocess.call(['mate-terminal', '-e', cmd])
#
time.sleep(30)
