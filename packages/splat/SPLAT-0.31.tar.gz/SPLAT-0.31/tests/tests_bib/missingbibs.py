# -*- coding: utf-8 -*-
from __future__ import print_function, division

"""
.. note::
         These are the database functions for SPLAT 
"""

import splat._initialize as Constants
import splat.bib as splbib

def missingbibs():
    bibs=[]
    dbsk = ['DISCOVERY_REFERENCE','OPT_TYPE_REF','NIR_TYPE_REF','LIT_TYPE_REF','GRAVITY_CLASS_OPTICAL_REF','GRAVITY_CLASS_NIR_REF','CLUSTER_REF','BINARY_REF','SBINARY_REF','COMPANION_REF','SIMBAD_SPT_REF','PARALLEX_REF','MU_REF','RV_REF','VSINI_REF']
    for k in dbsk:
        for b in Constants.DB_SOURCES[k]:
            if b not in bibs and b != '':
                if splbib.getBibTex(b,force=True) == False:
                    bibs.append(b)
    dbsk = ['DATA_REFERENCE']
    for k in dbsk:
        for b in Constants.DB_SPECTRA[k]:
            if b not in bibs and b != '':
                if splbib.getBibTex(b,force=True) == False:
                    bibs.append(b)
    if len(bibs) > 0:
        print('\nRetrieve the following from http://adsabs.harvard.edu/bib_abs.html and put into {}\n'.format(Constants.DB_FOLDER+Constants.BIBFILE))
        bibs.sort()
        for b in bibs: print(b)
    return

# main testing of program
if __name__ == '__main__':
#    dfolder = '/Users/adam/projects/splat/adddata/tobeadded/simp/prism/'
#    test_ingest(dfolder,spreadsheet=dfolder+'input.csv')
    test_missingbibs()
