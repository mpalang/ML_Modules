# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 15:05:35 2024

@author: mola4305
"""

import numpy as np
import tkinter as tk
from pathlib import Path


class APP:
    def __init__(self,root):
        
        self.root=root
        self.N_Levels=tk.IntVar()
        self.Max=tk.DoubleVar()
        self.Min=tk.DoubleVar()
        self.Igor=tk.BooleanVar()
        
        self.N_Levels.set(12)
        self.Max.set(1)
        self.Min.set(-0.4)
        self.Igor.set(True)
        
        tk.Label(root,text='Number of Levels').grid(column=0,row=0)
        N_Entry=tk.Entry(root,textvariable=self.N_Levels)
        N_Entry.grid(column=1,row=0,columnspan=2)
        tk.Label(root,text='Maximum').grid(column=0,row=1)
        Max_Entry=tk.Entry(root,textvariable=self.Max)
        Max_Entry.grid(column=1,row=1,columnspan=2)
        tk.Label(root,text='Minimum').grid(column=0,row=2)
        Min_Entry=tk.Entry(root,textvariable=self.Min)
        Min_Entry.grid(column=1,row=2,columnspan=2)
        
        OK_Button=tk.Button(root,text='OK',command=self.calculate)
        OK_Button.grid(column=0,row=3)
        Igor_Box=tk.Checkbutton(root,text='For Igor?',variable=self.Igor,onvalue=True,offvalue=False)
        Igor_Box.grid(column=1,row=3)
        Save_Button=tk.Button(root,text='Save',command=self.save)
        Save_Button.grid(column=2,row=3)


    def calculate(self):
        N=self.N_Levels.get()
        Max=self.Max.get()
        Min=self.Min.get()
        
        if Max==0:
            N_pos=0
            N_neg=N-1
        
        elif Min==0:
            N_pos=N-1
            N_neg=0
        
        else: 
            N_neg=int((N)/((Max/abs(Min))+1))
            N_pos=N-N_neg
                
        Positive_max=np.array((255,0,0))
        Positive_min=np.array((255,240,180))
        Negative_min=np.array((220,230,240))
        Negative_max=np.array((0,0,255))
        
        self.Positive_Colors=[(Positive_max+i*(Positive_min-Positive_max)/(N_pos-1)).astype(int) for i in range(N_pos)]
        self.Negative_Colors=[(Negative_min-i*(Negative_min-Negative_max)/(N_neg-1)).astype(int) for i in range(N_neg)]
        
        tk.Label(root,text=f'Pos.Cols.({N_pos}):').grid(column=3,row=0)
        tk.Label(root,text=f'0:').grid(column=3,row=1)
        tk.Label(root,text=f'Neg.Cols.({N_neg}):').grid(column=3,row=2)
        
        try:
            self.Colors_Frame.destroy()
        except:
            pass
        
        self.Colors_Frame=tk.Frame(root)
        self.Colors_Frame.grid(row=1,column=4)
        self.counter=0
        for rgb in self.Positive_Colors:
            self.show_color(rgb,row=0)
        
        self.counter=0
        self.show_color((255,255,255),row=1)
        
        self.counter=0
        for rgb in self.Negative_Colors:
            self.show_color(rgb,row=2)
            
        self.Colors=np.concatenate([self.Positive_Colors,np.array([(255,255,255)]),self.Negative_Colors])
 

    def show_color(self,rgb,row=0):
        # Create a canvas to display the color

        canvas = tk.Canvas(self.Colors_Frame, width=30, height=30, bg=self.rgb_to_hex(rgb))
        canvas.grid(column=self.counter+4,row=row)
        self.counter=self.counter+1

    
    def rgb_to_hex(self,rgb):
        """Convert RGB values to a hexadecimal color string."""
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
    
    def get_levels(self,lmin,lmax,N):
        Npos=int(N/((-lmin/lmax)+1))
        Nneg=N-Npos
        lpos=(np.array([lmax-(2*i+1)*lmax/(2*Npos+1) for i in range(Npos+1)])+np.array([lmax-(2*i+1)*abs(lmin)/(2*Nneg+1) for i in range(Npos+1)]))/2
        lneg=(np.array([-(2*i+1)*lmax/(2*Npos+1) for i in range(Nneg+1)])+np.array([-(2*i+1)*abs(lmin)/(2*Nneg+1) for i in range(Nneg+1)]))/2
        levels=np.concatenate((lpos,lneg))
        levels=np.array([round(i,2) for i in levels])
        return levels
    
    def save(self):
        if self.Igor.get():
            self.Colors=self.Colors*65535/255
        
        Levels=self.get_levels(self.Min.get(),self.Max.get(),self.N_Levels.get())
        # np.savetxt(Path(Path(__file__).parent.parent.parent.parent.parent,'Color_List.txt'),self.Colors,delimiter=',',header='Red,Green,Blue',comments='')
        # np.savetxt(Path(Path(__file__).parent.parent.parent.parent.parent,'Levels.txt'),np.linspace(self.Max.get(),self.Min.get(),self.N_Levels.get()))
        np.savetxt(Path(Path(__file__).parent,'Color_List.txt'),self.Colors,delimiter=',',header='Red,Green,Blue',comments='')
        np.savetxt(Path(Path(__file__).parent,'Levels.txt'),Levels)
        
        self.root.destroy()


# =============================================================================
# Execute:
# =============================================================================

if __name__=="__main__":
    root=tk.Tk()
    
    app=APP(root)

    root.mainloop()
