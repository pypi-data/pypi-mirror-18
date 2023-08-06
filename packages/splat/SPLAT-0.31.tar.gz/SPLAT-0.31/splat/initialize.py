# -*- coding: utf-8 -*-
from __future__ import print_function, division

"""
.. note::
         These commands initialize the SPLAT code 
"""

import os
import sys
from astropy import units as u


# things that are constants
SPLAT_URL = 'http://pono.ucsd.edu/~adam/splat/'
SPLAT_EMAIL = 'aburgasser@gmail.com'
DATA_FOLDER = '/reference/Spectra/'
FILTER_FOLDER = '/reference/Filters/'
SPECTRAL_MODEL_FOLDER = '/reference/SpectralModels/'
DB_FOLDER = '/db/'
DB_SOURCES_FILE = 'source_data.txt'
DB_SPECTRA_FILE = 'spectral_data.txt'
DB_PHOTOMETRY_FILE = 'photometry_data.txt'
BIBFILE = 'biblibrary.bib'
TMPFILENAME = 'splattmpfile'
ACCESS_FILE = '.splat_access'

MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

#set the SPLAT PATH, either from set environment variable or from sys.path
SPLAT_PATH = './'
if os.environ.get('SPLAT_PATH') != None:
    SPLAT_PATH = os.environ['SPLAT_PATH']
# get from PYTHONPATH
if os.environ.get('PYTHONPATH') != None and SPLAT_PATH == './':
    path = os.environ['PYTHONPATH']
    for i in path.split(':'):
        if 'splat' in i:
            SPLAT_PATH = i
# get from system path
if SPLAT_PATH == './':
    checkpath = ['splat' in r for r in sys.path]
    if max(checkpath):
        SPLAT_PATH = sys.path[checkpath.index(max(checkpath))]

# dwarf spectral standards
STDS_DWARF_SPEX_KEYS = { \
    'M0.0': 11335, #'11335_10505.fits',\
    'M1.0': 11364, #'11364_10806.fits',\
    'M2.0': 11181, #'11181_10187.fits',\
    'M3.0': 10823, #'10823_11422.fits',\
    'M4.0': 12004, #'12004_10444.fits',\
    'M5.0': 10829, #'10829_10104.fits',\
    'M6.0': 11182, #'11182_10188.fits',\
    'M7.0': 10822, #'10822_11283.fits',\
    'M8.0': 10824, #'10824_11423.fits',\
    'M9.0': 10821, #'10821_11058.fits',\
    'L0.0': 10107, #'10107_10315.fits',\
    'L1.0': 11072, #'11072_11527.fits',\
    'L2.0': 10600, #'10600_10957.fits',\
    'L3.0': 10592, #'10592_11111.fits',\
    'L4.0': 10675, #'10675_11572.fits',\
    'L5.0': 10351, #'10351_10583.fits',\
    'L6.0': 10375, #'10375_10696.fits',\
    'L7.0': 10678, #'10678_10105.fits',\
    'L8.0': 10115, #'10115_11254.fits',\
    'L9.0': 10268, #'10268_10237.fits',\
    'T0.0': 10771, #'10771_10871.fits',\
    'T1.0': 10767, #'10767_10591.fits',\
    'T2.0': 10017, #'10017_10945.fits',\
    'T3.0': 10034, #'10034_10874.fits',\
    'T4.0': 10143, #'10143_11632.fits',\
    'T5.0': 10021, #'10021_11106.fits',\
    'T6.0': 10200, #'10200_11236.fits',\
    'T7.0': 10159, #'10159_10513.fits',\
    'T8.0': 10126, #'10126_10349.fits',\
    'T9.0': 11536} #'11536_10509.fits'}
# EMPTY DICTIONARY

# subdwarf spectral standards
STDS_SD_SPEX_KEYS = { \
    'sdM5.5': 11670, #'11670_11134.fits',\
    'sdM6.0': 10265, #'10265_10045.fits',\
    'sdM7.0': 10197, #'10197_11074.fits',\
    'sdM8.0': 10123, #'10123_10145.fits',\
    'sdM9.5': 10188, #'10188_10700.fits',\
    'sdL0.0': 11972, #'11972_10248.fits',\
    'sdL3.5': 10364, #'10364_10946.fits',\
    'sdL4.0': 10203} #'10203_11241.fits'}
