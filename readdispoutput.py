# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 18:02:54 2018

@author: mvrri
"""
from abaqusConstants import *
from odbAccess import *
from textRepr import *
import numpy as np
import csv
odbName='Frequency'
odb=openOdb(odbName+'.odb',readOnly=True)
step1=odb.steps['Step-1']
frame=step1.frames[-1]
displ=frame.fieldOutputs['U']
displvalues=displ.values
dispres=np.zeros(shape=[len(displvalues),3])
for k in range(len(displvalues)):
    dispres[k]=np.array(displvalues[k].data,dtype='object')
header2=np.array(['U1','U2','U3'],dtype=object)
dispres=np.vstack((header2,dispres))
with open('results1.csv','wb') as csvfile:
    filewriter=csv.writer(csvfile, delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL)
    for i in range(len(dispres)):
        filewriter.writerow(dispres[i])
