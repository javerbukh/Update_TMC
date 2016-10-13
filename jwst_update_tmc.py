from astropy.io import fits
import os
import re
import csv
import argparse

def check_usability(hdulist):
    """
    Checks to make sure all necessary headers are present
    """
    status = True

    if 'INSTRUME' in hdulist[0].header:
        if change_style(hdulist[0].header['INSTRUME']):
            pass
        else:
            print ("Not a valid value for INSTRUME: {}".format(hdulist[0].header['INSTRUME']))
            status = False
    else:
        print ("Missing INSTRUME header in file ")
        status = False
    if 'REFTYPE' in hdulist[0].header:
        pass
    else:
        print ("Missing REFTYPE header in file ")
        status = False

def get_file_headers(hdulist):
    """
    Returns header values for the most frequently accessed headers
    """
    if 'TELESCOP' in hdulist[0].header:
        get_instrume = hdulist[0].header['INSTRUME']
        get_telescop = hdulist[0].header['TELESCOP']
        get_reftype = hdulist[0].header['REFTYPE']
        return (get_instrume, get_telescop, get_reftype)
    else:
        get_instrume = hdulist[0].header['INSTRUME']
        get_telescop = False
        get_reftype = hdulist[0].header['REFTYPE']
        return (get_instrume, get_telescop, get_reftype)

hdulist = fits.open("0661429jm_tmc.fits")
print (hdulist.info())

print (hdulist[0].header)

hdulist2 = fits.open("jwst_nircam_h2rg_ipckernel_20160902164019.fits")
print (hdulist2.info())

valid_values = {'INSTRUME':'JWST', 'DBTABLE': 'CRCOMPLIST', 'DESCRIP': '', 'PEDIGREE': ['GROUND', 'DUMMY', 'INFLIGHT']\
    'AUTHOR': '', 'HISTORY': ''}
