
# -*- coding: utf-8 -*-

# Copyright (C) 2016 Andreu Casas
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details: 
# https://www.gnu.org/licenses/gpl-3.0.en.html

"""
This python module provides a set of example dataset used in the notes,
	modules, and exercises of my -Text as Data for Social Science 
	Research- teaching material. You can acces the materials in the 
	following website: http://andreucasas.com/text_as_data/
"""

# Data directory
path_to_dir = re.sub("__init__.py", "", __file__)

# FUNCTIONS to load datasets
def two_bill_versions():
	with open(path_to_dir + 'bill1084.json') as data_file:
		return(json.load(data_file))