"""
import sqlite3
conn=qlite3.connect("project.db")
cur=conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS IMAGE(S.NO INTEGER, FILEPATH TEXT)")
conn.commit()
conn.CLOSE()
"""
from tkinter import *
import backend1 as backend
def view_command():
    ldisp.delete(0,END)
    for row in backend.view():
        ldisp.insert(END,row)

def add_command():
    backend.insert(ImPath.get(),UName.get())
    ldisp.delete(0,END)
    ldisp.insert(END,(ImPath.get(),UName.get()))

def delete_command():
    backend.delete(int(PID.get()))
    view_command()

def img_search_command():
    backend.ImgSearch(int(PID.get()),FilePath.get())


def getSelectedRow(event):
    index=ldisp.curselection()[0]
    selected_tuple=ldisp.get(index)

#-----------------------------------------------------------
window=Tk()
lblIPath=Label(window,text="Enter Image Path: ")
lblIPath.grid(row=0,column=0)
lblFPath=Label(window,text="Enter Search Folder: ")

lblFPath.grid(row=1,column=0)

lblFaceName=Label(window,text="Name of Person: ")
lblFaceName.grid(row=0,column=2)
lblID=Label(window,text="ID: ")
lblID.grid(row=1,column=2)
PID=StringVar()
eID=Entry(window,textvariable=PID)
eID.grid(row=1,column=3)
ImPath=StringVar()
eIP=Entry(window,textvariable=ImPath)
eIP.grid(row=0,column=1)
FilePath=StringVar()
eFP=Entry(window,textvariable=FilePath)
eFP.grid(row=1,column=1)
UName=StringVar()
eUN=Entry(window,textvariable=UName)
eUN.grid(row=0,column=3)
ldisp=Listbox(window,height=6,width=36)
ldisp.grid(row=2,column=0,rowspan=6,columnspan=2)
sbdisp=Scrollbar(window)
sbdisp.grid(row=2,column=2,rowspan=6)
ldisp.configure(yscrollcommand=sbdisp.set)
sbdisp.configure(command=ldisp.yview)
#--------------------------------------------------------------
ldisp.bind('<<ListboxSelect>>',getSelectedRow)

b1=Button(window,text="View All",width=12,command=view_command)
b1.grid(row=2,column=3)
b2=Button(window,text="Add in DB",width=12,command=add_command)
b2.grid(row=3,column=3)
b3=Button(window,text="Delete",width=12,command=delete_command)
b3.grid(row=4,column=3)
b4=Button(window,text="Search Images",width=12,command=img_search_command)
b4.grid(row=5,column=3)
window.mainloop()