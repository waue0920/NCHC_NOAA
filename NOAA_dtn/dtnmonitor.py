import itertools
import psutil
import time
import sys, os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import threading
from IPython import display
import csv
import utilities as util
from multiprocessing import Process
filename="initialize....."
class Graph(threading.Thread):
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
#        global filename
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup
        while not self.killed:
            network_monitor_list = []
            diskio_monitor_list = []
            cup_monitor_list = []
            mem_monitor_list = []
            with open('monitor') as f:
                # for line in f:
                #    monitor_list.append(line.strip())
                reader1, reader2 = itertools.tee(csv.reader(f, delimiter=","))
                for row in reader2:
                    if(len(next(reader1)) != 4):
                        continue

#                for row in csv.DictReader(f, ['network', 'diskio', 'cpu', 'mem']):
 #                   if(len(row) !=4):
  #                      continue
                    
                    network_monitor_list.append(row[0].strip())
                    diskio_monitor_list.append(row[1].strip())
                    cup_monitor_list.append(row[2].strip())
                    mem_monitor_list.append(row[3].strip())
            # print network_monitor_list
            netarr = np.array(network_monitor_list, dtype=float)
            diskarr = np.array(diskio_monitor_list, dtype=float)
            cpuarr = np.array(cup_monitor_list, dtype=float)
            memarr = np.array(mem_monitor_list, dtype=float)
            # fig , ax= plt.subplots(dpi=80)
            # f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row')
            f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col')
            f.set_size_inches(15, 10)
            f.suptitle(filename, fontsize=30)
            ax1.plot(((netarr / 1024)))
            ax1.grid(alpha=0.5)
            ax1.set_title("Network Performance")
            ax1.set_xlabel('Sec')
            ax1.set_ylabel('Mb')

            ax2.plot(((diskarr / 1024)), color="green")
            ax2.grid(alpha=0.5)
            ax2.set_title("DISK IO")
            ax2.set_xlabel('Sec')
            ax2.set_ylabel('Mb')

            ax3.plot(((cpuarr)))
            ax3.grid(alpha=0.5)
            ax3.set_title("CPU Usage")
            ax3.set_xlabel('Sec')
            ax3.set_ylabel('Percentage')

            ax4.plot(((memarr)))
            ax4.grid(alpha=0.5)
            ax4.set_title("Memory Usage")
            ax4.set_xlabel('Sec')
            ax4.set_ylabel('Percentage')

            display.display(plt.show())
            display.clear_output(wait=True)
            # plt.show()
            time.sleep(0.5)

    def globaltrace(self, frame, why, arg):
        if why == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, why, arg):
        if self.killed:
            if why == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True


#def dtn2db():

#    while True:
#        proc1 = subprocess.Popen(["./dtnscript.sh"], shell=True, stdout=subprocess.PIPE)
	#proc1.kill()
#        time.sleep(5)



def monitorit(func):
    def my_wrap(*args, **kwargs):
 #       procmongo = Process(target=dtn2db)
        procmongo = subprocess.Popen(["python","calldtnscript.py"], stdin=subprocess.PIPE)

        mode=args[3]
#        print(mode)
#        procmongo.start()
 #       procmongo.join()
        proc = subprocess.Popen(["python", "bandw.py", str(mode)], stdout=subprocess.PIPE)
        time.sleep(1)

        thread = Graph()
        thread.daemon = True
        thread.start()
        out = func(*args, **kwargs)
        time.sleep(8)
        proc.kill()
        procmongo.kill()
        thread.kill()

    return my_wrap

def download(date,simu_starttime,folder):

    output_directory=folder+"/"+date+"_"+simu_starttime

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    origin_folder =output_directory+"/grib2"
    util.mkdir_p(origin_folder)

    year=date[0:4]

    number=0

    while (number <=384):  
        number_str=("%03d" %(number))
        url="http://rda.ucar.edu/data/ds084.1/"+year+"/"+date+"/gfs.0p25."+date+simu_starttime+".f"+number_str+".grib2"
        global filename
        filename="starting to download file "+date+" "+number_str
   #     print("starting to download "+url+".....")
        wget_command = 'wget -N --no-check-certificate --load-cookies auth.rda_ucar_edu '+url+" -P "+origin_folder
        #os.system(wget_command)
        cmd = wget_command.split()
        subprocess.call(cmd)
#        execute(wget_command)

        if (number<240):
            number=number+3
        else: 
            number=number+12


@monitorit
def exec_command(date,time,folder,input_mode):
#    mode=input_mode
#    cmd = cmd.split()
#    if cmd is not None:
#    global filename
#    filename="1234"
#    DL.authenticate(username,passwd)
    
    try:
        download(date,time,folder)
            #subprocess.call(cmd)
    except KeyboardInterrupt:
        print ('Interrupted')
        sys.exc_info() == (None, None, None)
#            sys.exc_clear()

@monitorit
def eos_exec_command(cmd, account, password):
    os.system("kinit {};{}".format(account,password))
    cmd = cmd.split()
    if cmd is not None:
        try:
            subprocess.call(cmd)
        except KeyboardInterrupt:
            print ('Interrupted')
            sys.exc_clear()
