#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup, Extension
import numpy as np

numpy_include = np.get_include()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='SELDOMpy',
    version='0.9.8',
    description='Dynamic modelling of cellular signalling networks.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Luis Prado',
    author_email='pradolopezluis@gmail.com',
    url='https://github.com/lupralo31/SELDOMpy',
    download_url='https://github.com/lupralo31/SELDOMpy/archive/refs/tags/V_0.2.1.tar.gz',
    packages=find_packages(exclude=('tests',)),
    ext_modules=[Extension(
        "hello",
        sources=["SELDOMpy/src/AMIGO_problem.c", "SELDOMpy/src/cvodea.c", "SELDOMpy/src/cvodea_io.c",
                 "SELDOMpy/src/cvodes_band.c", "SELDOMpy/src/cvodes_bbdpre.c", "SELDOMpy/src/cvodes_diag.c",
                 "SELDOMpy/src/cvodes_dense.c", "SELDOMpy/src/cvodes_bandpre.c", "SELDOMpy/src/cvodes.c",
                 "SELDOMpy/src/AMIGO_model_stats.c", "SELDOMpy/src/AMIGO_model.c", "SELDOMpy/src/anODEModel.c",
                 "SELDOMpy/src/cvodes_direct.c", "SELDOMpy/src/cvodes_io.c", "SELDOMpy/src/cvodes_spbcgs.c",
                 "SELDOMpy/src/cvodes_spgmr.c", "SELDOMpy/src/cvodes_spils.c", "SELDOMpy/src/cvodes_sptfqmr.c",
                 "SELDOMpy/src/decimal2binary.c", "SELDOMpy/src/dhc.c", "SELDOMpy/src/fnvector_serial.c",
                 "SELDOMpy/src/findStates.c", "SELDOMpy/src/get_count_bits.c",
                 "SELDOMpy/src/get_support_truth_tables.c",
                 "SELDOMpy/src/get_input_index.c", "SELDOMpy/src/get_truth_tables_index.c",
                 "SELDOMpy/src/getAdjacencyMatrix.c",
                 "SELDOMpy/src/getNumBits.c", "SELDOMpy/src/getNumInputs.c", "SELDOMpy/src/getStateIndex.c",
                 "SELDOMpy/src/getTruthTables.c",
                 "SELDOMpy/src/hill_function.c", "SELDOMpy/src/linear_transfer_function.c", "SELDOMpy/src/normHill.c",
                 "SELDOMpy/src/nvector_serial.c", "SELDOMpy/src/printAdjMat.c", "SELDOMpy/src/printInterMat.c",
                 "SELDOMpy/src/printNminiTerms.c", "SELDOMpy/src/printTruthTables.c", "SELDOMpy/src/sim_logic_ode.c",
                 "SELDOMpy/src/simulate_amigo_model.c",
                 "SELDOMpy/src/sundials_band.c",
                 "SELDOMpy/src/sundials_dense.c", "SELDOMpy/src/sundials_direct.c", "SELDOMpy/src/sundials_iterative.c",
                 "SELDOMpy/src/sundials_math.c", "SELDOMpy/src/sundials_nvector.c", "SELDOMpy/src/sundials_spbcgs.c",
                 "SELDOMpy/src/sundials_spgmr.c", "SELDOMpy/src/sundials_sptfqmr.c"],
        include_dirs=['SELDOMpy/src/include/include_amigo', 'SELDOMpy/src/include/include_cvodes', "SELDOMpy/src", numpy_include],
    )],
    install_requires=["numpy", "scikit-learn", "pandas", "mealpy", "matplotlib", "setuptools", "openpyxl", "pypesto", "scipy"],
    include_package_data=True,
    license='GPLv3',
    classifiers=[
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    keywords=['SELDOMpy', 'SELDOM', 'dynamic modelling', 'cellular signalling networks', 'biomedical engineering'],
)
