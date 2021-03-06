import pandas as pd
import numpy as np	
import matplotlib as mpl
import matplotlib.pyplot as plt
import MySQLdb
import sys
import pylab
from matplotlib.pyplot import plot, scatter, show
from math import atan2, degrees, pi
import sys
from numpy import NaN, Inf, arange, isscalar, asarray, array

pslope=[]
nslope=[]
new_list =[]
incpeakx=[]
incpeaky=[]
decpeakx=[]
decpeaky=[]
downtemp=[]
stepxval=[]	
stepyval=[]	
ycount =[]
count1=[]
y=[]
xaxis =[]
yeardecxval =[]
yeardecyval =[]
trenddecxval=[]
trenddecyval=[]
diff=[0]
diff3=[]
change1=[]
peak=[]
evenarr=[]
oddarr=[]
weeksearch =0
trendlimit=0
spikediff1=[]
spikediff =[0]
spikemaxdiff =0
spikediffabs=[]
spikechange =[]
spiketemp=[]
spiketemp1=[]
spikeyaxisthreshold = 0
spikexaxisthreshold = 0
spikefinal=[]
spikeindex=[]
spikeyval=[]
ststart=[]
step=[]
trendecyval=[]
trendecyval=[]
desc=[]
desctemp=[]
temp =[]
incr=[]
spikecount=[]
policycount=[]
stepcount=[]
inctcount=[]
deccount=[]
table_vals=[]

trendcount =[0]*4
stepindices =[]
spikeindices =[]
incrtrendindices =[]
decrtrendindices =[]


fig = plt.figure()
ax = fig.add_subplot(111)


#For smoothing input: arrayToSmooth , smoothing factor
def movingaverage(array, window_size):
    window = np.ones(int(window_size))/int(window_size)
    return np.convolve(array, window, 'same')
	
#TO find slope for step
def findslope(y,i,end,lt):
	
	step ='false'
	
	fs = abs(y[i]-y[end])/abs(i-end)
	
	if(fs<lt):
		step ='true'
	else:
		step ='false'
	return step
	
#function for step detection
def stepdet(y,lt):
	st =[]
	n=0
	
	diff3 =[0]
	i=0
	diff3 = np.append(diff3,np.diff(y))
	print "diff 3 len "  + str(len(diff3))
	spltr =40
	spltl =40
	
	while(n<len(y)-1):
		sp=0
		l =n+1
		steppre =  findslope(y,n,l,lt)
		
		if(steppre == 'true'):
			start = n
			while(steppre == 'true'):
				if(l<len(diff3)-1):
					steppre = findslope(y,n,l+1,lt)
					l=l+1
				if(l == len(diff3)-1):
					steppre == 'false'
					break;
					
			end = l	
			
			
			for i in range(start,end):
				
				dx = i+1 - (i)
				dy = diff3[i+1] - diff3[i]
				rads = atan2(-dy,dx)
				rads %= 2*pi
				degs = degrees(rads)
				
				if(degs>80 and degs<360):
					sp =1
				else :
					n=end	
			if(sp==1):
				st.append(start)#, end))
				st.append(end)
				n=end
			else :
				n=end	
		else :
			n=n+1
				
	return st
	
#to detect policy change			
def findpolicychange(diff2,y):
	count = y
	diffavg =0
	check = 0
	maxdiff =0
	trendiffavg = 0
	index=[]
	temp =[]
	temp1 =[]
	maxarr=[]
	change =[]
	#Threshold to detect policy change
	#trendlimit = int(raw_input("enter threshold percentage for trend detection : "))
	trendlimit = 90
	for i in range(0,len(diff2)-1) :
		if((diff2[i] >weeksearch and diff2[i+1]<-weeksearch) or (diff2[i] <-weeksearch and diff2[i+1]>weeksearch) or
		(diff2[i] ==1 and diff2[i+1]<=weeksearch) or (diff2[i] ==1 and diff2[i+1]>=weeksearch)
		or (diff2[i] <=weeksearch and diff2[i+1]==1) or (diff2[i] >=weeksearch and diff2[i+1]==1)) :
			change.append(i)
	
	for x in change :
		temp.append(x)
		temp.append(count[x])
	
	for x in range(0,len(temp)-3,2):
		temp1.append(abs(temp[x+3]-temp[x+1]))
		
		temp1.append(temp[x])
		temp1.append(temp[x+2])
		
	for x in range(0,len(temp1)-2,3):
		#print 'temp1[x]' + str(temp1[x])
		diffavg = diffavg+ abs(temp1[x])
		check = check+1
		
	for x in range(0,len(temp1)-3,3):
		maxarr.append(abs(temp1[x]))
		
	maxdiff = max(maxarr)
	diffavg = diffavg/check
	print 'diffavg' + str(diffavg)
	
	print 'maxdiff '+str(maxdiff)
	print 'entered threshold ' + str(trendlimit)
	trendiffavg = ((maxdiff * trendlimit)/100)
	print "trenddiffvg " + str(trendiffavg)
	for x in range(0,len(temp1)-3,3):
		if( abs(temp1[x]) > float(trendiffavg) ):
			
			index.append(temp1[x+1])
			index.append(temp1[x+2])
	print 'index for trend change'+ str(index)	
		
	return 	index
		