# EMPTY DICTIONARY

# extreme subdwarf spectral standards
STDS_ESD_SPEX_KEYS = { \
    'esdM5.0': 10229, #'10229_10163.fits',\
#    'esdM6.5': '_10579.fits',\
    'esdM7.0': 10521, #'10521_10458.fits',\
    'esdM8.5': 10278} #'10278_10400.fits'}
# EMPTY DICTIONARY

# filters
FILTERS = { \
    '2MASS_J': {'file': 'j_2mass.txt', 'description': '2MASS J-band', 'zeropoint': 1594.0}, \
    '2MASS_H': {'file': 'h_2mass.txt', 'description': '2MASS H-band', 'zeropoint': 1024.0}, \
    '2MASS_KS': {'file': 'ks_2mass.txt', 'description': '2MASS Ks-band', 'zeropoint': 666.7}, \
    '2MASS_K': {'file': 'ks_2mass.txt', 'description': '2MASS Ks-band', 'zeropoint': 666.7}, \
    '2MASS_Ks': {'file': 'ks_2mass.txt', 'description': '2MASS Ks-band', 'zeropoint': 666.7}, \
    'BESSEL_I': {'file': 'bessel_i.txt', 'description': 'Bessel I-band', 'zeropoint': 2405.3}, \
    'HAWK_Y': {'file': 'hawk-y.txt', 'description': 'HAWK Y-band', 'zeropoint': 2092.9}, \
    'HAWK_J': {'file': 'hawk-j.txt', 'description': 'HAWK J-band', 'zeropoint': 1543.5}, \
    'HAWK_H': {'file': 'hawk-h.txt', 'description': 'HAWK H-band', 'zeropoint': 1053.6}, \
    'HAWK_H2': {'file': 'hawk-h2.txt', 'description': 'HAWK H2-band', 'zeropoint': 688.8}, \
    'HAWK_CH4': {'file': 'hawk-ch4.txt', 'description': 'HAWK CH4-band', 'zeropoint': 1093.4}, \
    'HAWK_KS': {'file': 'hawk-ks.txt', 'description': 'HAWK Ks-band', 'zeropoint': 675.3}, \
    'HAWK_BRG': {'file': 'hawk-brg.txt', 'description': 'HAWK Brackett Gamma', 'zeropoint': 638.9}, \
    'HAWK_NB1060': {'file': 'hawk-nb1060.txt', 'description': 'HAWK Narrow Band 1060', 'zeropoint': 2003.27}, \
    'HAWK_NB1190': {'file': 'hawk-nb1190.txt', 'description': 'HAWK Narrow Band 1190', 'zeropoint': 1697.50}, \
    'HAWK_NB2090': {'file': 'hawk-nb2090.txt', 'description': 'HAWK Narrow Band 2090', 'zeropoint': 706.68}, \
    'FOURSTAR_J': {'file': 'fourstar-j.txt', 'description': 'FOURSTAR J-band', 'zeropoint': 1581.2}, \
    'FOURSTAR_J1': {'file': 'fourstar-j1.txt', 'description': 'FOURSTAR J1-band', 'zeropoint': 1978.7}, \
    'FOURSTAR_J2': {'file': 'fourstar-j2.txt', 'description': 'FOURSTAR J2-band', 'zeropoint': 1774.5}, \
    'FOURSTAR_J3': {'file': 'fourstar-j3.txt', 'description': 'FOURSTAR J3-band', 'zeropoint': 1488.8}, \
    'FOURSTAR_H': {'file': 'fourstar-h.txt', 'description': 'FOURSTAR H-band', 'zeropoint': 1054.9}, \
    'FOURSTAR_H_SHORT': {'file': 'fourstar-hshort.txt', 'description': 'FOURSTAR H short', 'zeropoint': 1119.1}, \
    'FOURSTAR_H_LONG': {'file': 'fourstar-hlong.txt', 'description': 'FOURSTAR H long', 'zeropoint': 980.7}, \
    'FOURSTAR_K': {'file': 'fourstar-j.txt', 'description': 'FOURSTAR Ks-band', 'zeropoint': 675.7}, \
    'FOURSTAR_KS': {'file': 'fourstar-j.txt', 'description': 'FOURSTAR Ks-band', 'zeropoint': 675.7}, \
    'IRAC_CH1': {'file': 'irac1.txt', 'description': 'IRAC Channel 1 (3.6 micron)', 'zeropoint': 280.9}, \
    'IRAC_CH2': {'file': 'irac2.txt', 'description': 'IRAC Channel 2 (4.5 micron)', 'zeropoint': 179.7}, \
    'IRAC_CH3': {'file': 'irac3.txt', 'description': 'IRAC Channel 3 (5.8 micron)', 'zeropoint': 115.0}, \
    'IRAC_CH4': {'file': 'irac4.txt', 'description': 'IRAC Channel 4 (8.0 micron)', 'zeropoint': 64.13}, \
    'MKO_J_ATM': {'file': 'j_atm_mko.txt', 'description': 'MKO J-band + atmosphere', 'zeropoint': 1562.3}, \
    'MKO_H_ATM': {'file': 'h_atm_mko.txt', 'description': 'MKO H-band + atmosphere', 'zeropoint': 1045.9}, \
    'MKO_K_ATM': {'file': 'k_atm_mko.txt', 'description': 'MKO K-band + atmosphere', 'zeropoint': 647.7}, \
    'MKO_J': {'file': 'mko_j.txt', 'description': 'MKO J-band + atmosphere', 'zeropoint': 1562.3}, \
    'MKO_H': {'file': 'mko_h.txt', 'description': 'MKO H-band + atmosphere', 'zeropoint': 1045.9}, \
    'MKO_K': {'file': 'mko_ks.txt', 'description': 'MKO K-band', 'zeropoint': 647.7}, \
    'MKO_KP': {'file': 'mko_kp.txt', 'description': 'MKO Kp-band', 'zeropoint': 693.7}, \
    'MKO_LP': {'file': 'mko_lp.txt', 'description': 'MKO Lp-band', 'zeropoint': 248.3}, \
    'MKO_MP': {'file': 'mko_mp.txt', 'description': 'MKO Mp-band', 'zeropoint': 164.7}, \
    'NICMOS_F090M': {'file': 'nic1_f090m.txt', 'description': 'NICMOS F090M', 'zeropoint': 2255.0}, \
    'NICMOS_F095N': {'file': 'nic1_f095n.txt', 'description': 'NICMOS F095N', 'zeropoint': 2044.6}, \
    'NICMOS_F097N': {'file': 'nic1_f097n.txt', 'description': 'NICMOS F097N', 'zeropoint': 2275.4}, \
    'NICMOS_F108N': {'file': 'nic1_f108n.txt', 'description': 'NICMOS F108N', 'zeropoint': 1937.3}, \
    'NICMOS_F110M': {'file': 'nic1_f110m.txt', 'description': 'NICMOS F110M', 'zeropoint': 1871.8}, \
    'NICMOS_F110W': {'file': 'nic1_f110w.txt', 'description': 'NICMOS F110W', 'zeropoint': 1768.5}, \
    'NICMOS_F113N': {'file': 'nic1_f113n.txt', 'description': 'NICMOS F113N', 'zeropoint': 1821.0}, \
    'NICMOS_F140W': {'file': 'nic1_f140w.txt', 'description': 'NICMOS F140W', 'zeropoint': 1277.1}, \
    'NICMOS_F145M': {'file': 'nic1_f145m.txt', 'description': 'NICMOS F145M', 'zeropoint': 1242.0}, \
    'NICMOS_F160W': {'file': 'nic1_f160w.txt', 'description': 'NICMOS F160W', 'zeropoint': 1071.7}, \
    'NICMOS_F164N': {'file': 'nic1_f164n.txt', 'description': 'NICMOS F164N', 'zeropoint': 1003.0}, \
    'NICMOS_F165M': {'file': 'nic1_f165m.txt', 'description': 'NICMOS F165M', 'zeropoint': 1023.6}, \
    'NICMOS_F166N': {'file': 'nic1_f166n.txt', 'description': 'NICMOS F166N', 'zeropoint': 1047.7}, \
    'NICMOS_F170M': {'file': 'nic1_f170m.txt', 'description': 'NICMOS F170M', 'zeropoint': 979.1}, \
    'NICMOS_F187N': {'file': 'nic1_f187n.txt', 'description': 'NICMOS F187N', 'zeropoint': 803.7}, \
    'NICMOS_F190N': {'file': 'nic1_f190n.txt', 'description': 'NICMOS F190N', 'zeropoint': 836.5}, \
    'NIRC2_J': {'file': 'nirc2-j.txt', 'description': 'NIRC2 J-band', 'zeropoint': 1562.7}, \
    'NIRC2_H': {'file': 'nirc2-h.txt', 'description': 'NIRC2 H-band', 'zeropoint': 1075.5}, \
    'NIRC2_HCONT': {'file': 'nirc2-hcont.txt', 'description': 'NIRC2 H-continuum band', 'zeropoint': 1044.5}, \
    'NIRC2_K': {'file': 'nirc2-k.txt', 'description': 'NIRC2 K-band', 'zeropoint': 648.9}, \
    'NIRC2_KP': {'file': 'nirc2-kp.txt', 'description': 'NIRC2 Kp-band', 'zeropoint': 689.3}, \
    'NIRC2_KS': {'file': 'nirc2-ks.txt', 'description': 'NIRC2 Ks-band', 'zeropoint': 676.2}, \
    'NIRC2_KCONT': {'file': 'nirc2-kcont.txt', 'description': 'NIRC2 K continuum-band', 'zeropoint': 605.9}, \
    'NIRC2_FE2': {'file': 'nirc2-fe2.txt', 'description': 'NIRC2 Fe II', 'zeropoint': 1019.7}, \
    'NIRC2_LP': {'file': 'nirc2-lp.txt', 'description': 'NIRC2 LP', 'zeropoint': 248.0}, \
    'NIRC2_M': {'file': 'nirc2-ms.txt', 'description': 'NIRC2 M', 'zeropoint': 165.8}, \
    'PANSTARRS_I': {'file': 'panstarrs-i.txt', 'description': 'PANSTARRS i-band', 'zeropoint': 2584.6}, \
    'PANSTARRS_Z': {'file': 'panstarrs-z.txt', 'description': 'PANSTARRS z-band', 'zeropoint': 2584.6}, \
    'PANSTARRS_Y': {'file': 'panstarrs-y.txt', 'description': 'PANSTARRS y-band', 'zeropoint': 2584.6}, \
    'UKIDSS_Z': {'file': 'ukidss-z.txt', 'description': 'UKIDSS Z-band', 'zeropoint': 2261.4}, \
    'UKIDSS_Y': {'file': 'ukidss-y.txt', 'description': 'UKIDSS Y-band', 'zeropoint': 2057.2}, \
    'UKIDSS_J': {'file': 'ukidss-j.txt', 'description': 'UKIDSS J-band', 'zeropoint': 1556.8}, \
    'UKIDSS_H': {'file': 'ukidss-h.txt', 'description': 'UKIDSS H-band', 'zeropoint': 1038.3}, \
    'UKIDSS_K': {'file': 'ukidss-k.txt', 'description': 'UKIDSS K-band', 'zeropoint': 644.1}, \
    'VISTA_Z': {'file': 'vista_z.txt', 'description': 'VISTA Z-band', 'zeropoint': 2263.81}, \
    'VISTA_Y': {'file': 'vista_y.txt', 'description': 'VISTA Y-band', 'zeropoint': 2087.32}, \
    'VISTA_J': {'file': 'vista_j.txt', 'description': 'VISTA J-band', 'zeropoint': 1554.03}, \
    'VISTA_H': {'file': 'vista_h.txt', 'description': 'VISTA H-band', 'zeropoint': 1030.40}, \
    'VISTA_KS': {'file': 'vista_ks.txt', 'description': 'VISTA Ks-band', 'zeropoint': 674.83}, \
    'WFC3_F127M': {'file': 'wfc3_F127M.txt', 'description': 'WFC3 F127M', 'zeropoint': 2261.3}, \
    'WFC3_F139M': {'file': 'wfc3_F139M.txt', 'description': 'WFC3 F139M', 'zeropoint': 2261.3}, \
    'WFC3_F164N': {'file': 'wfc3_F164N.txt', 'description': 'WFC3 F164N', 'zeropoint': 2261.3}, \
    'WFC3_F167N': {'file': 'wfc3_F167N.txt', 'description': 'WFC3 F167N', 'zeropoint': 2261.3}, \
    'WFCAM_Z': {'file': 'wfcam-z.txt', 'description': 'UKIRT WFCAM Z', 'zeropoint': 2261.3}, \
    'WFCAM_Y': {'file': 'wfcam-y.txt', 'description': 'UKIRT WFCAM Y', 'zeropoint': 2040.9}, \
    'WFCAM_J': {'file': 'wfcam-j.txt', 'description': 'UKIRT WFCAM J', 'zeropoint': 1548.7}, \
    'WFCAM_H': {'file': 'wfcam-h.txt', 'description': 'UKIRT WFCAM H', 'zeropoint': 1027.1}, \
    'WFCAM_H2': {'file': 'wfcam-h2.txt', 'description': 'UKIRT WFCAM H2', 'zeropoint': 677.1}, \
    'WFCAM_BRG': {'file': 'wfcam-brg.txt', 'description': 'UKIRT WFCAM Brackett Gamma', 'zeropoint': 645.5}, \
    'WFCAM_K': {'file': 'wfcam-k.txt', 'description': 'UKIRT WFCAM K', 'zeropoint': 630.0}, \
    'WIRCAM_Y': {'file': 'wircam-cfht-y.txt', 'description': 'CFHT WIRCAM Y', 'zeropoint': 2073.32}, \
    'WIRCAM_J': {'file': 'wircam-cfht-j.txt', 'description': 'CFHT WIRCAM J', 'zeropoint': 1551.01}, \
    'WIRCAM_H': {'file': 'wircam-cfht-h.txt', 'description': 'CFHT WIRCAM H', 'zeropoint': 1044.35}, \
    'WIRCAM_KS': {'file': 'wircam-cfht-ks.txt', 'description': 'CFHT WIRCAM Ks', 'zeropoint': 674.62}, \
    'WIRCAM_KCONT': {'file': 'wircam-cfht-kcont.txt', 'description': 'CFHT WIRCAM K-cont', 'zeropoint': 636.17}, \
    'WIRCAM_CH4_OFF': {'file': 'wircam-cfht-ch4s.txt', 'description': 'CFHT WIRCAM CH4-off', 'zeropoint': 987.39}, \
    'WIRCAM_CH4_ON': {'file': 'wircam-cfht-ch4l.txt', 'description': 'CFHT WIRCAM CH4-on', 'zeropoint': 1076.31}, \
    'WIRC_J': {'file': 'wirc_jcont.txt', 'description': 'WIRC J-cont', 'zeropoint': 0.}, \
    'WIRC_H': {'file': 'wirc_hcont.txt', 'description': 'WIRC H-cont', 'zeropoint': 0.}, \
    'WIRC_K': {'file': 'wirc_kcont.txt', 'description': 'WIRC K-cont', 'zeropoint': 0.}, \
    'WIRC_CO': {'file': 'wirc_co.txt', 'description': 'WIRC CO', 'zeropoint': 0.}, \
    'WIRC_CH4S': {'file': 'wirc_ch4s.txt', 'description': 'WIRC CH4S', 'zeropoint': 0.}, \
    'WIRC_CH4L': {'file': 'wirc_ch4l.txt', 'description': 'WIRC CH4L', 'zeropoint': 0.}, \
    'WIRC_FE2': {'file': 'wirc_feii.txt', 'description': 'WIRC Fe II', 'zeropoint': 0.}, \
    'WIRC_BRGAMMA': {'file': 'wirc_brgamma.txt', 'description': 'WIRC H I Brackett Gamma', 'zeropoint': 0.}, \
    'WIRC_PABETA': {'file': 'wirc_pabeta.txt', 'description': 'WIRC H I Paschen Beta', 'zeropoint': 0.}, \
    'WISE_W1': {'file': 'wise_w1.txt', 'description': 'WISE W1 (3.5 micron)', 'zeropoint': 309.54}, \
    'WISE_W2': {'file': 'wise_w2.txt', 'description': 'WISE W2 (4.6 micron)', 'zeropoint': 171.79}, \
    'WISE_W3': {'file': 'wise_w3.txt', 'description': 'WISE W3 (13 micron)', 'zeropoint': 31.67}, \
    'WISE_W4': {'file': 'wise_w4.txt', 'description': 'WISE W4 (22 micron)', 'zeropoint': 8.363} \
    }

