# -*- coding: utf-8 -*-

#  fatal I module
#  fatalgui.py

#  Copyright � 2009-2014 Ancestors Soft

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.


from fatalvar import *
import fatalapi

try:
    import tkinter
except ImportError:
    pass

try:
    import tkinter.ttk
    wlib = ttk
except ImportError:
    wlib = Tkinter

#------------------------------- fatal GUI routines ---------------------------

def fatal_gui():
    ftk = tkinter.Tk()
    
    flf_frame = wlib.Frame(ftk)
    frt_frame = wlib.Frame(ftk)
    flf_frame.grid(row=0, column=0, sticky='nw')
    frt_frame.grid(row=0, column=1, sticky='ne')
    
    set_fatal_var('ftk', '.', 'tw', ftk)
    set_fatal_var('ftk', '.', 'mframe', 'frame', flf_frame)
    
    ftk.wm_title('fatal-bot v2.x')
    
    mxs = ftk.maxsize()
    
    scwidth = mxs[0]
    scheight = mxs[1] 
    
    hscwidth = int(scwidth * 0.8)
    hscheight = int(scheight * 0.7)
    
    dxpos = int(scwidth / 2) - int(hscwidth / 2) 
    dypos = int(scheight / 2) - int(hscheight / 2)
    
    ftk.wm_geometry('%sx%s+%s+%s' % (hscwidth, hscheight, dxpos, dypos))
    #ftk.wm_resizable(0, 0)
    ftk.iconbitmap('@fatal.xbm')
    
    fmn_menu = tkinter.Menu(ftk)
    ftk.configure(menu=fmn_menu)
    
    fmn_manage = tkinter.Menu(fmn_menu)
    fmn_menu.add_cascade(label="Manage", menu=fmn_manage)
    fmn_manage.add_command(label="Stop bot", command=fatalapi.interrupt)
    fmn_manage.add_command(label="Close GUI", command=ftk.destroy)
    
    flf_lstbx = tkinter.Listbox(flf_frame, width=1, height=hscheight)
    flf_lstbx.grid()
    print(flf_lstbx.size())
    #fmn_lstbx.pack()
    
    frt_ntbook = wlib.Notebook(frt_frame, width=70, height=hscheight)
    frame = tkinter.Frame()
    frame2 = tkinter.Frame()
  
    frt_ntbook.add(frame, text='System')
    frt_ntbook.add(frame2, text='Unknown')
      
    frt_ntbook.grid()
    
    #fmn_menu.pack()
    
    #stop_bot = wlib.Button(fmn_frame, text='Stop fatal-bot', command=fatalapi.interrupt)
    #close_panel = wlib.Button(fmn_frame, text=' Close panel ', command=ftk.destroy)
    
    #stop_bot.pack()
    #close_panel.pack()
    
    #set_fatal_var('ftk', '.', 'mframe', 'sbtn', stop_bot)
    #set_fatal_var('ftk', '.', 'mframe', 'cbtn', close_panel)
    
    ftk.iconify()
    ftk.update()
    ftk.deiconify()
    ftk.mainloop()