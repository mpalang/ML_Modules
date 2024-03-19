# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 11:49:15 2023

@author: morit
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 10:01:47 2022

@author: work
"""
import sys
sys.path.append(r'C:\Users\morit\OneDrive - UCB-O365\11_Software\Python\ML_Modules\Plotting')
import numpy as np
from MLPlot import MLplot as plot


#%%

filepath=r'C:\Users\morit\OneDrive - UCB-O365\03_Data\procd_fs.mat'#GUI.SelectFile()
# filepath2="Z:/Nutzer/Lang/privat/02_Projekte/Huerta_Cu_TiO2_LIKAT/NMP/Re _AW _NMP_spectra/Blanknmp2.dat"#GUI.SelectFile()

delimiter=';'


#%%

# def getText(filepath):
    
t=np.fromfile(filepath,dtype=np.dtype('|S1'),count=-1,offset=0)
text=[]
for i in t:
    try: 
        text.append(i.decode("utf-8"))
    except:
        text.append(None)

#%%
text_str=""
for i in text:
    try:
        text_str+=i
    except:
        text_str+="_"

#%%
s=100000 #<8000000
start=[s,s+1,s+2,s+3]
count=2600
data={}
for n,s in enumerate(start):
    data[str(n)]=np.fromfile(filepath,dtype=np.float32,count=count+1,offset=s)
del(s)



for i in data.keys():
    plot(None,data[i])

#%%

np.savetxt(filepath.replace('.dat','.csv'),np.column_stack((data['XDATA'],data['YDATA'])),fmt='%.6f',delimiter=delimiter)