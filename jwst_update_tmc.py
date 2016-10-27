from astropy.io import fits
import os
import argparse
import time
from datetime import date
import getpass
import sys
import numpy as np
import re

filename_to_ev = {
    #jwst nircam blaze
    'jwst_nircam_speceff':'crnircamblaze',
    #jwst nircam detector
    'jwst_nircam_h2rg_ipckernel':'crnircamdet',
    #jwst nircam dispersion
    'jwst_nircam_disp':'crnircamdisp',
    #jwst nircam filter
    'jwst_nircam_f070w_trans':'crnircamfilt',
    'jwst_nircam_f090w_trans':'crnircamfilt',
    'jwst_nircam_f115w_trans':'crnircamfilt',
    'jwst_nircam_f140m_trans':'crnircamfilt',
    'jwst_nircam_f150w2_trans':'crnircamfilt',
    'jwst_nircam_f150w_trans':'crnircamfilt',
    'jwst_nircam_f162m_trans':'crnircamfilt',
    'jwst_nircam_f164n_trans':'crnircamfilt',
    'jwst_nircam_f182m_trans':'crnircamfilt',
    'jwst_nircam_f187n_trans':'crnircamfilt',
    'jwst_nircam_f200w_trans':'crnircamfilt',
    'jwst_nircam_f210m_trans':'crnircamfilt',
    'jwst_nircam_f212n_trans':'crnircamfilt',
    'jwst_nircam_f250m_trans':'crnircamfilt',
    'jwst_nircam_f277w_trans':'crnircamfilt',
    'jwst_nircam_f300m_trans':'crnircamfilt',
    'jwst_nircam_f322w2_trans':'crnircamfilt',
    'jwst_nircam_f323n_trans':'crnircamfilt',
    'jwst_nircam_f335m_trans':'crnircamfilt',
    'jwst_nircam_f356w_trans':'crnircamfilt',
    'jwst_nircam_f360m_trans':'crnircamfilt',
    'jwst_nircam_f405n_trans':'crnircamfilt',
    'jwst_nircam_f410m_trans':'crnircamfilt',
    'jwst_nircam_f430m_trans':'crnircamfilt',
    'jwst_nircam_f444w_trans':'crnircamfilt',
    'jwst_nircam_f460m_trans':'crnircamfilt',
    'jwst_nircam_f466n_trans':'crnircamfilt',
    'jwst_nircam_f470n_trans':'crnircamfilt',
    'jwst_nircam_f480m_trans ':'crnircamfilt',
    'jwst_nircam_lw-lyot_trans_modmean':'crnircamfilt',
    'jwst_nircam_moda_com_substrate_trans':'crnircamfilt',
    'jwst_nircam_sw-lyot_trans_modmean':'crnircamfilt',
    #'jwst_nircam_optical'
    'jwst_nircam_internaloptics_throughput':'crnircamopt',
    'jwst_nircam_lw-lyot_trans_modmean':'crnircamopt',
    'jwst_nircam_lw_dbs':'crnircamopt',
    'jwst_nircam_moda_com_substrate_trans':'crnircamopt',
    'jwst_nircam_sw-lyot_trans_modmean':'crnircamopt',
    'jwst_nircam_sw_dbs':'crnircamopt',
    'jwst_nircam_wlp4':'crnircamopt',
    'jwst_nircam_wlp8':'crnircamopt',
    #'jwst_nircam_psfs' #none
    #'jwst_nircam_qe' #too many
    #jwst_niriss_blaze
    'jwst_niriss_gr150c-ordm1_speceff': 'crnirissblaze',
    'jwst_niriss_gr150c-ordp2_speceff': 'crnirissblaze',
    'jwst_niriss_gr150c-ordp3_speceff': 'crnirissblaze',
    'jwst_niriss_gr150r-ordm1_speceff': 'crnirissblaze',
    'jwst_niriss_gr150r-ordp1_speceff': 'crnirissblaze',
    'jwst_niriss_gr150r-ordp2_speceff': 'crnirissblaze',
    'jwst_niriss_gr150r-ordp3_speceff': 'crnirissblaze',
    'jwst_niriss_gr700xd-ord1_speceff': 'crnirissblaze',
    'jwst_niriss_gr700xd-ord2_speceff': 'crnirissblaze',
    'jwst_niriss_gr700xd-ord3_speceff': 'crnirissblaze',
    #jwst niriss dispersion
    'jwst_niriss_gr150c-ordm1_disp':'crnirissdet',
    'jwst_niriss_gr150c-ordp1_disp':'crnirissdet',
    'jwst_niriss_gr150c-ordp2_disp':'crnirissdet',
    'jwst_niriss_gr150c-ordp3_disp':'crnirissdet',
    'jwst_niriss_gr150r-ordm1_disp':'crnirissdet',
    'jwst_niriss_gr150r-ordp1_disp':'crnirissdet',
    'jwst_niriss_gr150r-ordp2_disp':'crnirissdet',
    'jwst_niriss_gr150r-ordp3_disp':'crnirissdet',
    'jwst_niriss_gr700xd-ord1_disp':'crnirissdet',
    'jwst_niriss_gr700xd-ord2_disp':'crnirissdet',
    'jwst_niriss_gr700xd-ord3_disp':'crnirissdet',
    #jwst niriss filters
    'jwst_niriss_f090w_trans':'crnirissdisp',
    'jwst_niriss_f115w_trans':'crnirissdisp',
    'jwst_niriss_f140m_trans':'crnirissdisp',
    'jwst_niriss_f150w_trans':'crnirissdisp',
    'jwst_niriss_f158m_trans':'crnirissdisp',
    'jwst_niriss_f200w_trans':'crnirissdisp',
    'jwst_niriss_f277w_trans':'crnirissdisp',
    'jwst_niriss_f356w_trans':'crnirissdisp',
    'jwst_niriss_f380m_trans':'crnirissdisp',
    'jwst_niriss_f430m_trans':'crnirissdisp',
    'jwst_niriss_f444w_trans':'crnirissdisp',
    'jwst_niriss_f480m_trans':'crnirissdisp',
    'jwst_niriss_nrm_trans':'crnirissdisp',
    #jwst niriss masks
    'jwst_niriss_soss-256-ord1_mask':'crnirissfilt',
    'jwst_niriss_soss-256-ord2_mask':'crnirissfilt',
    'jwst_niriss_soss-256-ord3_mask':'crnirissfilt',
    'jwst_niriss_soss-96-ord1_mask':'crnirissfilt',
    #jwsy niriss optical
    'jwst_niriss_internaloptics-clear_throughput':'crnirissopt',
    'jwst_niriss_internaloptics-clearp_throughput':'crnirissopt',
    'jwst_niriss_internaloptics_throughput':'crnirissopt',
    #'jwst_niriss_psfs' #None
    #jwst niriss qe
    'jwst_niriss_h2rg_qe':'crnirissqe',
    #jwst niriss wavepix
    'jwst_niriss_soss-256-ord1_trace':'crniriswave',
    'jwst_niriss_soss-256-ord2_trace':'crniriswave',
    'jwst_niriss_soss-256-ord3_trace':'crniriswave',
    'jwst_niriss_soss-96-ord1_trace':'crniriswave',
    'jwst_niriss_soss-96-ord2_trace':'crniriswave',
    'jwst_niriss_soss-96-ord3_trace':'crniriswave',
    #jwst niriss xtras #None
    #jwst telescope
    'jwst_telescope':'cttelescope'
}

