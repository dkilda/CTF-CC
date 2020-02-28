#!/usr/bin/env python
#
# Author: Yang Gao <younggao1994@gmail.com>
#

'''
A simple example to run pbc KRCCSD with ctf parallelization
Usage: mpirun -np 4 python 02-pbc_ctf_krccsd.py
'''
from pyscf.pbc import scf, gto
from cc_sym import kccsd_rhf, settings

rank = settings.rank
comm = settings.comm

cell = gto.Cell()
cell.atom='''
C 0.000000000000   0.000000000000   0.000000000000
C 1.685068664391   1.685068664391   1.685068664391
'''
cell.basis = 'gth-szv'
cell.pseudo = 'gth-pade'
cell.a = '''
0.000000000, 3.370137329, 3.370137329
3.370137329, 0.000000000, 3.370137329
3.370137329, 3.370137329, 0.000000000'''
cell.unit = 'B'
cell.verbose = 5
cell.mesh = [15,15,15]
cell.build()

kpts = cell.make_kpts([1,1,3])
mf = scf.KRHF(cell, kpts, exxdiv=None)

if rank==0: #SCF only needs to run on one process
    mf.kernel()

comm.barrier()
mf.mo_coeff = comm.bcast(mf.mo_coeff, root=0)
mf.mo_occ = comm.bcast(mf.mo_occ, root=0)

mycc = kccsd_rhf.KRCCSD(mf)
mycc.kernel()

mycc.ipccsd(nroots=2, kptlist=[0], koopmans=True)
mycc.eaccsd(nroots=2, kptlist=[0], koopmans=True)
