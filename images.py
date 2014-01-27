#! /usr/bin/python
 
from pyx import *

barrier = []
barrierfile = open('output/output-barriernumber')
for item in barrierfile:
	item = item.split()
	barrier.append(float(item[1]))

filaments = []
filamentsfile = open('output/output-length')
for item in filamentsfile:
	item = item.split()
	filaments.append(item[1:])

bundling = []
bundlingfile = open('output/output-bundling')
for item in bundlingfile:
	item = item.split()
	bundling.append(item[1:])
noofbuns = len(bundling[0])/3

nooffils = len(filaments[0])
boundary = max(barrier)

universeacross = path.line(0,0,float(boundary)+2,0)
universeup = path.line(0,0,0,float(nooffils)+3)
backmembrane = path.line(1, 1, 1, nooffils+2)

tmax = len(barrier)

for i in range(0,tmax):
	tether = barrier[i]+1
	frontmembrane = path.line(tether,1,tether,nooffils+2)
	c = canvas.canvas()
	c.stroke(universeup,[color.rgb.white])
	c.stroke(universeacross,[color.rgb.white])
	index = 2
	for item in filaments[i]:
		start = tether - float(item)
		statement = path.line(start,index,tether,index)
		index += 1
		c.stroke(statement,[style.linewidth.THICK,color.rgb.blue])
	for a in range(0,noofbuns):
		position = bundling[i][3*a] 
		if position != "a":
			start = tether - float(position)
			first = float(bundling[i][3*a+1])+2
			second = float(bundling[i][3*a+2])+2
			bundleone = path.circle(start,first,0.1)
			bundletwo = path.circle(start,second,0.1)
			connector = path.line(start,first,start,second)
			c.stroke(connector)
			c.fill(bundleone)
			c.fill(bundletwo)

	c.stroke(backmembrane,[style.linewidth.THICK,color.rgb.red])
	c.stroke(frontmembrane,[style.linewidth.THICK,color.rgb.red])
	
	filename = '{0:04}'.format(i)
	c.writeEPSfile('output/'+filename)
