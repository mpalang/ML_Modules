# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 09:45:32 2024

@author: mola4305
"""

_drive=r'C:\Users\mola4305\OneDrive - UCB-O365'
# _drive=r'C:\Users\Mo\OneDrive - UCB-O365'

from pathlib import Path
import numpy as np
import pandas as pd
from scipy.io import loadmat
import sys
from matplotlib import pyplot as plt
from datetime import datetime

sys.path.append(str(Path(_drive,r'CukResearchGroup\TR-VIS\05_Scripts\Python\CukLabScripts')))
# from CukLabScripts import mat_data
from CukLabScripts import get_mat_data
sys.path.append(str(Path(_drive,r'04_Software\Python\ML_Modules\Plotting')))
from MLColors import contour_colors as cc

from iminuit import Minuit
from iminuit.cost import LeastSquares
from scipy.optimize import brute




#%%
class chirp_correct:
    def __init__(self,wl,dt,S,settings=None):
        
        self.wl=wl
        self.dt=dt
        self.S=S
        
        self.settings={'fromdt':-0.1,
                  'todt':2,
                  'fromwl':370,
                  'towl':660,
                  'step_size':10,
                  'limits':{},
                  'p0':{}}
               
        if settings:
            for key in settings:
                self.settings[key]=settings[key]
        
        self.cut_data()
        self.fit_t0()  
        self.chirp_fit()
        self.chirp_correction() 
        self.plot()

    # =============================================================================
    # Functions    
    # =============================================================================
    def cut_data(self):
        wl=self.wl
        dt=self.dt
        S=self.S
        fromwl=self.settings['fromwl']
        towl=self.settings['towl']
        fromdt=self.settings['fromdt']
        todt=self.settings['todt']
        step_size=self.settings['step_size']
        
        self.wl_cut=wl[np.argmax(wl>fromwl):np.argmax(wl>towl):step_size]
        self.dt_cut=dt[np.argmax(dt>fromdt):np.argmax(dt>todt)]
        self.S_cut=S[np.argmax(dt>fromdt):np.argmax(dt>todt),np.argmax(wl>fromwl):np.argmax(wl>towl):step_size]
        
    def fit_t0(self):
        #fit t0 for each wl point:
        def logistic(dt,A,k,t0):
            return A/(1+np.exp(-k*(dt-t0)))
        t0=[]
        for n in range(len(self.wl_cut)):        
            trace=self.S_cut[:,n]  
            ls=LeastSquares(self.dt_cut,trace,0.01,logistic)
            m=Minuit(ls,A=0.3,k=1,t0=0.5)
            m.limits['t0']=(self.settings['fromdt'],self.settings['todt'])
            m.migrad()
            t0.append(m.values['t0'])
        self.t0=np.array(t0)
            
    def damped_polynome(self,wl,wl0,a0,a1,a2,d):
        y=np.poly1d((a0,a1,a2))(wl)
        return y/(d*wl)
    
    def chirp_fit(self):   
        #Fit polynomial to t0s
        ls=LeastSquares(self.wl_cut,self.t0,0.01,self.damped_polynome)
        m=Minuit(ls,wl0=500,a0=0,a1=0,a2=0,d=1e-3)
        for parm in self.settings['limits'].keys():
            m.limits[parm]=self.settings['limits'][parm]
        for parm in self.settings['p0'].keys():
            m.params[parm]=self.settings['p0'][parm]
        
        m.migrad()
        self.chirp_parms=m.values
       
    def chirp_correction(self):
        # Chirp Corr:
        self.S_corr=np.zeros(self.S.shape)
        for n,w in enumerate(self.wl):
            self.S_corr[:,n]=np.interp(self.dt,self.dt-self.damped_polynome(w,*self.chirp_parms),self.S[:,n]) 

    
    def plot(self):      
        #Plot
        fig,axs=plt.subplots(1,2,dpi=30,figsize=(10,3))
        levels,colors=cc(-0.5,0.5,20)
        axs[0].contourf(self.wl,self.dt,self.S,colors=colors,levels=levels)
        axs[0].plot(self.wl,self.damped_polynome(self.wl,*self.chirp_parms),color='lime')
        axs[0].axhline(self.settings['fromdt'])
        axs[0].axhline(self.settings['todt'])
        axs[0].axvline(self.settings['fromwl'])
        axs[0].axvline(self.settings['towl'])
        
        axs[1].contourf(self.wl,self.dt,self.S_corr,colors=colors,levels=levels)
        
        for ax in axs.flat:
            # ax.set_yscale('log')
            ax.set_ylim((-1,10))
        
        self.fig=fig