# some data formats (for future expansion)
INSTRUMENTS = {
	'SPEX': {'pixel_scale': 0.15*u.arcsec, 'wave_range': [0.8,2.5]*u.micron, 'slit_width': 0.3*u.arcsec, 'resolution': 200, 'norders': 1, 'readnoise': 12, 'dark_current': 0.2, 'gain': 12},
	'SPEX_PRISM': {'pixel_scale': 0.15*u.arcsec, 'wave_range': [0.8,2.4]*u.micron, 'slit_width': 0.3*u.arcsec, 'resolution': 2000, 'norders': 1, 'readnoise': 12, 'dark_current': 0.2, 'gain': 12},
	'SPEX_SXD': {'pixel_scale': 0.15*u.arcsec, 'wave_range': [0.8,2.5]*u.micron, 'slit_width': 0.3*u.arcsec, 'resolution': 200, 'norders': 7, 'readnoise': 12, 'dark_current': 0.2, 'gain': 12},
	'USPEX': {'pixel_scale': 0.10*u.arcsec, 'wave_range': [0.7,2.5]*u.micron, 'slit_width': 0.3*u.arcsec, 'resolution': 200, 'norders': 1, 'readnoise': 5, 'dark_current': 0.05, 'gain': 1.5},
	'USPEX_PRISM': {'pixel_scale': 0.10*u.arcsec, 'wave_range': [0.7,2.5]*u.micron, 'slit_width': 0.3*u.arcsec, 'resolution': 200, 'norders': 1, 'readnoise': 5, 'dark_current': 0.05, 'gain': 1.5},
	'USPEX_SXD': {'pixel_scale': 0.15*u.arcsec, 'wave_range': [0.7,2.55]*u.micron, 'slit_width': 0.3*u.arcsec, 'resolution': 200, 'norders': 7, 'readnoise': 5, 'dark_current': 0.05, 'gain': 1.5},
}

