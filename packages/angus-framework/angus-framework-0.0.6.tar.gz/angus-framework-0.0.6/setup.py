#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

""" Simple setup for Angus.ai Service framework library
"""

from setuptools import setup, find_packages
import os

__updated__ = "2016-12-09"
__author__ = "Aurélien Moreau"
__copyright__ = "Copyright 2015-2016, Angus.ai"
__credits__ = ["Aurélien Moreau", "Gwennaël Gâté"]
__status__ = "Production"

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                       "requirements.txt")) as f:
    requirements = f.read().splitlines()

setup(name='angus-framework',
      version="0.0.6",
      description='Angus Cloud Framework',
      author=__author__,
      author_email='aurelien.moreau@angus.ai',
      url='http://www.angus.ai/',
      install_requires=requirements,
      packages=find_packages(),
      )
