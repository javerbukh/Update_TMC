from astropy.io import fits
import os
import argparse
import time
from datetime import date
import getpass
import sys
import numpy as np
import re
import jwst_update_dict
from shutil import copyfile
import operator

def check_filename(filename):
    """
    Uses the dictionary filename_to_ev to prepend a descriptive string to each
    filename, which states it's directory of origin, and returns the new filename
    """
    checker = False
    for k,v in jwst_update_dict.filename_to_ev.iteritems():
        if re.search(k,filename) != None:
            checker = True
            new_filename = v + "$" + filename
            return new_filename
    if not checker:
        print ("Path for {} not found, not able to prepend Environmental Variable to filename".format(filename))
        return filename

def get_all_files():
    """
    Gets all files from the pandeia directory, as well as all of its subdirectories.
    This then returns 4 arrays, one for each of the following attributes: time of
    access, file's compname, file's name, and the DESCRIP of the file
    """
    time_array = []
    compname = []
    filename_array = []
    comment = []

    all_files = {}
    all_instruments = ["miri/","nircam/","niriss/","nirspec/","telescope"]
    all_sub_dirs = ["blaze/","detector/","dispersion/","filters/","optical/","psfs/","qe/","wavepix/","xtras/"]
    old_directory = "/grp/hst/cdbs/work/jwst/delivery/pandeia/"
    for instr_dir in all_instruments:
        for instr_sub_dir in all_sub_dirs:
            if instr_dir != "telescope":
                directory = old_directory + instr_dir + instr_sub_dir
            else:
                directory = old_directory + instr_dir
            print (directory)
            if os.path.isdir(directory) or os.path.exists(directory):
                for filename in os.listdir(directory):
                    if filename.endswith(".fits"):
                        new_path = str(os.path.join(directory, filename))
                        all_files[new_path] = filename
    all_files = check_dup_comp_values(all_files)
    new_all_files = sorted(all_files.items(), key=operator.itemgetter(1))

    for df, f in new_all_files:
        print ("-------------------------------------------------------------")
        print ("Checking {}".format(f))

        (temp_time, temp_compname, temp_filename, temp_comment) = update_columns(df, f, "default")
        time_array.append(temp_time)
        compname.append(temp_compname)
        filename_array.append(temp_filename)
        comment.append(temp_comment)

    return (time_array, compname, filename_array, comment)

def get_all_files_chosen_dir(directory):
    """
    Gets all files from the pandeia directory, as well as all of its subdirectories.
    This then returns 4 arrays, one for each of the following attributes: time of
    access, file's compname, file's name, and the DESCRIP of the file
    """
    time_array = []
    compname = []
    filename_array = []
    comment = []

    all_files = {}
    if os.path.isdir(directory) or os.path.exists(directory):
        for filename in os.listdir(directory):
            if filename.endswith(".fits"):
                new_path = str(os.path.join(directory, filename))
                all_files[new_path] = filename
    all_files = check_dup_comp_values(all_files)
    for df, f in all_files.iteritems():
        print ("-------------------------------------------------------------")
        print ("Checking {}".format(f))

        (temp_time, temp_compname, temp_filename, temp_comment) = update_columns(df, f, "non_default")
        time_array.append(temp_time)
        compname.append(temp_compname)
        filename_array.append(temp_filename)
        comment.append(temp_comment)

    return (time_array, compname, filename_array, comment)

def check_dup_comp_values(all_files):
    """
    Checks to see if anyfiles within a certain directory contain duplicate COMPNAMEs
    """
    all_files_new = {}
    comp_with_filenames = {}
    for df,f in all_files.iteritems():
        hdulist = fits.open(df)
        if "COMPNAME" not in hdulist[0].header:
            print ("ERROR: COMPNAME not found in {}, exiting program".format(f))
            sys.exit()
        elif hdulist[0].header["COMPNAME"] not in comp_with_filenames:
            all_files_new[df] = f
            comp_with_filenames[hdulist[0].header["COMPNAME"]] = f
        else:
            print ("ERROR: {} and {} have same COMPNAME values, exiting program".format(f, comp_with_filenames[hdulist[0].header["COMPNAME"]]))
            sys.exit()
    return all_files_new