def check_filename(filename):
    checker = False
    for k,v in filename_to_ev.iteritems():
        if re.search(k,filename) != None:
            checker = True
            new_filename = v + "$" + filename
            return new_filename
    if not checker:
        print ("Path for {} not found, not able to prepend Environmental Variable to filename".format(filename))
        return filename

def check_dup_comp_values(all_files):
    all_files_new = {}
    comp_with_filenames = {}
    for df,f in all_files.iteritems():
        hdulist = fits.open(df)
        if "COMPNAME" not in hdulist[0].header:
            print ("ERROR: COMPNAME not found in {}, exiting program".format(f))
            sys.exit()
            #Do not copy into new directory
            #COMPNAME not found in this file, sys.exit
            #Change filename length to 80
            pass
        elif hdulist[0].header["COMPNAME"] not in comp_with_filenames:
            all_files_new[df] = f
            comp_with_filenames[hdulist[0].header["COMPNAME"]] = f
        else:
            print ("ERROR: {} and {} have same COMPNAME values, exiting program".format(f, comp_with_filenames[hdulist[0].header["COMPNAME"]]))
            #sys.exit()
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
            #hdulist[0].header += str(key)
            hdulist[0].header[key] = value
    #tbdata = hdulist[1].data
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

def update_file(hdulist, is_test, time_array, compname_array, filename_array, comment):
    #file_hdu = fits.open(input_files_dir)
    test = False
    if is_test == "y":
        test = True

    compname = hdulist[0].header["COMPNAME"]
