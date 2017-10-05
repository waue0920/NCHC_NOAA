#!/usr/bin/pythoni
from multiprocessing import Process,Value
import time
import errno    
import sys
import os
import subprocess
from os import path   

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

import subprocess
import shutil
def execute(command):

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while process.poll() is None:
        nextline = process.stdout.readline()
        sys.stdout.write(nextline)

def authenticate(username,passwd):
 #user authorized
    authen_command = 'wget --no-check-certificate -O Authentication.log --save-cookies auth.rda_ucar_edu --post-data="email='+username+'&passwd='+passwd+'&action=login" https://rda.ucar.edu/cgi-bin/login '
    execute(authen_command)
    
def main(argv):

    date=argv[0] #"20170428" #enter dates between previous 2 years
    simu_starttime=argv[1]#"00"  #00 06 12 18
    folder=argv[2]
   
    username = "peggy.lu@northwestern.edu"
    passwd="1234"

    authenticate(username,passwd)

   # download(folder,date,simu_starttime)


if __name__ == "__main__":
   main(sys.argv[1:])
