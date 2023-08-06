#
# setup.py
#
# // license
# Copyright 2016, Free Software Foundation.
#
# This file is part of Solent.
#
# Solent is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# Solent is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# Solent. If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup

setup(
  name = 'solent',
  packages = ['solent'],
  version = '0.14',
  description = 'Event-driven concurrency engine',
  author = 'Craig Turner',
  url = 'https://github.com/cratuki/solent',
  download_url = 'https://github.com/cratuki/solent/tarball/0.14',
  keywords = ['solent', 'eng', 'term', 'networking', 'roguelikes', 'async'],
  classifiers = [],
)

