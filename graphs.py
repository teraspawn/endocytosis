#! /usr/bin/python
 
from pyx import *

graphsize = 50

#makes line graph of number of active filaments
g = graph.graphxy(width=graphsize,
	x=graph.axis.lin(title="Time (s)"),
	y=graph.axis.lin(min=0, title="Number of filaments"))
g.plot(graph.data.file("output/output-number", x=1, y=2),
	[graph.style.line()])
g.writeEPSfile("output/graph-number")

#counts number of filaments in the length file
lf = open('output/output-length','r')
columns = len(lf.readline().split())

#makes line graph of length vs time, with longest filament in red
p = graph.graphxy(width=graphsize,
        x=graph.axis.lin(title="Time (ms)"),
        y=graph.axis.lin(title="Length"))
for i in range(2,columns):
	p.plot([graph.data.file("output/output-length", x=1, y=i)],[graph.style.line()])
p.plot([graph.data.file("output/output-longest", x=1, y=2)],[graph.style.line([color.rgb.red])])
p.writeEPSfile("output/graph-length")

q = graph.graphxy(width=graphsize,
	x=graph.axis.lin(title="Time(ms)"),
	y=graph.axis.lin(),
	key=graph.key.key(pos="tl", dist=0.1))
q.plot(graph.data.file("output/output-barriernumber", x=1, y=2, title="Barrier position"),[graph.style.line()])
q.plot(graph.data.file("output/output-barriernumber", x=1, y=3, title="Number of filaments touching barrier"),[graph.style.line([color.rgb.red])])

q.writeEPSfile("output/graph-barriernumber")
