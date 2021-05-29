import numpy as np
import math as m
import sys
import matplotlib.pyplot as plt
from matplotlib import ticker
import builtins as blt

import params_OWFA as OWFA
import read_write as rw

OWFA.params("P0")
'''
# ======== constants ========#
C = 299.792 # velocity of light in Km/s


#========= define system parameters =========#
nu_c = 326.5 #central frequency in MHz
N_c = 312 	# Number of spectral channels
dnu = 0.125	#Channel width in MHz
lam_c = C/nu_c # Wavelength corresponding to central frequency in meters
B_bw = N_c*dnu # Bandwidth in MHz
b = 30.0	# Antenna aperture dimension in meters along E-W direction
d = 11.5	# Antenna aperture dimension in meters along N-S direction
NA = 40	# Number of antennas
Nbl = 39	#Number of unique baselines
'''
print(NA, N_c, Nbl)
#========= System parameter defination ends =======#

#=========   Primary Beam Pattern   ===============#
#ap = pixel RA in rad, dp = pixel dec in rad, 
#(a0, d0) = pointing (RA,Dec), nnu = frequency in MHz

def beam(ap, dp, nnu, a0, d0):
	Ax = np.sinc((d*nnu/C)*(np.sin(dp) - np.sin(d0)))**2.0 
	Ay = np.sinc((b*nnu/C)*np.cos(dp)* np.sin(ap-a0))**2.0
	
	return Ax*Ay
	
#======== Beam Pattern done ======================#


#====== Tapering Function and parameters ========#
#tapering function is defined only along N-S direction
#with telescope pointing at (a0,d0) = (0,0)

th0 = 0.248 # th0 = 0.6 X th_{FWHM} for OWFA PII in rad
f = 0.6	# Tapering parameter
thw = th0*f

def w(dp, thw):
	return  np.exp(-(dp/thw)**2.0)
	
#=========== Tapering Function done =============#

#orig_stdout = sys.stdout
#f = open('PS_vis_tap_41', 'w')
#sys.stdout = f
#========== Visibility computation ===============#
def visgen(al_p, dl_p):
	V = np.zeros([Nbl, N_c],dtype = 'complex_')

	#al_p, dl_p = 0, np.pi/9.0	# source position in sky (rad)
	al_0, dl_0 = 0, 0	# pointing direction of the telescope (rad)

	for ii in range (0, N_c):
		nu = nu_c - (B_bw/2.0) + ii * dnu_c
		lam = C/nu
	
		for jj in range (0, Nbl):
		
			U = (jj+1)*d/lam
			V[jj, ii] = 1.0*beam(al_p, dl_p, nu, al_0, dl_0)*np.exp(-1j*2.0*np.pi*U*(np.sin(dl_p) - np.sin(dl_0)))
			#V[jj, ii] = w(dl_p)*beam(al_p, dl_p, nu, al_0, dl_0)*np.exp(-1j*2.0*np.pi*U*(np.sin(dl_p) - np.sin(dl_0)))
		
		
			#print("%d\t"%(jj+1),"%f\t"%U,"%e\t"%V[jj,ii].real,"%e\t"%V[jj,ii].imag)

	return(V)
#sys.stdout = orig_stdout
#f.close()


def plot_vis(data, dr, num):
	
	mm, nn =data.shape
	
	if dr == "B" :
		print("showing data for baseline %d\t "%num)
		
		x = np.arange(0, nn, 1)
		plt.figure(1)
		plt.subplot(211)
		plt.plot(x, data[num, :].real, 'b-')

		plt.subplot(212)
		plt.plot(x, data[num, :].imag, 'r-')

		plt.show()
		
		
	elif dr == "C" :
		print("showing data for channel %d\t "%num)
		
		x = np.arange(0, mm, 1)
		plt.figure(1)
		plt.subplot(211)
		plt.plot(x, data[ :, num].real, 'b-')

		plt.subplot(212)
		plt.plot(x, data[:, num].imag, 'r-')

		plt.show()


def gauss(n, thw, lam):
	return (np.pi * thw**2.0 * np.exp(-np.pi**2.0 * (n*d/lam)**2.0 * thw**2.0))


def vis_tap(data, f):

	thw = th0*f
	mm, nn =data.shape
	vis = data
	visc = np.zeros([mm, nn], dtype = 'complex_')
	wnorm = np.zeros([mm, nn], dtype = 'float64')
	U = np.zeros(Nbl)
	w = np.zeros(Nbl)
	for ll in range (0, N_c):
		nu = nu_c - (B_bw/2.0) +  ll* dnu
		lam = C/nu	

		for ii in range (0, Nbl):
			U[ii] = ii * d/lam
			w[ii] = gauss(ii, thw, lam)
			
		for ii in range (0, Nbl):
		#visc[ii, ll] = vis[ii, 1]
		#wg[ii, 0] = vis[ii, 1]
			for jj in range (0, Nbl):
				kk = abs(ii - jj)
				visc[ii, ll] += vis[jj,ll]*w[kk]
				wnorm[ii, ll] += w[kk]
	visc.real = visc.real/wnorm
	visc.imag = visc.imag/wnorm
	return (visc)
	


def plot_vis_comp(data, data_tap, dr, num):
	
	mm, nn =data.shape
	
	if dr == "B" :
		print("showing data for baseline %d\t "%num)
		
		x = np.arange(0, nn, 1)
		plt.figure(1)
		plt.subplot(211)
		plt.title('Real')
		plt.plot(x, data[num, :].real, 'b-', x, data_tap[num, :].real, 'r--')

		plt.subplot(212)
		plt.title('Imag')
		plt.plot(x, data[num, :].imag, 'r-', x, data_tap[num, :].imag, 'b--')

		plt.show()
		
		
	elif dr == "C" :
		print("showing data for channel %d\t "%num)
		
		x = np.arange(0, mm, 1)
		plt.figure(1)
		plt.subplot(211)
		plt.title('Real')
		plt.plot(x, data[ :, num].real, 'b-', x, data_tap[ :, num].real, 'r--')

		plt.subplot(212)
		plt.title('Imag')
		plt.plot(x, data[:, num].imag, 'r-', x, data_tap[:, num].imag, 'b--')

		plt.show()





def plot_vis_3D(data1):
	data = data1.transpose()
	#plt.subplots(figsize = (18,4))
	plt.subplot(121, aspect = 'auto')#, adjustable = 'box-forced')
	plt.title('Real')
	plt.ylabel('Channel')
	plt.xlabel('baseline')
	plt.imshow(data.real, cmap = 'coolwarm', interpolation = 'none', aspect = 'auto')
	cb = plt.colorbar(fraction = 0.05,orientation='horizontal')	
	tick_locator = ticker.MaxNLocator(nbins=3)
	cb.locator = tick_locator
	cb.update_ticks()
	
	plt.subplot(122, aspect = 'auto')#, adjustable = 'box-forced')
	plt.title('imag')
	plt.xlabel('Baseline')
	plt.ylabel('')	
	plt.imshow(data.imag, cmap = 'coolwarm', interpolation = 'none', aspect = 'auto')
	cb = plt.colorbar(fraction = 0.05,orientation='horizontal')
	tick_locator = ticker.MaxNLocator(nbins=3)
	cb.locator = tick_locator
	cb.update_ticks()
	
	plt.show()	








