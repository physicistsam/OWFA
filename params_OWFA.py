import numpy as np
import sys
import builtins as blt
# ======== constants ========#
blt.C = 299.792 # velocity of light in Km/s

#class var:
def params(phase):
	#global b
	#OWFA system paprams:
	blt.b = 30				#in meters
	blt.nu_c = 326.5 		#central frequency in MHz
	blt.N_c = 312			# No. of channel
	blt.B_bw = 39			#in MHz units bandwidth
	blt.dnu_c = 0.125 		# channel width in MHz units
	blt.lam_c = C/nu_c 		# Wavelength corresponding to central frequency in mete
	if (phase == 'PI'):
		blt.d = 11.50		#in meters
		blt.NA = 40			#no of antennas
		blt.Nbl = 39		#no of baselines
		blt.A_dBdT = 14.9	#for PI	#(A*(dB/dT)^2)-1 (mk/Jy)^2 # due to modified pbeam
		
	elif (phase == 'PII'):
		blt.d = 1.92		#in meters
		blt.NA = 264		#no of antennas
		blt.Nbl = 263		#no of baselines
		blt.A_dBdT =2.483	#for PI	#(A*(dB/dT)^2)-1 (mk/Jy)^2 # due to modified pbeam

	elif (phase == 'P0'): #* Hypothetical phase
		blt.d = 23		#in meters
		blt.NA =22			#no of antennas
		blt.Nbl = 21			#no of baselines
		blt.A_dBdT =15.		#for PI	#(A*(dB/dT)^2)-1 (mk/Jy)^2 # due to modified pbeam
		blt.N_c = 40
		blt.B_bw = 20
		blt.dnu_c = blt.B_bw / blt.N_c	
	else :
		print ("Please enter either PI or PII")
		#sys.exit(0)
		
	#Cosmology of OWFA	
	blt.r = 6845.5			#comoving distance in Mpc
	blt.rp = 11.5			#dr/dnu in Mpc/MHz
	blt.dBdT = 3.27			#(dB/dT)_326.5 in Jy/mK 
	blt.Tsys = 150 			# system temperature in K
	blt.KB = 1.38 * 1e3 	# Boltzman constant in Jy/K
	blt.eta = 0.6		 	# efficiency of the telescope
	#global b
	blt.Nthreads = 8
	return (0)
	

