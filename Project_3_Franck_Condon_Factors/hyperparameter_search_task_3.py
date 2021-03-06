from sys import argv
from strawberryfields.apps import vibronic, data, sample, plot
import numpy as np
from plotly import offline


###############################
####### OPEN INPUT FILE #######
###############################

def run_and_create(n):
    inputfile = open('./Task2Code/input_for_exercise3.txt', "r")

    N=int(inputfile.readline())     #Number of Atoms
    nmodes=3*N-6                    #Number of Modes

    w=np.zeros(nmodes,float)        #vib. frequencies of ground electronic state
    wp=np.zeros(nmodes,float)       #vib. frequencies of excited electronic state
    Ud=np.zeros((nmodes,nmodes),float)   #Duschinsky Matrix
    delta=np.zeros(nmodes,float)    #Displacement Vector


    ###############################
    ##### READ IN PARAMETERS ######
    ###############################

    for i in range(nmodes):
        w[i]=float(inputfile.readline())
    for i in range(nmodes):
        wp[i]=float(inputfile.readline())
    for i in range(nmodes):
        for j in range(nmodes):
            Ud[i,j]=float(inputfile.readline())

    for i in range(nmodes):
        delta[i]=float(inputfile.readline())

    T = 500  # temperature

    #####################################
    ##### CALCULATE GBS PARAMETERS ######
    #####################################

    t, U1, r, U2, alpha = vibronic.gbs_params(w, wp, Ud, delta, T)


    ###############################
    ###### GENERATE SAMPLES #######
    ###############################

    nr_samples = n
    s = sample.vibronic(t, U1, r, U2, alpha, nr_samples)
    e = vibronic.energies(s, w, wp)

    ###############################
    ######## PLOT SPECTRUM ########
    ###############################

    spectrum = plot.spectrum(e, xmin=-300, xmax=2000)
    offline.plot(spectrum, filename="spectrum_{}_samples.html".format(n))


def main():
    for n in [10, 100, 500, 1000, 5000, 10000, 20000]:
        run_and_create(n)

if __name__ == '__main__':
    main()
