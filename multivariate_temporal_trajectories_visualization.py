# -*- coding: utf-8 -*-
"""
Created on Sun Nov 08 14:28:40 2020

@author: Johannes
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt    
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import matplotlib.colors as colors
import matplotlib.cm as cmx    
import os,sys

import matplotlib
matplotlib.rcParams['font.sans-serif'] = "Arial"
matplotlib.rcParams['font.family'] = "sans-serif"
#matplotlib.rcParams['font.size'] = 4 

### read some country level statistics 
#Source: United Nations, 
#Department of Economic and Social Affairs, Population Division (2019). 
#World Population Prospects 2019 - Special Aggregates, Online Edition. Rev. 1.)
popdata=pd.read_csv('totpop.csv')
agedata=pd.read_csv('medianage.csv')
sexdata=pd.read_csv('sexratio.csv')

### specify relevant columns for t-SNE transform:
relcols=['pop','medianage','sexratio'] 

### selected objects (here: countries) to be labelled in the plot:
example_labels=['Germany','Mexico','Burundi','Australia','Luxembourg','Viet Nam','Lesotho']
label_examples=True

## some cleaning and restructuring: ##############################
agedata=agedata[agedata['Country code']<900]
popdata=popdata[popdata['Country code']<900] 
sexdata=sexdata[sexdata['Country code']<900]

## country name dictionary:
obj_dict = dict(agedata[['Country code','Region, subregion, country or area *']].values)
  
years=np.arange(1950,2021,10)
agedata=agedata[['Country code']+[str(int(x)) for x in years]]
popdata=popdata[['Country code']+[str(int(x)) for x in years]]
sexdata=sexdata[['Country code']+[str(int(x)) for x in years]] 
  
agedata.columns=['Country code']+['medianage%s' %x for x in agedata.columns[1:]]
popdata.columns=['Country code']+['pop%s' %x for x in popdata.columns[1:]]
sexdata.columns=['Country code']+['sexratio%s' %x for x in sexdata.columns[1:]]

mergeddata=agedata.merge(popdata,on='Country code').merge(sexdata,on='Country code')
for col in mergeddata.columns:
    mergeddata[col]=mergeddata[col].map(str).str.replace(' ','')
    mergeddata[col]=mergeddata[col].map(float)
        
datadf=pd.DataFrame()
for year in years:
    yeardf=pd.DataFrame()
    yeardf['object']=mergeddata['Country code']
    yeardf['pop']=mergeddata['pop%s' %year]
    yeardf['medianage']=mergeddata['medianage%s' %year]
    yeardf['sexratio']=mergeddata['sexratio%s' %year]
    yeardf['time']=year
    datadf=datadf.append(yeardf)

###############################################################################

fig,ax=plt.subplots()
ax.scatter(x=datadf['medianage'].values,y=np.log(datadf['pop'].values),s=1,alpha=0.5)
ax.set_ylabel('Log(Population)')
ax.set_xlabel('Median age')
plt.show()
fig.savefig('scat_pop_medage.jpg',dpi=90) 

fig,ax=plt.subplots()
ax.scatter(x=datadf['sexratio'].values,y=np.log(datadf['pop'].values),s=1,alpha=0.5)
ax.set_ylabel('Log(Population)')
ax.set_xlabel('Women per 100 men')
plt.show()
fig.savefig('scat_pop_sexratio.jpg',dpi=90) 

fig,ax=plt.subplots()
ax.scatter(x=datadf['medianage'].values,y=datadf['sexratio'].values,s=1,alpha=0.5)
ax.set_xlabel('Median age')
ax.set_ylabel('Women per 100 men')
plt.show()
fig.savefig('scat_medianage_sexratio.jpg',dpi=90)

###############################################################################

datadf=datadf.sort_values(by=['object','time'])

#transform to log, assumed to be skewed
datadf['pop']=np.log(1+datadf['pop'].values) 

#scale to (0,1)
datadf['pop']=np.divide(datadf['pop'],np.nanmax(datadf['pop']))
datadf['medianage']=np.divide(datadf['medianage'],np.nanmax(datadf['medianage']))
datadf['sexratio']=np.divide(datadf['sexratio'],np.nanmax(datadf['sexratio']))

# as baseline t-SNE model, to be refined by the user.
model = TSNE(n_components=2,n_iter = 1000, random_state=0)

np.set_printoptions(suppress=True)
tsnecoords = model.fit_transform(datadf[relcols].values)  

datadf['tsne_x']=tsnecoords[:,0]
datadf['tsne_y']=tsnecoords[:,1]

#plot trajectories: ###########################################################
cmap=plt.get_cmap('jet')
uniq = np.unique(datadf.time.values)
cNorm  = colors.Normalize(vmin=0, vmax=len(uniq))
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cmap)    

fig = plt.figure()
#plot.style.use('dark_background')
plt.grid(False)
objcount=0
for objid,objdf in datadf.groupby('object'):
    objdf=objdf.sort_values(by='time')               
    currptsx = objdf.tsne_x.values
    currptsy = objdf.tsne_y.values
    count=0
    for segment in np.arange(0,currptsx.shape[0]):
        segmx=currptsx[segment:segment+2]
        segmy=currptsy[segment:segment+2]
        plt.plot(segmx, segmy, color=scalarMap.to_rgba(count),alpha=0.6, linewidth=1,zorder=1) #scalarMap.to_rgba(count)
        
        if label_examples and obj_dict[objid] in example_labels:
            if count==0:
                plt.annotate(obj_dict[objid]+' %s' %years[count], (currptsx[segment], currptsy[segment]),color='white',fontsize=8,zorder=2)                           
                plt.scatter(x=currptsx[segment], y=currptsy[segment],c='white',s=1,zorder=2)
            if count==currptsx.shape[0]-1:
                plt.annotate(obj_dict[objid]+' %s' %years[count], (currptsx[segment], currptsy[segment]),color='white',fontsize=8,zorder=2)
                plt.scatter(x=currptsx[segment], y=currptsy[segment],c='white',s=1,zorder=2)
        count+=1
                                 
ax = plt.gca()
ax.set_facecolor('black')         
plt.show()
fig.savefig('tsne_trajectories.jpg',dpi=150)    