def findspike(diff3,y):
	count =y
	spikediffavg =0
	spikemaxdiff =0
	spikeyaxisthreshold = 0
	spikexaxisthreshold = 0
	del spikechange[:]
	del spikediff1[:]
	del spiketemp[:]
	del spiketemp1[:]
	del spikeindex[:]
	del spikefinal[:]
	
	lt =0
	for i in range(0,len(diff3)-1) :
		
		if((diff3[i] >0 and diff3[i+1]<0) or (diff3[i] <0 and diff3[i+1]>0) or (diff3[i] ==0 and diff3[i+1]<0) or (diff3[i] ==0 and diff3[i+1]>0
		or (diff3[i] <0 and diff3[i+1]==0) or (diff3[i] >0 and diff3[i+1]==0))) :
			spikechange.append(i)
				
		
		if((diff3[i] >lt and diff3[i+1]<-(lt))  ) :
			spikechange.append(i)
		if((diff3[i] <-(lt) and diff3[i+1]>lt)  ) :
			spikechange.append(i)	
	#print 'spikechange'
	#print spikechange
	#temp = [count1[x] for x in change]
	for i in range(0,len(diff3)) :
		spikediff1.append(abs(diff3[i]))
	#print('diff1 ')
	#print(diff1)	
	for x in spikechange :
		spiketemp.append(x)
		spiketemp.append(count[x])
	
	for x in range(0,len(spiketemp)-3,2):
		spiketemp1.append(abs(spiketemp[x+3]-spiketemp[x+1]))
		#print 'diff' + str(abs(spiketemp[x+1]-spiketemp[x+3]))
		spiketemp1.append(spiketemp[x])
		#print 'start index' + str(x)
		spiketemp1.append(spiketemp[x+2])
		#print 'end index' + str(x+2)
	#print 'spiketemp1'
	#print spiketemp1
	
	for x in range(0,len(spiketemp1)-5,3):
		if((spiketemp1[x]==0) and (spiketemp1[x+1]==spiketemp1[x+2])) :
			spikeindex.append(spiketemp1[x-2])
			spikeindex.append(spiketemp1[x+2])
			spikeindex.append(spiketemp1[x+5])
	#print '	spikeindex '
	#print spikeindex
	spikeyaxisthreshold = float(raw_input("enter y threshold for spike detection : "))
	spikexaxisthreshold = float(raw_input("enter x threshold for spike detection : "))
	for x in range(0,len(spikeindex)-2,3) :
		if((abs(count[spikeindex[x]]-count[spikeindex[x+1]])> spikeyaxisthreshold) and (abs(count[spikeindex[x]]-count[spikeindex[x+1]])> spikeyaxisthreshold) and abs(spikeindex[x]-spikeindex[x+2])< spikexaxisthreshold):
			#spikefinal.append(spikeindex[x])
			spikefinal.append(spikeindex[x+1])
			#spikefinal.append(spikeindex[x+2])
	print 'spikefinal'
	print spikefinal
	return 	spikefinal	

def findstep(diff5):
	count=0
	sub =0
	start =[]
	init=[]
	middle =[]
	inter=[]
	endpt=[]
	stepend=[]
	flag=0
	print diff5
	for i in range(2,len(diff5)-2):
		if((diff5[i]>500 and diff5[i-1]<-500) or (diff5[i]>500 and diff5[i-1]==0 and diff5[i-2]==0 )) :
			start.append(i)
		#if ( (diff3[i] ==0 and  abs(diff3[i+1]) >0 ) or (diff3[i] ==0 and abs(diff3[i-1]) >0)):
		if ( (diff3[i] ==0 or abs(diff3[i+1]) <100 )):
			step.append(i)
			for m in range(i-1, 1,-1):
				if(diff5[m]<0 and diff5[m-1]>0):
					slope = diff5[i-1]-diff[m-1]/m-i-2
					if(slope<30 or slope > -30):
						step.append(i)
						#step.append(i-1)
					
						#step.append(m-1)
					
					break;
					
	return step

