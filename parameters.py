#! /usr/bin/python
 
import sys

# probabilities sum to 1
# from fujiwara 2007 and sirotkin 2010
# in time step 1ms and [G-actin] 22uM
probability_addone = 0.25520
probability_minusone = 0.00025
probability_staysame = 0.74455


# from Beltzner & Pollard 2008
# 8 x 10^-9 uM-3 s-1
# weird units: divide by concentration of G-actin cubed??
# 7.51 x 10^-16 ms-1
probability_nucleation = 7.51*10**-16

probability_bend = 0.1
probability_bundle = 0.1
probability_unbundle = 0.01

# From Liu et al 2006
# 10^-4 N/m
# units N/nm
membranetension = 10**-13

# number of filaments 
numberoffilaments = 10

# number of bundling proteins
bundlingnumber = 10
#bundlingnumber = int(numberoffilaments/8)

#time step and tmax, time is measured in ms
dt = 1
try:
	tmax = int(sys.argv[1])	
except:
	tmax = 100

# in nm
unitlength = 2.7

barrier = unitlength * 7

#
youngsmodulus_pernm = 1.8*(10**(-9))
# kelvin
temperature = 298
boltzmann = 1.38*(10**(-14))


