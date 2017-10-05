#load function first
import time
import errno    
import sys
import os
from os import path   


def rm_file_in_folder(path):
    filelist = [ f for f in os.listdir(path) ]
    for f in filelist:
        os.remove(path+"/"+f)
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

    
    
#import sys, getopt
import matplotlib.pyplot as plt
import netCDF4
import numpy as np

def plot(inputfile,refFile,outputfile):        

        nc = netCDF4.Dataset(inputfile,mode='r')

        # examine the variables
        #print nc.variables.keys()
        #print nc.variables['Band1']

        # sample every 10th point of the 'z' variable
        topo = nc.variables['Band1'][2::,2::]
        if refFile!="null" and isinstance(topo,np.ma.MaskedArray):
            refnc = netCDF4.Dataset(refFile,mode='r')
            refdata = refnc.variables['Band1'][2::,2::]
            topo[topo.mask]=refdata[topo.mask]

        # make image
        plt.figure(figsize=(10,10))
        plt.imshow(topo,origin='lower',cmap='jet')
        #plt.title(nc.title)
        plt.tight_layout()
        plt.savefig(outputfile, bbox_inches='tight')
#        plt.cla()
        plt.clf()
        plt.close()       
import subprocess
import shutil
def execute(command):

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while process.poll() is None:
        nextline = process.stdout.readline()
        sys.stdout.write(nextline)
        time.sleep(1)  
        #sys.stdout.flush()
        #print(output, end='')

def authenticate(username,passwd):
 #user authorized
    authen_command = 'wget --no-check-certificate -O Authentication.log --save-cookies auth.rda_ucar_edu --post-data="email='+username+'&passwd='+passwd+'&action=login" https://rda.ucar.edu/cgi-bin/login '
    execute(authen_command)
