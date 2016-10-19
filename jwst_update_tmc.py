from astropy.io import fits
import os
import argparse
import time
from datetime import date
import getpass
import sys

def check_dup_comp_values(all_files):
    comp_with_filenames = {}
    for f in all_files:
        hdulist = fits.open(f)
        if hdulist[0].header["COMPNAME"] not in comp_with_filenames:
            comp_with_filenames[hdulist[0].header["COMPNAME"]] = f
        else:
            print ("{} and {} have same COMPNAME values".format(f, comp_with_filenames[hdulist[0].header["COMPNAME"]]))
            sys.exit()

def check_valid_values(hdulist):
    """
    Checks to make sure all necessary headers are present
    """
    valid_values = {'INSTRUME':'JWST', 'DBTABLE': 'CRCOMPLIST', 'DESCRIP': 'A test TMC for JWST', 'PEDIGREE':'DUMMY',\
        'AUTHOR': 'Jesse A', 'HISTORY': 'Jesse added this test TMC file', 'COMPNAME':'NIRCAM_detector'}

    for key,value in valid_values.iteritems():
        if key in hdulist[0].header:
            if hdulist[0].header[key] == '' and value == '':
                hdulist[0].header[key] = "Testing"
            else:
                hdulist[0].header[key] = value
        else:
            #hdulist[0].header += str(key)
            hdulist[0].header[key] = value
    hdulist.writeto("testing_file.fits", clobber = True)

def update_file(hdulist, input_files_name):
    file_hdu = fits.open(input_files_name)
    is_test = raw_input("Is this a test? (y/n)")
    test = False
    if is_test == "y":
        test = True
    if "COMPNAME" not in hdulist[0].header:
        print ("COMPNAME header not found")
        return False
    compname = hdulist[0].header["COMPNAME"]
    files_compname = file_hdu[0].header["COMPNAME"]

    if compname == files_compname:
        hdulist[1].header["TTYPE3"] = input_files_name
        hdulist[1].header["TTYPE4"] = "Updated FILENAME to " + input_files_name

        today = date.today()
        new_useafter = time.strftime("%Y-%m-%d") + "T" + time.strftime("%H:%M:%S")
        hdulist[0].header["USEAFTER"] = new_useafter
        #print (new_useafter)
        if not test:
            username = raw_input("Please input your name: ")
            reason_for_change = raw_input("Please state the reason for this update: ")
            if username == "":
                username = getpass.getuser()
            hdulist[0].header["AUTHOR"] = username
            hdulist[0].header["HISTORY"] = reason_for_change

        print ("TMC file has been updated with information from {}".format(input_files_name))

    pass


hdulist = fits.open("0661429jm_tmc.fits")
hdulist2 = fits.open("testing_file.fits")
input_files_name = "jwst_nircam_h2rg_ipckernel_20160902164019.fits"
#hdulist3 = fits.open("jwst_nircam_h2rg_ipckernel_20160902164019.fits")

hdulist.writeto("testing_file.fits", clobber=True)
print (hdulist.info())

print (hdulist[0].header)
check_valid_values(hdulist)
#update_file(hdulist2, input_files_name)


# print (hdulist3[0].header)
# print (hdulist3[1].header)

# parser = argparse.ArgumentParser()
# parser.add_argument("chosen_directory", help="the directory of fits files to be run")
# args = parser.parse_args()
#
# directory = args.chosen_directory
#directory = "/grp/crds/jwst/references/jwst/"
#irectory = "/user/rmiller/CDBS/testfile"
all_files = []
directory = "/Users/javerbukh/Documents/Update_TMC"
for filename in os.listdir(directory):
    if filename.endswith(".fits"):
        print ("Checking {}".format(filename))
        new_path = str(os.path.join(directory, filename))
        all_files.append(new_path)
check_dup_comp_values(all_files)
for f in all_files:
    update_file(hdulist2, f)
print (hdulist2[0].header)
print (hdulist2[1].header)
