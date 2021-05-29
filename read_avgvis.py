import sys, os, math, time
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import cmath as cm
#import calib as cal

def read_avg_vis(filename, NA = 24, NC = 800):
    #* Antenna names
    ANTLIST = ["S11ORT","S10ORT","S09ORT","S08ORT",
    "S07ORT", "S06ORT","S05ORT","S04ORT","S03ORT",
    "S02ORT","S01ORT","N01ORT","N02ORT","N03ORT",
    "N04ORT","N05ORT","N06ORT","N07ORT","N08ORT",
    "N09ORT","N10ORT","N11ORT","S00ORT","N12ORT"]
    #* define visibility array [channel, antenna 1, antenna 2]
    vis = np.empty([NC, NA, NA], dtype=complex)
    #* open filename to read headers
    f = open(filename)
    header = f.readline() #* reads the header
    cols = header.split('       ') #* header has 6 spaces in-between columns
    col_num = len(cols) #* check how many such columns are there
    #* last noe only have spaces, must ignore during assign
    #
    #* open same file to read data
    data = np.loadtxt(filename)
    #! May be opening large visibility file twice 
    #! is not a good idea.
    for ii in range (0, col_num-1): 
        #* choose the pair of antenna from header
        #* split them into two antennas
        ant_pair= cols[ii].split(' ')[-1].split('-')
        #print(ant_pair)
        #* from antenna list find order of the antennas
        ant1 = [ANTLIST.index(jj) for jj in ANTLIST if ant_pair[0] in jj]
        ant2 = [ANTLIST.index(kk) for kk in ANTLIST if ant_pair[1] in kk]
        #print(ant_pair, ant1[0], ant2[0], ii*2+2)
        #* fill the visibility array accordingly
        #! Complex conjugate values are also filled
        vis[:, ant1[0], ant2[0]] = data[:, ii*2+1] + 1j*data[:, ii*2+2]
        vis[:, ant2[0], ant1[0]] = data[:, ii*2+1] - 1j*data[:, ii*2+2]
    return(vis)
def plot_bandpass(vis):
    NC, NA, _ = vis.shape
    vis_polar =np.zeros([NC, NA, NA, 2])
    for ii in range (0, NA):
        for jj in range (0, NA):
            for kk in range (0, NC):
                vis_polar[kk, jj, ii,0], vis_polar[kk, jj, ii, 1] = cm.polar(vis[kk, jj, ii])


    chan = np.linspace(0, NC, num=NC, endpoint=True)
    ANTLIST = ["S11ORT","S10ORT","S09ORT","S08ORT",
    "S07ORT", "S06ORT","S05ORT","S04ORT","S03ORT",
    "S02ORT","S01ORT","N01ORT","N02ORT","N03ORT",
    "N04ORT","N05ORT","N06ORT","N07ORT","N08ORT",
    "N09ORT","N10ORT","N11ORT","S00ORT","N12ORT"]
    check = input("Do you want to plot bandpass? ")
    q = input("phase also?")
    while (check == 'y'):
        ant = input("which antenna?")
        ant_num = ANTLIST.index(ant+'ORT')
        fig = plt.figure()
        plt.title(ant, fontsize=20)
        fig.subplots_adjust(hspace=0.6, wspace=0.4)
        for ii in range (0, NA):
            ax = fig.add_subplot(4, int (NA/4),ii+1)
            ax.semilogy(chan[:],abs(vis_polar[:,ant_num, ii, 0]), '-k', linewidth=0.5)
            ax.set_title(ANTLIST[ii], fontsize=8)
        plt.show()
        if (q == 'y'):
            fig2 = plt.figure()
            plt.title(ant, fontsize=20)
            fig2.subplots_adjust(hspace=0.6, wspace=0.4)
            for ii in range (0, NA):
                ax2 = fig2.add_subplot(4, int (NA/4),ii+1)
                ax2.plot(chan[:],vis_polar[:,ant_num, ii, 1], '-k', linewidth=0.5)
                ax2.set_title(ANTLIST[ii], fontsize=8)
            plt.show()
            
        check = input("Do you want to plot bandpass, again? ")

#tvis = read_avg_vis(filename = "avgvis.txt")
#print(tvis.shape)
#plot_bandpass(tvis)