# spectral model information
MODEL_PARAMETER_NAMES = ['teff','logg','z','fsed','cld','kzz','slit']
MODEL_PARAMETERS = {'teff': 1000.0,'logg': 5.0,'z': 0.0,'fsed':'nc','cld':'nc','kzz':'eq','slit':0.5}
MODEL_PARAMETER_TITLES = {\
    'teff': '$T_{eff}$',\
    'logg': '$log\ g$',\
    'z': '$[M/H]$',\
    'fsed': '$f_{sed}$',\
    'cld': '$cld$',\
    'kzz': '$log\ \kappa_{zz}$',\
    'slit': '$slit$'}
#MODEL_PARAMETER_UNITS = [u.K,u.cm/u.s/u.s,u.m/u.m,u.m/u.m,u.m/u.m,u.m/u.m,u.arcsec]
MODEL_PARAMETER_UNITS = {\
    'teff': u.K, \
    'logg': u.dex(u.cm/u.s/u.s), \
    'z': u.dex(), \
    'fsed': u.m/u.m, \
    'cld': u.m/u.m, \
    'kzz': u.m/u.m, \
#    'kzz': u.dex(u.cm*u.cm/u.s), \
    'slit': u.arcsec}
DEFINED_MODEL_SET = ['BTSettl2008','burrows06','morley12','morley14','saumon12','drift']
DEFINED_MODEL_NAMES = {
    'BTSettl2008': 'BT-Settl (2008)',\
    'burrows06': 'Burrows et al. (2006)',\
    'morley12': 'Morley et al. (2012)',\
    'morley14': 'Morley et al. (2014)',\
    'saumon12': 'Saumon et al. (2012)',\
    'drift': 'Witte et al. (2011)'}
DEFINED_MODEL_SETS = {\
    'BTSettl2008': ['allard','allard12','allard2012','btsettl','btsettled'], \
    'burrows06': ['burrows','burrows2006'], \
    'morley12': ['morley','morley2012'], \
    'morley14': ['morley2014'], \
    'saumon12': ['saumon','saumon2012'], \
    'drift': ['witte','witte11','witte2011','helling']}
DEFINED_MODEL_BIBCODES = {\
    'BTSettl2008': '2012RSPTA.370.2765A', \
    'burrows06': '2006ApJ...640.1063B',\
    'morley12': '2012ApJ...756..172M',\
    'morley14': '2014ApJ...787...78M',\
    'saumon12': '2012ApJ...750...74S',\
    'drift': '2011A&A...529A..44W'}

