#!/usr/bin/env python
#
# Author: Yang Gao <younggao1994@gmail.com>
#

import ctf
from pyscf import gto, scf
from cc_sym.rccsd import RCCSD
from cc_sym.settings import comm, rank, size
import sys, os

if rank!=0:
    sys.stdout = open(os.devnull, "w")
else:
    sys.stdout = open("h2o_10pvdz_%i.dat"%size, "w")

mol = gto.Mole()
mol.atom = '''
O       97.873900000   103.017000000   100.816000000
H       98.128600000   103.038000000    99.848800000
H       97.173800000   102.317000000   100.960000000
O       99.814000000   100.835000000   101.232000000
H       99.329200000    99.976800000   101.063000000
H       99.151600000   101.561000000   101.414000000
O       98.804000000    98.512200000    97.758100000
H       99.782100000    98.646900000    97.916700000
H       98.421800000    99.326500000    97.321300000
O      100.747000000   100.164000000   103.736000000
H      100.658000000   100.628000000   102.855000000
H      100.105000000    99.398600000   103.776000000
O       98.070300000    98.516900000   100.438000000
H       97.172800000    98.878600000   100.690000000
H       98.194000000    98.592200000    99.448100000
O       98.548000000   101.265000000    97.248600000
H       98.688900000   102.140000000    97.711000000
H       97.919900000   101.391000000    96.480800000
O      102.891000000   100.842000000    97.477600000
H      103.837000000   100.662000000    97.209700000
H      102.868000000   101.166000000    98.423400000
O      102.360000000   101.551000000    99.964500000
H      102.675000000   102.370000000   100.444000000
H      101.556000000   101.180000000   100.430000000
O      101.836000000    97.446700000   102.110000000
H      100.860000000    97.397400000   101.898000000
H      101.991000000    97.133400000   103.047000000
O      101.665000000    98.316100000    98.319400000
H      101.904000000    99.233800000    98.002000000
H      102.224000000    97.640900000    97.837700000
'''
mol.basis = "ccpvdz"
mol.verbose = 5
mol.build()

mf = scf.RHF(mol)
if rank==0:
    mf.kernel()

comm.barrier()
mf.mo_coeff = comm.bcast(mf.mo_coeff, root=0)
mf.mo_occ = comm.bcast(mf.mo_occ, root=0)

mycc = RCCSD(mf, SYMVERBOSE=1)
mycc.max_cycle = 1
mycc.kernel()
