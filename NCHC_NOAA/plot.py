#!/usr/bin/python
import sys, getopt
import matplotlib.pyplot as plt
import netCDF4
def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('plot.py -i <inputfile> -o <outputfile>')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
    	    print('plot.py -i <inputfile> -o <outputfile>')
    	    sys.exit()
        elif opt in ("-i", "--ifile"):
    	    inputfile = arg
        elif opt in ("-o", "--ofile"):
    	    outputfile = arg
    # print 'Input file is "', inputfile
    # print 'Output file is "', outputfile
    
    nc = netCDF4.Dataset(inputfile,mode='r')
    
    # examine the variables
    #print nc.variables.keys()
    #print nc.variables['Band1']
    
    # sample every 10th point of the 'z' variable
    topo = nc.variables['Band1'][2::,2::]
    
    # make image
    plt.figure(figsize=(10,10))
    plt.imshow(topo,origin='lower',cmap='jet')
    #plt.title(nc.title)
    plt.tight_layout()
    plt.savefig(outputfile, bbox_inches='tight')
    plt.clf()
    plt.close()

if __name__ == "__main__":
   main(sys.argv[1:])