#####################LOOK HERE
# Need to figure out why you aren't able to append new compnames
# Why is it not getting to the else statement bellow?
    tbdata = hdulist[1].data
    #print (tbdata["COMPNAME"])
    #print ("adding")
    today = date.today()
    new_useafter = time.strftime("%b %d %Y") + " " + time.strftime("%H:%M:%S")
    hdulist[0].header["USEAFTER"] = new_useafter
    ############################################################################
    # print (len(filename))
    # print (len(tbdata['FILENAME']))
    # tbdata['TIME'].reshape = len(time_array)
    # tbdata['TIME'] = np.asarray(time_array)
    # tbdata['COMPNAME'].size(len(compname))
    # tbdata['COMPNAME'] = np.asarray(time_array)
    # tbdata['FILENAME'] = size(len(filename))
    # tbdata['FILENAME'] = np.asarray(filename)
    # tbdata['COMMENT'] = size(len(comment))
    # tbdata['COMMENT'] = np.asarray(comment)
    ############################################################################
    print (len(time_array), len(compname_array), len(filename_array), len(comment))
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

    ############################################################################
    # tbdata['TIME'] = np.append(new_useafter, tbdata['TIME'])
    # tbdata['COMPNAME'] = np.append(file_hdu[0].header["COMPNAME"], tbdata['COMPNAME'])
    # tbdata['FILENAME'] = np.append(check_filename(input_files_name), tbdata['FILENAME'])
    # tbdata['COMMENT'] = np.append(file_hdu[0].header["DESCRIP"], tbdata['COMMENT'])

    # print (tbdata["FILENAME"])
    print (len(tbdata["FILENAME"]))
    # print (tbdata["TIME"])
    # print (tbdata["COMPNAME"])
    # print (tbdata["COMMENT"])

    if not test:
        username = raw_input("Please input your name: ")
        reason_for_change = raw_input("Please state the reason for this update: ")
        if username == "":
            username = getpass.getuser()
        hdulist[0].header["AUTHOR"] = username
        hdulist[0].header["HISTORY"] = reason_for_change

    thdulist = fits.HDUList([hdulist[0],tbhdu])
    thdulist.writeto("testing_file2.fits", clobber = True)
    #hdulist.writeto("testing_file2.fits", clobber = True)
    print ("TMC file has created a new COMPNAME and has been updated with information from {}".format(input_files_name))

