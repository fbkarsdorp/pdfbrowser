#! /usr/bin/python

import os
import sys
import sh

from config import SRC, PATHS

for path in PATHS:
	for filename in os.listdir(path):
		try:
			if filename.endswith('.pdf') and not os.path.exists(os.path.join(SRC, filename)):
				sh.ln('-s', os.path.join(path, filename), os.path.join(SRC, filename))
		except Exception as e:
			sys.stderr.write(u"Can't create symlink to file '{}'.\n{}".format(filename,e))
			pass
