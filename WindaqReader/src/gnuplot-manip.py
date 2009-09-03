#!/usr/bin/python
import os
import math
import numpy
import Gnuplot
from Gnuplot import PlotItems,funcutils
from numpy import ones
plotfile = "cy_f143r_h_stoich_083109_outfile.csv"

import csv 
f = open(plotfile,"r")
creader = csv.reader(f,dialect=csv)
volts = []
for line in creader:
	try:
		volts.append(float(line[0]))
	except IndexError ,e:
		pass



import numpy

def smooth(x,window_len=11,window='hanning'):
    """smooth the data using a window with requested size.
    
    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.
    
    input:
        x: the input signal 
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal
        
    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)
    
    see also: 
    
    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter
 
    TODO: the window parameter could be the window itself if an array instead of a string   
    """

    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."


    if window_len<3:
        return x


    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"


    s=numpy.r_[2*x[0]-x[window_len:1:-1],x,2*x[-1]-x[-1:-window_len:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=ones(window_len,'d')
    else:
        w=eval('numpy.'+window+'(window_len)')

    y=numpy.convolve(w/w.sum(),s,mode='same')
    return y[window_len-1:-window_len+1]

def mysum(arr):
	v = 0 
	for i in arr:
		v = v + i
	return v
	
def detect_event(mylist):
	vals = len(mylist)
	ra = []
	step = 100
	for i in range(0,vals,step):
	#	print  mylist[i-step:i+step]
		try:
			avgval = (mysum(mylist[i-step:i+step]))/len(mylist[i-step:i+step])
			ra.append(avgval*2*step)
		except Exception , e:
			pass
	return ra
			
data = smooth(numpy.array(volts),window_len=10,window="blackman")
#deriv = numpy.diff(data,n=1,axis=0)
other = detect_event(volts)
deriv =numpy.diff(numpy.array(data),n=1,axis=0)
derivderiv = smooth(numpy.diff(deriv,n=1,axis=0),window_len=500,window="hamming")

fdd = open("fdd.dat","w")
for i in derivderiv:
	print i 
	fdd.write("%f\n" % float(100*i))
fdd.close()

fo = open("other.dat","w")
for i in other:
	fo.write("%f\n" %i)
fo.close()

f = open("tmph.dat","w")
for i in data:
	write = math.log(i)
	if write != "nan":
		print i
		f.write("%f\n" % math.log(i))
f.close


fd = open("tmphderiv.dat","w")
for i in deriv:
	fd.write("%f\n" % i)
fd.close


g = Gnuplot.Gnuplot(debug=1)
#g('set term postscript eps enhanced')
#'plot \"fdd.dat\" with lines
g('set term aqua')
# , \"tmpcl.dat\" with lines ,
g('plot \"tmph.dat\" with lines')
#g('plot \"other.dat\" with lines')
#g('plot \"tmphderiv.dat\" with lines')