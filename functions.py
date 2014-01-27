#! /usr/bin/python
 
from parameters import *
from classes import *
import decimal
import random, math, sys

# functions

def growing(filaments,touching,membrane):
	""" Grow, shrink and bend filaments """
	longestsofar = 0		
	localbarrier = membrane.position
	amountpushed = membrane.position - barrier
	for individual in filaments:
		# takes the last item in the list of lengths
		thislength = filaments[individual].length
		# checks if the filament has disappeared
		if thislength > 0:
			# unbend if enough space
			bent = filaments[individual].bent
			if bent != 0:
				if thislength < localbarrier:
					if thislength+bent <= localbarrier:
						thislength += bent
						filaments[individual].bent = 0
					else: 
						dist = localbarrier-thislength
						thislength += dist
						filaments[individual].bent -= dist
			# add or subtract subunit
			diceroll = random.random()
			if diceroll <= probability_addone:
				# checks to see if the filament hits the barrier
				if thislength+unitlength <= localbarrier:
					# adds a monomer if not
					thislength+=unitlength
				else:
					roulette = random.random()
					# push the barrier forwards
					probability_push = 2*math.exp((-membranetension*amountpushed**2)/(boltzmann*temperature))/(math.sqrt(boltzmann*temperature*math.pi/membranetension))
					if roulette < probability_push:
						thislength+=unitlength
						localbarrier+=unitlength
					else:
					# bend as a single filament
						filaments[individual] = bend(filaments[individual],localbarrier,amountpushed,"single")
					# bend as a group
						bendingmessage = bend(filaments[individual],localbarrier,amountpushed,"group")
						if bendingmessage[1] != 0:
							for o in range(0,len(filaments)):
								if o in bendingmessage[0]:
									#print "before", o, filaments[o].bent, filaments[o].length
									filaments[o].bent += bendingmessage[1]
									filaments[o].length -= bendingmessage[1]
									#print "after", o,  filaments[o].bent, filaments[o].length
			# remove a monomer
			elif diceroll <= probability_addone+probability_minusone:
				thislength-=unitlength

		# add new length to the filament object
		filaments[individual].moveon(thislength)
	return filaments

def count(filaments,*param):
	""" Count the number of (active or total) filaments """
	counter = 0
	for item in filaments:
		if param == "active":
			if filaments[item].length > 0:
				counter += 1
		else:
			counter+=1
	return counter

def touching(filaments,membrane):
	counter = 0
	for item in filaments:
		if filaments[item].length == membrane.position:
			counter += 1
	return counter

def longest(filaments):
	""" Find the length of the longest filament """
	longestsofar = 0
	for item in filaments:
		if filaments[item].length > longestsofar:
			longestsofar = filaments[item].length
	return longestsofar

def nucleate(filaments,time):
	""" Nucleate new filaments """
	nofils = numberoffilaments
	nucleationdiceroll = random.random()
	if nucleationdiceroll <= probability_nucleation:
		filaments[nofils] = filament(numberoffilaments+1)
		filaments[nofils].history = [0]*((time/dt))
		filaments[nofils].length = 1
	return filaments

def bundlemessage(bundlingregister,filaments):
	""" Passes messages between bundles and filaments """
	message = []
	wholebundle = []
	# creates a list with an entry for each filament
	# with one empty list (the position of bundling proteins)
	# and 1 for the radius of the bundle
	for item in filaments:
		message.append([[],1])
	for item in bundlingregister:
		# if the bundling protein is attached to two filaments
		if bundlingregister[item].position != 'a':
			pos = bundlingregister[item].position
			pal = bundlingregister[item].attachedto
			# put the position of the bundle into the message for each filament
			message[pal[0]][0].append(pos)
			message[pal[1]][0].append(pos)
			# makes lists of bundles of filaments by stepping through each bundling protein
			nowhere = True
			for abc in wholebundle:
					if pal[0] in abc:
						nowhere = False
						if pal[1] not in abc:
							abc.append(pal[1])
					elif pal[1] in abc:
						nowhere = False
						abc.append(pal[0])
			# makes a new bundle list if the filament is not in another bundle
			if nowhere:
				wholebundle.append([pal[0],pal[1]])
	wholebundle = condense(wholebundle)			
	# checks to see if each filament is attached to something or not
	# gives back a bundle size for each filament
	for i in range(0,len(message)):
		if message[i][0] == []:
			message[i][0] = "alone"
		bsize = [i]
		for thing in wholebundle:
			if thing != None:
				if i in thing:
					bsize = thing
		message[i][1] = bsize
	# adds the message to the filament objects
	for individual in filaments:
		filaments[individual].bundler(message[individual][0])
		filaments[individual].radiusofbundle = message[individual][1]
	return filaments

