#!/usr/bin/pythoni
from multiprocessing import Process,Value
import time
import errno    
import sys
import os
from os import path   
import download as DL

import subprocess
import shutil
def execute(command):

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while process.poll() is None:
        nextline = process.stdout.readline()
        sys.stdout.write(nextline)


def main(argv):

    date=argv[0] #"20170428" #enter dates between previous 2 years
    simu_starttime=argv[1]#"00"  #00 06 12 18
    folder="NOAA_SRC"
    output_directory=folder+"/"+date+"_"+simu_starttime
    origin_folder =output_directory+"/grib2"
    username = "peggy.lu@northwestern.edu"
    passwd="1234"
    year=date[0:4]
    number_str="000"
    #user authorized
    authen_command = 'wget --no-check-certificate -O Authentication.log --save-cookies auth.rda_ucar_edu --post-data="email='+username+'&passwd='+passwd+'&action=login" https://rda.ucar.edu/cgi-bin/login '
    #execute(authen_command)
    os.system(authen_command)


    DL.download(folder,date,simu_starttime)
    
#    url="http://rda.ucar.edu/data/ds084.1/"+year+"/"+date+"/gfs.0p25."+date+simu_starttime+".f"+number_str+".grib2"
#    print("starting to download "+url+".....")
#    wget_command = 'wget -N --no-check-certificate --load-cookies auth.rda_ucar_edu '+url
#    os.system(wget_command)


    #check data number
    time.sleep(3)

    client_user="peggy"
    client_ip="140.110.141.141"
    #client_ip="10.7.50.205"
    client_folder="~/origin"
    #client_ip="165.124.158.52"
    #client_folder="~/NCHC_simu"
    scp_cmd = "scp -r "+output_directory+ " "+client_user+"@"+client_ip+":"+client_folder
    print(scp_cmd)
    os.system(scp_cmd)


if __name__ == "__main__":
   main(sys.argv[1:])