def update_columns(input_files_dir, input_files_name):
    file_hdu = fits.open(input_files_dir)
    files_compname = file_hdu[0].header["COMPNAME"]

    today = date.today()
    new_useafter = time.strftime("%b %d %Y") + " " + time.strftime("%H:%M:%S")
    hdulist[0].header["USEAFTER"] = new_useafter

    return (new_useafter, file_hdu[0].header["COMPNAME"], check_filename(input_files_name), file_hdu[0].header["DESCRIP"])
    #print (type(tbdata['FILENAME']))
    #compname_index_find = tbdata['COMPNAME'].find(files_compname)
    #testing_index = tbdata['COMPNAME'].find("acs_block1")
    #print ("testing_index: {}".format(testing_index))
    #print (compname_index_find)
    #compname_index = np.where(compname_index_find > -1)
    #print ("Index of where compname is: {}, {}".format(compname_index, files_compname))
    #print (len(compname_index), compname_index)
    # if files_compname in compname:
    #     today = date.today()
    #     new_useafter = time.strftime("%b %d %Y") + " " + time.strftime("%H:%M:%S")
    #     hdulist[0].header["USEAFTER"] = new_useafter
    #
    #     tbdata['TIME'][compname_index] = new_useafter
    #     #tbdata['COMPNAME'][compname_index] = file_hdu[0].header["COMPNAME"]
    #     tbdata['FILENAME'][compname_index] = check_filename(input_files_name)
    #     tbdata['COMMENT'][compname_index] = file_hdu[0].header["DESCRIP"]
    #
    #     # print (tbdata["FILENAME"])
    #     print (len(tbdata["FILENAME"]))
    #     # print (tbdata["TIME"])
    #     # print (tbdata["COMPNAME"])
    #     # print (tbdata["COMMENT"])
    #
    #     if not test:
    #         username = raw_input("Please input your name: ")
    #         reason_for_change = raw_input("Please state the reason for this update: ")
    #         if username == "":
    #             username = getpass.getuser()
    #         hdulist[0].header["AUTHOR"] = username
    #         hdulist[0].header["HISTORY"] = reason_for_change
    #
    #     hdulist.writeto("testing_file2.fits", clobber = True)
    #     print ("TMC file has been updated with information from {}".format(input_files_name))
    #else:




hdulist = fits.open("0661429jm_tmc.fits")
hdulist2 = fits.open("testing_file2.fits")
input_files_name = "jwst_nircam_h2rg_ipckernel_20160902164019.fits"
hdulist3 = fits.open("jwst_nircam_h2rg_ipckernel_20160902164019.fits")

hdulist2[0].header["COMPNAME"] = "acs_block1"

hdulist2.writeto("0661429jm_tmc.fits", clobber=True)
#print (hdulist.info())

#print (hdulist[0].header)
#check_valid_values(hdulist)
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
time_array = []
compname = []
filename_array = []
comment = []

is_test = raw_input("Is this a test? (y/n)")

all_files = {}
all_instruments = ["miri/","nircam/","niriss/","nirspec/","telescope"]
all_sub_dirs = ["blaze/","detector/","dispersion/","filters/","optical/","psfs/","qe/","wavepix/","xtras/"]
old_directory = "/grp/hst/cdbs/work/jwst/delivery/pandeia/"
for instr_dir in all_instruments:
    for instr_sub_dir in all_sub_dirs:
        directory = old_directory + instr_dir + instr_sub_dir
        print (directory)
        if os.path.isdir(directory) or os.path.exists(directory):
            for filename in os.listdir(directory):
                if filename.endswith(".fits") and filename != "testing_file.fits":
                    new_path = str(os.path.join(directory, filename))
                    all_files[new_path] = filename
all_files = check_dup_comp_values(all_files)
for df, f in all_files.iteritems():
    print ("-------------------------------------------------------------")
    print ("Checking {}".format(f))

    (temp_time, temp_compname, temp_filename, temp_comment) = update_columns(df, f)
    time_array.append(temp_time)
    compname.append(temp_compname)
    filename_array.append(temp_filename)
    comment.append(temp_comment)
# print (hdulist3[0].header)
# print (hdulist3[1].header)
update_file(hdulist2, is_test, time_array, compname, filename_array, comment)

print (compname)
print (hdulist2[0].header)
print (hdulist2[1].header)
