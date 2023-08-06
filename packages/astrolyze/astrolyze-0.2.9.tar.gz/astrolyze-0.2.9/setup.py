# Copyright (C) 2012, Christof Buchbender
# BSD License (License.txt)
r""" Installation of Astrolyze using distutils.core.setup.
Basically it copies all scripts to
"""

import os
import sys
import site
import subprocess
from setuptools import setup


USER = os.getenv("SUDO_USER")
if not USER:
    USER = os.getenv("USER")


data_files=[]

CONFIG_FOLDER = "/home/{}/.astrolyze/".format(USER)

data_files = [("/home/{}/.astrolyze/cfg/".format(USER),
              ["cfg/calibration_error.txt", "cfg/galaxy_parameter.txt",
               "cfg/line_parameter.txt"]),
              ("/home/{}/.ipython/profile_astrolyze/".format(USER),
               ["cfg/ipython_config.py"]),
              ("/home/{}/.astrolyze/".format(USER),
               ["cfg/astrolyze.cfg"])
]

if str(USER) == "None":
    data_files = []

setup(
    name='astrolyze',
    version=open('VERSION').read().strip(),
    author='Christof Buchbender',
    author_email='buchbend@ph1.uni-koeln.de',
    url='https://github.com/buchbend/astrolyze.git',
    packages=['astrolyze',
              'astrolyze/maps',
              'astrolyze/spectra',
              'astrolyze/sed',
              'astrolyze/lte',
              'astrolyze/functions',
             ],
    package_data={"astrolyze":["VERSION"]},
    data_files = data_files,
    license='LICENSE.txt',
    description=('Reduction and analysing tools for (mainly)'
                 'Radioastronomical Data.'),
    long_description=open('README.rst').read(),
    requires=[
        "astropy",
        "numpy",
        "scipy",
        "matplotlib",
        "pysqlite2",
        "docutils",
        "generaltools"
    ],
    classifiers=[
        'Intended Audience :: Science/Research',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics'
      ],
    scripts=['scripts/astrolyze_opt_db_setup.py',
             'scripts/astrolyze']
)

subprocess.call("chown -R {0}:{0} {1}".format(USER,
                                              CONFIG_FOLDER),
                shell=True)