def findincslope(y,i,end,lt):
	
	step ='false'
	#next = inc-1
	#fs = (abs(y[i])-abs(y[end]))/(abs(i)-abs(end))
	fs = (y[end]-y[i])
	#print "original slope for " + str(i)+ "- "+ str(end) + "value" + str(y[i]) +"to"+ str(y[end])
	print str(fs)
	if(fs>lt):
			
			#print str(y[i]) + " - "+ str(abs(y[end])) + "= " + str(abs(y[i]-y[end]))
			#print "deniminators " + str(i)+ "- "+ str(end) + " = "+ str(abs(i-end))
			#print "slope " + str(fs)+ " lt = "+ str(lt)
			step ='true'
	else:
		step ='false'
	return step	
def finddecslope(y,i,end,lt):
	
	step ='false'
	#next = inc-1
	#fs = (abs(y[i])-abs(y[end]))/(abs(i)-abs(end))
	fs =(y[end]-y[i])
	#print "original slope" + str(i)+ "- "+ str(end)+ "value" +  str(y[end]) +"to"+ str(y[i])
	print str(fs)
	if(fs<lt):
			
			#print str(y[i]) + " - "+ str(abs(y[end])) + "= " + str(abs(y[i]-y[end]))
			#print "deniminators " + str(i)+ "- "+ str(end) + " = "+ str(abs(i-end))
			#print "slope " + str(fs)+ " lt = "+ str(lt)
			step ='true'
	else:
		step ='false'
	return step	
	
	
	
def monoton(y,lt):
	i=0
	#next = inc-1  
	
	#print "diff 3 len "  + str(len(diff3))
	#while(i<len(y)-(inc+1)):
	inc =1
	while(i<(len(y)-(inc+1))):
		sp=0
		l =i+inc
		steppre =  findincslope(y,i,l,0)
		#steppre =  findslope(diff3,i,l,lt)
		print "slope result "+ steppre
		if(steppre == 'true'):
			start = i
			while(steppre == 'true'):
				if(l<(len(y)-(inc+1))):
					steppre = findincslope(y,l,l+inc,0)
					l=l+inc
				if(l == (len(y)-inc)):
					steppre == 'false'
					
			end = l-inc
			i=end
			pslope.append(start)
			pslope.append(end)
		else:
			i=l+inc
	print pslope
	i=0
	inc =1
	while(i<(len(y)-(inc+1))):
		sp=0
		l =i+inc
		steppre =  finddecslope(y,i,l,0)
		
		if(steppre == 'true'):
			start = i
			while(steppre == 'true'):
				if(l<(len(y)-(inc+1))):
					steppre = finddecslope(y,l,l+inc,0)
					
					l=l+inc
					print "after desc"+ str(l)+" "+str(len(y))
				if(l >= (len(y)-inc-1)):
					steppre == 'false'
					break;
					
			end = l	
			i=l+inc
			nslope.append(start)
			nslope.append(end)
		else:
			i=l+inc
	print "nslope"		
	print nslope

def peakdet(v, idelta,ddelta, x = None):
    
    maxtab = []
    mintab = []
    idelta = float(idelta) 
    if x is None:
        x = arange(len(v))
    
    v = asarray(v)
    
    if len(v) != len(x):
        sys.exit('Input vectors v and x must have same length')
    
    if not isscalar(idelta):
        sys.exit('Input argument incr delta must be a scalar')
	
	if not isscalar(ddelta):
		sys.exit('Input argument decr delta must be a scalar')
    
    if float(idelta) < 0:
        sys.exit('Input argument incr delta must be positive')
		
	if float(ddelta) < 0:
		sys.exit('Input argument decr delta must be positive')
    
    mn, mx = Inf, -Inf
    mnpos, mxpos = NaN, NaN
    
    lookformax = True
    
    for i in arange(len(v)):
        this = float(v[i])
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]
        
        if lookformax:
            if float(this) < float(mx-idelta):
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn+ddelta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    return array(maxtab), array(mintab)	