def check_valid_values(hdulist):
    """
    Checks to make sure all necessary headers are present
    """
    valid_values = {'INSTRUME':'JWST', 'DBTABLE': 'CRCOMPLIST', 'DESCRIP': 'A test TMC for JWST', 'PEDIGREE':'DUMMY',\
        'AUTHOR': 'Jesse A', 'HISTORY': 'Jesse added this test TMC file', 'COMPNAME':'acs_block1'}

    for key,value in valid_values.iteritems():
        if key in hdulist[0].header:
            if hdulist[0].header[key] == '' and value == '':
                hdulist[0].header[key] = "Testing"
            else:
                hdulist[0].header[key] = value
        else:
            hdulist[0].header[key] = value

    time=[]
    compname=[]
    filename=[]
    comment=[]
    col1= fits.Column(name='TIME', format='26A', array=time,
        disp='26A')
    col2= fits.Column(name='COMPNAME', format='18A', array=compname,
        disp='18A')
    col3= fits.Column(name='FILENAME', format='68A', array=filename,
        disp='68A')
    col4= fits.Column(name='COMMENT', format='68A', array=comment,
        disp='68A')

    cols=fits.ColDefs([col1,col2,col3,col4])
    tbhdu = fits.BinTableHDU.from_columns(cols)
    thdulist = fits.HDUList([hdulist[0],tbhdu])
    thdulist.writeto("testing_file2.fits", clobber = True)
    #hdulist.writeto("testing_file.fits", clobber = True)

def update_file(hdulist, writeto_file, is_test, time_array, compname_array, filename_array, comment):
    """
    Takes the 4 arrays created earlier and adds them to the new JWST_TMC file
    """
    test = False
    if is_test == "y":
        test = True

    tbdata = hdulist[1].data

    today = date.today()
    new_useafter = time.strftime("%b %d %Y") + " " + time.strftime("%H:%M:%S")
    hdulist[0].header["USEAFTER"] = new_useafter

    col1= fits.Column(name='TIME', format='26A', array=time_array,
        disp='26A')
    col2= fits.Column(name='COMPNAME', format='18A', array=compname_array,
        disp='18A')
    col3= fits.Column(name='FILENAME', format='68A', array=filename_array,
        disp='68A')
    col4= fits.Column(name='COMMENT', format='68A', array=comment,
        disp='68A')

    cols = fits.ColDefs([col1,col2,col3,col4])
    tbhdu = fits.BinTableHDU.from_columns(cols)

    if not test:
        username = raw_input("Please input your name: ")
        reason_for_change = raw_input("Please state the reason for this update: ")
        if username == "":
            username = getpass.getuser()
        hdulist[0].header["AUTHOR"] = username
        hdulist[0].header["HISTORY"] = reason_for_change

    thdulist = fits.HDUList([hdulist[0],tbhdu])
    thdulist.writeto(writeto_file, clobber = True)
    print ("A new TMC file {} has been created with data up-to-date as of {}".format("testing_file2.fits",new_useafter))

def update_columns(input_files_dir, input_files_name, is_default):
    """
    As the files are looped through, this method extracts information from the file,
    such as its COMPNAME, filename and DESCRIP, as well as the date and time this
    file was accessed
    """
    file_hdu = fits.open(input_files_dir)
    files_compname = file_hdu[0].header["COMPNAME"]

    today = date.today()
    new_useafter = time.strftime("%b %d %Y") + " " + time.strftime("%H:%M:%S")
    hdulist[0].header["USEAFTER"] = new_useafter

    return (new_useafter, file_hdu[0].header["COMPNAME"].lower(), check_filename(input_files_name), file_hdu[0].header["DESCRIP"])

################################################################################
# Main
################################################################################

parser = argparse.ArgumentParser()
parser.add_argument("chosen_directory", help="the directory of fits files to be run (type default for pandeia directories)")
parser.add_argument("old_tmc", help="the old tmc file")
parser.add_argument("new_tmc", help="the newer tmc file")
args = parser.parse_args()

hdulist = fits.open(args.old_tmc)

time_array = []
compname = []
filename_array = []
comment = []

is_test = raw_input("Is this a test? (y/n)")

if args.chosen_directory == "default":
    (time_array, compname, filename_array, comment) = get_all_files()
else:
    (time_array, compname, filename_array, comment) = get_all_files_chosen_dir(args.chosen_directory)

update_file(hdulist, args.new_tmc, is_test, time_array, compname, filename_array, comment)

print (hdulist[0].header)
print (hdulist[1].header)
