#! /usr/bin/python

import os
import sh

from config import SRC, PATHS

for path in PATHS:
	for filename in os.listdir(path):
		if filename.endswith('.pdf') and not os.path.exists(os.path.join(SRC, filename)):
			sh.mv(os.path.join(path, filename), os.path.join(SRC, filename))