def drawgraph(ycount,col):
	diff =0
	
	trendracecount =[0]*4
	trendrace2count =[0]*4
	global trendcount
	global stepindices
	global spikeindices
	global incrtrendindices
	global decrtrendindices
	
	for i in range(0,len(ycount)):
		xaxis.append(i)
	count1 = movingaverage(ycount,7)
	print 'len(count1)' + str(len(count1))
	#results = zip([x[0] for x in results], count1)
	diff = np.append(diff,np.diff(count1))
	lt = float(raw_input("enter threshold tfor step detection : "))
	stepxval = stepdet(count1,lt)	
	stepyval = [count1[x] for x in stepxval]
	print "step"
	print stepxval
	pxval = findpolicychange(diff,count1)
	for i in range(0,len(pxval)-1,2):
		evenarr.append(pxval[i])
	for i in range(1,len(pxval),2):
		oddarr.append(pxval[i])	
	pyval = [count1[x] for x in pxval]
	pevenyval = [count1[x] for x in evenarr]
	poddyval = [count1[x] for x in oddarr]
	spikexval= findspike(diff,count1)
	y = movingaverage(ycount,7)
	t = float(raw_input("enter threshold percentage for Monotonictrend detection : "))
	maxtab, mintab = peakdet(y,float(t),0.0001)
	
	peakux = array(maxtab)[:,0]
	peakuy = array(maxtab)[:,1]
	for i in range(0,len(peakux)-1):
		if(count1[peakux[i]] < count1[peakux[i+1]]):
			incpeakx.append(peakux[i])
			if(i==len(peakux)-1):
				incpeakx.append(peakux[i+1])	
			#decpeakx.append(peakux[i+1])
		elif (count1[peakux[i+1]] < count1[peakux[i]]):	
			incpeakx.append(peakux[i])
			decpeakx.append(peakux[i+1])
	decpeaky= [count1[x] for x in decpeakx]	
	incpeaky= [count1[x] for x in incpeakx]	
	
	#plt.plot(peakux,peakuy ,color='red')
	
	desctemp.append((len(spikexval))/2)
	desctemp.append((len(stepxval))/2)
	desctemp.append((len(incpeakx)))
	desctemp.append((len(decpeakx)))
	
	if(col== 'blue'):
		stepindices = [int(x) for x in stepxval]
		spikeindices = [int(x) for x in spikexval]
		incrtrendindices= [float(x) for x in incpeakx]
		decrtrendindices= [float(x) for x in decpeakx]
		trendcount[0] =len(stepxval)
		trendcount[1] =len(spikexval)
		trendcount[2] =len(incpeakx)
		trendcount[3] =len(decpeakx)
		tofile = str(trendcount)
		
	else:
		for i in stepindices:
			if not i in stepxval:
				trendracecount[0] = trendracecount[0]+1
		for j in spikeindices:
			if  not j in spikexval:
				trendracecount[1] = trendracecount[1]+1	
		for k in incrtrendindices:
			if  not k in incpeakx:
				trendracecount[2] = trendracecount[2]+1
		for m in decrtrendindices:
			if  not m in decpeakx:
				trendracecount[3] = trendracecount[3]+1	
		print "trendcount" + str(trendcount)
		print "trendracecount" + str(trendracecount)
		trendrace2count[0] =trendracecount[0]/float(trendcount[0])
		trendrace2count[1] = trendracecount[1]/float(trendcount[1])
		trendrace2count[2] = trendracecount[2]/float(trendcount[2])
		trendrace2count[3] = trendracecount[3]/float(trendcount[3])
		tofile = str(trendrace2count)
		
	
	
	new_list = list(desctemp)
	table_vals.append(new_list)
	spikeyval = [count1[x] for x in spikexval]
	plt.plot(xaxis,count1,color=col)
	plt.plot(spikexval,spikeyval,'ko')
	plt.plot(evenarr,pevenyval,'rD')	
	plt.plot(oddarr,poddyval,'yD')	
	
	plt.plot(incpeakx,incpeaky,'mD')
	plt.plot(decpeakx,decpeaky,'gD')
	plt.plot(stepxval,stepyval,'co')	
	print "peakux", peakux, peakuy
	print type(peakux), type(peakuy)
	#import sys
	#sys.exit(0)
	del oddarr[:]
	del evenarr[:]
	del pxval[:]
	del spikexval[:]
	del stepxval[:]
	del xaxis[:]
	del incpeakx[:]
	del decpeakx[:]
	del desctemp[:]
	return tofile

main =[0.752,0.765]
raceB =[0.481,0.514]
raceP =[0.068,0.048]
raceQ =[0.253,0.238]
raceW = [0.072,0.124]
target = open('F:\\UDS\\new\\race.txt', 'w')
	
cnt = drawgraph(main,"blue")
target.write("stopcs_casng:"+str(cnt)+',')
cnt =drawgraph(raceB,"black")
target.write("stopcs_casng:"+str(cnt)+',')
cnt =drawgraph(raceP,"#806517")#light green
target.write("stopcs_casng:"+str(cnt)+',')
cnt =drawgraph(raceQ,"#CC6600")#brown
target.write("stopcs_casng:"+str(cnt)+',')
cnt =drawgraph(raceW,"#F778A1")#pnk
target.write("stopcs_casng:"+str(cnt)+',')
	
target.close()


col_labels=['spike','step','inc','dec']
row_labels=['general','B','P','Q','W']
#row_labels=['general']
print "table_vals"
print table_vals
the_table = plt.table(cellText=table_vals,
                  colWidths = [0.06]*4,
                  rowLabels=row_labels,
                  colLabels=col_labels,
                  loc='upper center')

plt.show()