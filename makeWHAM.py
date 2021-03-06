#!/home/kmm5/anaconda2/bin/python
#---------------------------------------------------------------------------------
# Generates WHAM configure file
# Date: 18 Sept 2017
# Author: Kareem Mehrabiani (Re-wrote Xingcheng's getHist.wham1d.umbre.py code)
#---------------------------------------------------------------------------------
import math;
import subprocess;
import os;
import shutil;
import sys;
import numpy as np
#---------------------------------------------------------------------------------
# ### Overview

# - [Functions](#Functions)
#     - [Wham Options](#Wham-Options)
#     - [DOS Write](#DOS-Write)
#     - [Free Energy Write](#Free-Energy-Write)
#     - [CV Write](#CV-Write)
#     - [Rxn Coord Binning](#E-and-Q-binning)

#---------------------------------------------------------------------------------
# ## Functions
#---------------------------------------------------------------------------------

# ### Wham Options
def whamOptions(whamdir, outfile, low_T, high_T, step_T, num_dimensions, threads):

    outfile.write("## WHAM Config File generated by makeWHAM.py\n")

    # Bin the temperatures
    num_of_tbin = int((high_T-low_T)/step_T + 0.5) + 1
    print('Bins: %d' % num_of_tbin)
    print('------------------')

    # WHAM options
    outfile.write("numDimensions %s\n" % num_dimensions)
    outfile.write("threads %s\n" % threads)
    
    kB = 0.008314
    outfile.write("kB %s\n" % kB)

    max_iterations = 100000
    tolerance = 0.0001

    outfile.write("maxIterations %s\n" % max_iterations)
    outfile.write("tolerance %s\n" % tolerance)
    return num_of_tbin


#---------------------------------------------------------------------------------
# ### DOS Write
def dosWrite(whamdir, outfile):
    # Density of States Calculation
    outfile.write("\n")
    outfile.write("## Density of States Calculation \n")
    outfile.write("run_wham \n")

    dos_file = whamdir + "/dos"
    outfile.write("dosFile %s\n" % dos_file)

#---------------------------------------------------------------------------------
# ### Free Energy Write
def freeEnergyWrite(whamdir, outfile, low_T, step_T, num_of_tbin):
    # For calculating free energy
    free_name = whamdir + "/free"
    subprocess.call(["mkdir", "-p", free_name])

    outfile.write("\n")
    outfile.write("## Free Energy Calculation \n")
    outfile.write("run_free \n")

    run_free_out = whamdir + "/free/"
    outfile.write("run_free_out %s\n" % run_free_out)

    start_TF = low_T
    delta_TF = step_T
    ntemps_F = 10*num_of_tbin

    outfile.write("startTF %s\n" % start_TF)
    outfile.write("deltaTF %s\n" % delta_TF)
    outfile.write("ntempsF %s\n" % ntemps_F)

#---------------------------------------------------------------------------------
# ### CV Write
def cvWrite(whamdir, outfile, low_T, step_T, num_of_tbin):
    # For calculating the heat capacity
    outfile.write("\n")
    outfile.write("## Heat Capacity Calculation \n")
    outfile.write("run_cv \n")

    run_cv_out = whamdir + "/cv"
    outfile.write("run_cv_out %s\n" % run_cv_out)

    start_T = low_T
    delta_T = step_T
    ntemps  = num_of_tbin

    outfile.write("startT %s\n" % start_T)
    outfile.write("deltaT %s\n" % delta_T)
    outfile.write("ntemps %s\n" % ntemps)

#---------------------------------------------------------------------------------
# ### E and Q binning
def binCoordWrite(whamdir, outfile, hist_name, low_T, high_T, step_T,
        least_Ene, most_Ene, least_Q, most_Q):

    # Here we calculate the number of files used
    num_files = 0

    for i in xrange(low_T, high_T+step_T, step_T):
        histfile = hist_name + ('run_%s/wham_input_%s.txt' % (i,i))
        num_files += 1
        energy, q_value = np.loadtxt(histfile, unpack=True)
        min_E = np.amin(energy)
        max_E = np.amax(energy)
        if min_E < least_Ene:
            least_Ene = min_E
        if max_E > most_Ene:
            most_Ene = max_E
        min_Q = np.min(q_value)
        max_Q = np.max(q_value)
        if min_Q < least_Q:
            least_Q = min_Q
        if max_Q > most_Q:
            most_Q = max_Q

    print("Smallest E: %d\nLargest E: %d" % (least_Ene, most_Ene))
    print('------------------')
    print("Smallest Q: %d\nLargest Q: %d" % (least_Q, most_Q))
    print('------------------')
    print("Number of files: %d" % num_files)

    step_E = 1.0
    step_Q = 1.0

    # Energy binning
    outfile.write("\n")
    outfile.write("## Energy Binning\n")
    num_ene_bins = int((most_Ene-least_Ene)/step_E + 0.5)
    outfile.write("numBins %s\n" % num_ene_bins)
    outfile.write("start %s\n" % least_Ene)
    outfile.write("step %s\n" % step_E)

    # Q binning
    precision = 1
    outfile.write("\n")
    outfile.write("## Q Binning\n")
    least_Q = round(least_Q, precision)
    num_q_bins = int((most_Q-least_Q)/step_Q + 0.5)
    outfile.write("numBins %s\n" % num_q_bins)
    outfile.write("start %s\n" % least_Q)
    outfile.write("step %s\n" % step_Q)
    
    # list of histogram filenames and their temperatures
    outfile.write("\n")
    outfile.write("numFiles %s\n" % num_files)
    for i in xrange(low_T, high_T+step_T, step_T):
        histfile = hist_name + ('run_%s/wham_input_%s.txt' % (i,i))
        outfile.write("name %s temp %s\n" % (histfile, i))

#---------------------------------------------------------------------------------
# Program Run
#---------------------------------------------------------------------------------
scratch_dir = "/dascratch/"
hist_name = scratch_dir + "/sbm/oda9mer/results_top45/step10e7/"
whamdir = "WHAM"
# Delete the previously existing wham file
subprocess.call(["rm", "-rf", whamdir])
# create a new wham file
subprocess.call(["mkdir", "-p", whamdir])

outfile = open("wham_config.txt", 'w')

# WHAM options
low_T = 80
high_T = 160
step_T = 10
num_dimensions = 2
threads = 4

num_of_tbin = whamOptions(whamdir, outfile, low_T, high_T, step_T, 
        num_dimensions, threads)

dosWrite(whamdir, outfile)
freeEnergyWrite(whamdir, outfile, low_T, step_T, num_of_tbin)
cvWrite(whamdir, outfile, low_T, step_T, num_of_tbin)

# Energy and Q bins;
outfile.write("\n")

least_Ene = 1000000
most_Ene = -5000000
least_Q = 500
most_Q = 0

binCoordWrite(whamdir, outfile, hist_name, low_T, high_T, step_T, 
        least_Ene, most_Ene, least_Q, most_Q)

outfile.close()

