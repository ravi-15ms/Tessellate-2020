#seggeration in grid
import numpy as np
from matplotlib import colors
import random
import itertools 
from collections import Counter
from random import choice
import matplotlib.pyplot as plt
import matplotlib.colors
import matplotlib.patches as mpatches



row=10*5					#Number of rows
col=10*5					#number of columns
a=np.zeros((row,col))			#size of lattice grid

#******IMPORTANT***********
#8 represents empty spaces
#1 represents one type of population
#0 represents other type of population	
density=0.98			#density of grid that are filled
happy=0.5			#probabilty of neighbours that should be similar for not to change place
prob=0.5			#probabilty that a grid will be either of one population(0) or the other.

###########################################################			
def nghd(i,j):
			agent=a[i][j]			#function for finding all 8 neighbouring positions
			if(i==0):
				p=i+1
				q=row-1
			if(j==0):
				r=j+1
				s=row-1
			if(i==row-1):
				p=1
				q=i-1
			if(j==col-1):
				r=1
				s=j-1
			if(i!=0 and i!=row-1 ):
				p=i+1
				q=i-1
			if( j!=0 and j!=col-1):
				r=j+1
				s=j-1	
			l1=[i,p,q]
			l2=[j,r,s]
			temp = list(itertools.product(l1, l2))						#all the neighbour points of the position i,j
			temp=temp[1:]												#to remove the element itself
			list_nghd=[a[temp[k]] for k in range(len(temp))]
			list_nghd=np.array(list_nghd)								#converting into numpy array
			empty_space=np.count_nonzero(list_nghd==8)					#number of empty neighbours 
			nghd_one=np.count_nonzero(list_nghd==1)#/(8.0-empty_space)		#counting number of 1 neighbours
			nghd_zero=np.count_nonzero(list_nghd==0)#/(8.0-empty_space)		#counting number of 0 neighbours
			total=nghd_one+nghd_zero
			
			if(agent==1 and total!=0):
				return(nghd_one/total,temp)
			if(agent==0 and total!=0):
				return(nghd_zero/total,temp)
			else:
				return(0,temp)
			#return(nghd_one,nghd_zero,temp)	
			
#####################################################################
#function to find the current status of the overall population(fraction of people satisfied and unsatisfied)
def status(a):
	count_satisfied=0
	count_unsatisfied=0
	e=np.count_nonzero(a==8)			#total number of empty spaces
	e=float(row*col-e)								#total number of occupied spaces
	for i in range(row):
		for j in range(col):
			p=a[i][j]
			b=nghd(i,j)
			if(a[i][j]!=8):
				if(a[i][j]==1 and b[0]>=happy or (a[i][j]==0 and b[0]>=happy)):
					count_satisfied+=1
					
				else:
					count_unsatisfied+=1
			else:
					continue
	
	return(count_satisfied/e,count_unsatisfied/e)			
#######################################################################					
#for initilisation of grid
for i in range(row):
	for j in range(col):
		r=random.uniform(0,1)
		if (r<density):
			q=random.uniform(0,1)
			if(q>prob):
				a[i][j]=0
			else:
				a[i][j]=1
		else:
			a[i][j]=8
print(status(a))	
print(np.count_nonzero(a==1),np.count_nonzero(a==0))		

#**********************************************************************
#code section for creating graphs
cmap = colors.ListedColormap(['orange', 'blue' ,'white'])
bounds=[0,0.5,2,8]
norm = colors.BoundaryNorm(bounds, cmap.N)
im=plt.imshow(a)
labels = {0:'A population',1:'B population',2:'vacant space'}
values = np.unique((a.ravel()))
values = [int(x) for x in values]
#print(values)
# get the colors of the values, according to the 
# colormap used by imshow
colors = ['orange', 'blue' ,'white']
# create a patch (proxy artist) for every color 
patches = [ mpatches.Patch(color=colors[i], label=labels[i] ) for i in range(len(values)) ]
# put those patched as legend-handles into the legend
#***********************************************************************
plt.legend(handles=patches, bbox_to_anchor=(1, 1), loc=6, borderaxespad=0. )
plt.imshow(a,cmap=cmap,norm=norm)
plt.savefig('initial.png', bbox_inches='tight')
plt.close()


#######################################################
#function to assign an empty space to the required agent
def empty_spaces(a):
	index=[]
	for m in range(row):
		for n in range(col):
			if(a[m][n]==8):
				index.append([m,n])
	return(choice(index))	
########################################################
time=[] 
num_happy=[]
num_sad=[]
#########################################################
for t in range(50):
	for i in range(row):
		for j in range(col):
			p=a[i][j]
			b=nghd(i,j)
			if(a[i][j]!=8):
				if((a[i][j]==1 and b[0]>=happy) or (a[i][j]==0 and b[0]>=happy)):
					continue
				else:
						new_pos=empty_spaces(a)
						a[new_pos[0]][new_pos[1]]=a[i][j]
						a[i][j]=8
						
			else:
				continue
	print(status(a))
	time.append(t)
	num_happy.append(status(a)[0])
	num_sad.append(status(a)[1])
plt.plot(time,num_happy,label='Fraction of satisfied people',color='red')
plt.plot(time,num_sad,label='Fraction of unsatisfied people')
plt.xlabel('time')
plt.ylabel('fraction of people')
plt.legend()
plt.savefig('Variation.png')
plt.close()
plt.legend(handles=patches, bbox_to_anchor=(1, 1), loc=6, borderaxespad=0. )
plt.imshow(a, cmap=cmap,norm=norm)
plt.savefig('final.png', bbox_inches='tight')
plt.close()
