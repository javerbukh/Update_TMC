import re
import os
import argparse
from astropy.io import fits
import time
from datetime import date
import jwst_update_dict
from shutil import copy

################################################################################
# For testing purposes
def change_access_date(directory):
    for filename in os.listdir(directory):
        new_path = directory+filename
        print(new_path)
        hdulist = fits.open(new_path)
        today = date.today()
        new_useafter = time.strftime("%Y-%m-%d") + "T" + time.strftime("%H:%M:%S")
        #print (new_useafter)
        if "DATE" in hdulist[0].header:
            print (hdulist[0].header["DATE"])
            #hdulist[0].header["DATE"] = new_useafter
            #hdulist.writeto(new_path, clobber=True)

def send_files_to_new_directory(new_file, input_directory, dest_directory):
    if get_date(new_file) == False:
        print ("Time stamp not present in filename of {}".format(new_file))
        return False
    all_instruments = ["miri/","nircam/","niriss/","nirspec/","telescope"]
    all_sub_dirs = ["blaze/","detector/","dispersion/","filters/","optical/","psfs/","qe/","wavepix/","xtras/"]
    #old_directory = "/grp/hst/cdbs/work/jwst/delivery/pandeia/"
    old_directory = "/Users/javerbukh/Documents/Update_TMC/pandeia_test/"
    for instr_dir in all_instruments:
        for instr_sub_dir in all_sub_dirs:
            if instr_dir != "telescope":
                directory = old_directory + instr_dir + instr_sub_dir
            else:
                directory = old_directory + instr_dir
            if os.path.isdir(directory) or os.path.exists(directory):
                for filename in os.listdir(directory):
                    if new_file == filename:
                        old_path = directory+filename
                        old_hdu = fits.open(old_path)
                        new_path = input_directory + new_file
                        new_hdu = fits.open(new_path)
                        get_date(new_file)
                        #print ("New file: {}, old file: {}".format(new_hdu[0].header["DATE"], old_hdu[0].header["DATE"]))
                        #if new_hdu[0].header["DATE"] > old_hdu[0].header["DATE"]:
                        if get_date(new_file) > get_date(filename):
                            print ("File {} was moved to the Pandeia directory".format(new_file))
                            print (old_path)
                            print (new_path)
                            os.remove(old_path)
                            copy(new_path, directory)
                        #elif new_hdu[0].header["DATE"] == old_hdu[0].header["DATE"]:
                            #print ("WARNING: File {} has the same DATE as {}, no changes made".format(new_file, old_path))
                        else:
                            print ("WARNING: File {} is not newer than {}, file still replaced, however".format(new_file, old_path))
                            print (old_path)
                            print (new_path)
                            os.remove(old_path)
                            copy(new_path, directory)
                        print ("------------------------------------------------")


# For testing purposes
################################################################################

def get_date(filename):
    try:
        time_stamp = int(filename[-19:-5])
        return time_stamp
    except ValueError:
        return False

def check_filename(new_file, input_directory, dest_directory):
    """
    Uses the dictionary filename_to_ev to move the newest iteration of a files
    into the appropriate pandeia directory
    """
    if get_date(new_file) == False:
        print ("Time stamp not present in filename of {}".format(new_file))
        return False
    checker = False
    for k,v in jwst_update_dict.filename_to_ev.iteritems():
        if re.search(k,new_file) != None:
            checker = True
            #new_filename = v + "$" + new_file
            for filename_old in os.listdir(jwst_update_dict.file_to_pandeia[k]):
                if filename_old.endswith(".fits") and re.search(k,filename_old):
                    old_path = jwst_update_dict.file_to_pandeia[k]+filename_old
                    old_hdu = fits.open(old_path)
                    new_path = input_directory + new_file
                    new_hdu = fits.open(new_path)
                    #print ("New file date: {}; old file date: {}".format(new_hdu[0].header["DATE"], old_hdu[0].header["DATE"]))
                    #if new_hdu[0].header["DATE"] > old_hdu[0].header["DATE"]:
                    if get_date(new_file) > get_date(filename):
                        print ("File {} was moved to the Pandeia directory".format(new_file))
                        # print (old_path)
                        # print (new_path)
                        os.remove(old_path)
                        copy(new_path, jwst_update_dict.file_to_pandeia[k])
                        pass
                    #elif new_hdu[0].header["DATE"] == old_hdu[0].header["DATE"]:
                    #    print ("WARNING: File {} has the same DATE as {}, no changes made".format(new_file, old_path))
                    else:
                        print ("WARNING: File {} is not newer than {}, file still replaced, however".format(new_file, old_path))
                        # print (old_path)
                        # print (new_path)
                        os.remove(old_path)
                        copy(new_path, directory)
                    print ("---------------------------------------------------------------")

    if not checker:
        print ("ERROR: {} not matching any key in jwst_update_dict".format(new_file))

def get_files(input_directory):
    all_files= []
    for filename in os.listdir(input_directory):
        if filename.endswith(".fits"):
            all_files.append(filename)
    return all_files

def check_if_file_is_update(all_files, input_directory, dest_directory):
    for filename in all_files:
        check_filename(filename, input_directory, dest_directory)
        # Line below for testing purposes
        #send_files_to_new_directory(filename, input_directory, dest_directory)

################################################################################
# Main
################################################################################

parser = argparse.ArgumentParser()
parser.add_argument("input_directory", help="the directory of fits files to be sent")
parser.add_argument("dest_directory", help="(default = pandeia) the directory where the files in input_directory will be sent")
args = parser.parse_args()

all_files = get_files(args.input_directory)
check_if_file_is_update(all_files, args.input_directory, args.dest_directory)