def bundles(bundlingregister,filaments):
	""" Give bundling proteins a position """
	for item in bundlingregister:
		bundleroll = random.random()
		if bundlingregister[item].position == 'a':
			if bundleroll <= probability_bundle:
				bundlingregister[item].attached = 1
				filist = []
				for i in range(0,numberoffilaments):
					filist.append(i)
				first = random.choice(filist)
				filist.remove(first)
				second = random.choice(filist)
				attachedto = [first,second]
				limit = min(filaments[first].length,filaments[second].length)
				newposition = random.randint(1,math.floor(limit))
			else: 
				attachedto = "n"
				newposition = "a"
		else:
			if bundleroll <= probability_unbundle:
				bundlingregister[item].attached = 0
				newposition = "a"
				attachedto = "n"
			else:
				newposition = bundlingregister[item].position
				attachedto = bundlingregister[item].attachedto
		bundlingregister[item].moveon(newposition,attachedto)
	return bundlingregister

def condense(wholebundle):
	''' combine bundles that share common filaments'''
	oldgroup = []
	if len(wholebundle) > 0:
		for i in range(0,len(wholebundle)):
			condition = False
			group = wholebundle[i]
			for item in oldgroup:
				if item in group:
					wholebundle[i].extend(oldgroup)
					wholebundle[i] = list(set(wholebundle[i]))
					wholebundle[i-1] = None
			oldgroup = group
		for thing in wholebundle:
			if thing == None:
				wholebundle.remove(thing)
	return wholebundle

def bend(filament,localbarrier,amountpushed,*param):
	shorten = 0
	if "single" in param:
		groupradius = 3.5
		if filament.bundled != "alone":
			grouplength = localbarrier - int(max(filament.bundled))
		else:
			grouplength = filament.length	
		gp = False
	elif "group" in param:
		groupradius = len(filament.radiusofbundle)*3.5
		grouplength = filament.length
		gp = True

	curvature = 0.001
	mominert = (math.pi * groupradius **4) /4
	fx = amountpushed * membranetension * unitlength
	groupbend = (fx - (curvature**2) * youngsmodulus_pernm * grouplength * mominert )/ (boltzmann * temperature)

	scalingfactor = 1/(math.exp(fx / (boltzmann * temperature)) * (math.sqrt(boltzmann * temperature * math.pi))/(2*math.sqrt(youngsmodulus_pernm * grouplength * mominert)))

#	scalingfactor = (youngsmodulus_pernm * curvature**2 * mominert)/(boltzmann * temperature)
#	scalingfactor = 2*(math.sqrt((youngsmodulus_pernm * grouplength * mominert / (boltzmann * temperature * math.pi)))

	probability_groupbend = scalingfactor*math.exp(groupbend)
	#print "P=", probability_groupbend, "N=", scalingfactor, "F=", amountpushed*membranetension, "x=", unitlength, "Y=", youngsmodulus_pernm, "l=", grouplength, "I=", mominert, "kB=", boltzmann, "T=", temperature

	if random.random() < probability_groupbend:
		shorten = grouplength-(1/curvature)*math.sin(grouplength*curvature)
		if not gp:
			filament.bent += shorten
			filament.length -= shorten
	if gp:
		return [filament.radiusofbundle,shorten]
	else:
		return filament

def output(time,activefils,longestfilament,filaments,membrane,touchingbarrier,bundlingregister,files):
 """writing data out to files"""

 affile = files[0]
 lefile = files[1]
 onfile = files[2]
 bnfile = files[3]
 bpfile = files[4]
 befile = files[5]

 string = str(time) + "\t" + str(activefils) + "\n"
 affile.write(string)

 string = str(time) + "\t" + str(longestfilament) + "\n"
 onfile.write(string)

 string = str(time) + "\t"
 for number in range(0,numberoffilaments):
	try: 
		string += str(filaments[number].length)+"\t"
	except:
		string += "\t"
 string+= "\n"
 lefile.write(string)

 string = str(time) + "\t"
 for number in range(0,numberoffilaments):
	try: 
		string += str(filaments[number].bent)+"\t"
	except:
		string += "\t"
 string+= "\n"
 befile.write(string)

 string = str(time) + "\t"
 for thing in bundlingregister:
		place = bundlingregister[thing].position
		if place != "a":
			first = bundlingregister[thing].attachedto[0]
			second = bundlingregister[thing].attachedto[1]
		else:
			first = "n"
			second = "n"
		string += str(place)+ "\t" + str(first) + "\t" + str(second) + "\t"
 string += "\n"
 bpfile.write(string)

 string = str(time) + "\t" + str(membrane.position)+ "\t" + str(touchingbarrier) + "\n"
 bnfile.write(string)

def openfiles():

	affile = open('output/output-number','w')
	lefile = open('output/output-length','w')
	onfile = open('output/output-longest','w')
	bnfile = open('output/output-barriernumber','w')
	bpfile = open('output/output-bundling','w')
	befile = open('output/output-bent','w')

	return [affile,lefile,onfile,bnfile,bpfile,befile]
