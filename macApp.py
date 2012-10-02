import sys
import os.path

base = os.path.dirname(os.path.abspath(sys.argv[0]))
base = os.path.join(base, 'lib/python2.7/')
sys.path.append(base)

import builder
