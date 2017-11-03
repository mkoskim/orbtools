###############################################################################
#
# Orbit visualizer
#
###############################################################################

from orbtools import *

from Tkinter import *

#-----------------------------------------------------------------------------

root = Tk()
root.title("Orbtools")
#root.geometry("700x500")

#-----------------------------------------------------------------------------

class Window(Frame):

    def __init__(self, parent = None):
        Frame.__init__(self, parent, pady = 5, padx = 5)
        self.pack(fill=BOTH, expand=1)
        
        w = Canvas(self, width=200, height=100)
        w.pack()

        w.create_line(0, 0, 200, 100)
        w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))

#-----------------------------------------------------------------------------

def window():
    return Window(root)

#-----------------------------------------------------------------------------

def run():
    #app = Window(root)
    root.mainloop()
