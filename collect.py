#! /usr/bin/python

import os
import sys
import sh

from config import SRC, PATHS

for path in PATHS:
	for folder, subfolders, filenames in os.walk(path):
		for filename in filenames:
			try:
				if filename.endswith('.pdf') and not os.path.exists(os.path.join(SRC, filename)):
					sh.ln('-s', os.path.join(path, filename), os.path.join(SRC, filename))
			except Exception as e:
				sys.stderr.write(u"Can't create symlink to file '{}'.\n{}".format(filename.decode('utf8'),e))
				pass
