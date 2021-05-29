import numpy as np
import builtins as blt
import sys

def write_vis(filename, data):
	
	orig_stdout = sys.stdout
	f = open(filename, 'w')
	sys.stdout = f
		
	for ii in range (0, N_c):
		nu = nu_c - (B_bw/2.0) + ii * dnu_c
		lam = C/nu
	
		for jj in range (0, Nbl):
		
			U = (jj+1)*d/lam
		
			print("%d\t"%(jj+1),"%f\t"%U,"%e\t"%data[jj,ii].real,"%e\t"%data[jj,ii].imag)	
	sys.stdout = orig_stdout
	f.close()

def read_vis(filename):
	
	data = np.loadtxt(filename)
	print(data.shape)	
	mm , nn = data.shape
	Nchan = int(mm/Nbl)
	V = np.zeros([Nbl, Nchan],dtype = 'complex_')
	B = int(0)
	N = int(0)
	for ii in range (0, mm):
		V[B, N] = data[ii, nn-2] + 1j*data[ii, nn-1]
		#V[B, N].real = data[ii, 2]
		#V[B, N].imag = data[ii, 3]
		B = B+1
		if (B == Nbl):
			N = N + 1
			B = 0	

	return (V)
	
	
	
	
def mod_format_vis(data):
	
	#data = np.loadtxt(filename)
	mm, nn =data.shape
	Nchan = int(mm/Nbl)
	V = np.zeros([Nbl, Nchan],dtype = 'complex_')
	#mm  = data.shape
	B = int(0)
	N = int(0)
	for ii in range (0, mm):
		V[B, N] = data[ii]
		#V[B, N].real = data[ii, 2]
		#V[B, N].imag = data[ii, 3]
		B = B+1
		if (B == Nbl):
			N = N + 1
			B = 0	

	return (V)
		
	
def reduce_chan(data, Nchan, keep_bandwidth=True):

	bl, nc = data.shape
	V = np.zeros([bl, Nchan],dtype = 'complex_')
	if (keep_bandwidth==True):
		nf = int(nc/Nchan)

		for ii in range (0, Nchan):
			V[:, ii] = data[:, nf*ii]

	else:
		ns = int(nc/2 - Nchan/2)
		for ii in range (0, Nchan):
			V[:, ii] = data[:, ns+ii]

	return(V)

	
	
	
	
	
	
	
	
	
	
