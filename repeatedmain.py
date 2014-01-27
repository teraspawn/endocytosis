#! /usr/bin/python
# takes number of iterations (tmax in ms) as optional command line argument
 
import random, sys, math
from parameters import *
from functions import *
from classes import *

mafile = open('output/'+str(y),'w+')
metaoutput = []
z = membranetension

for y in range(0,60):
 for x in range(1,20):
   files = openfiles()

  # creates bundling protein dictionary, which is full of bundling protein objects
   bundlingregister = {}
   for i in range(0,bundlingnumber):
 	bundlingregister[i] = bundlingptn(i)

  # creates filament dictionary, which is full of filament objects
   filaments = {}
   for i in range(0,numberoffilaments):
	filaments[i] = filament(i)

  # creates membrane object
   membrane = membraney(barrier)

  # empty lists for recording the longest filament, and the number of active filaments
   longestfilament = [1]
   activefils = [numberoffilaments]
   touchingbarrier = [0]

  # growing filaments and storing list of lengths in values dictionary with filament no as key
   time = 0
   while membrane.position < 40:	

	# count the total number of filaments
	numberoffilaments = count(filaments)

	# record the total number of active filaments
	activefils = count(filaments,"active")

	# record the length of the longest filament
	longestfilament = longest(filaments)

	# count number of filaments touching the barrier
	touchingbarrier = touching(filaments,membrane)

	# add and remove bundling proteins
	bundlingregister = bundles(bundlingregister,filaments)	

	# pass information between bundling proteins and filaments
	filaments = bundlemessage(bundlingregister,filaments)

	# grow, bend or shrink filaments
	filaments = growing(filaments,touchingbarrier, membrane)

	# push against the membrane	
	membrane.moveon(longest(filaments))	

	# nucleate new filaments
	filaments = nucleate(filaments,time)

#	print time, count(filaments), count(filaments,"active"), longest(filaments), membrane.position, barrier,
#	for item in filaments:
#		print filaments[item].length, filaments[item].bundled,
#	for item in bundlingregister:
#		print bundlingregister[item].position, bundlingregister[item].attachedto,
#	print touchingbarrier[-1:]
#	print 


 	# output data
 	output(time,activefils,longestfilament,filaments,membrane,touchingbarrier,bundlingregister,files)

	# increment time
	time+=dt
   string = str(z) + "\t" + str(y) + "\t" + str(time) + "\n"
   metaoutput.append([z,y,time])		
   print string
   mafile.write(string)
#print metaoutput
