import matplotlib.pyplot as pl
from matplotlib.widgets import Button, Slider
from matplotlib.gridspec import GridSpec
import numpy as np
import matplotlib as mpl
import collections, serial
from serial.tools import list_ports
OBJ,CB,LAB = 0,1,2
mpl.rcParams['toolbar'] = 'None'

class IntSlider(Slider):
    def __init__(self, *args, **kwargs):
        Slider.__init__(self, *args, **kwargs)

    def set_val(self, val):
        val_int = int(np.round(val))
        self.val = val_int
   
        self.valtext.set_text(self.valfmt % val_int)

        xy = self.poly.get_xy()
        xy[2] = (val_int, 1)
        xy[3] = (val_int, 0)
        self.poly.set_xy(xy)
        
        if self.drawon: 
            self.ax.figure.canvas.draw()
        if not self.eventson: 
            return
        for _,fxn in self.observers.items():
            fxn(val_int)

class Interface():
    def __init__(self):

        # arduino
        baud_rate = 9600
        self.speeds = {6:"f",5:"e",4:"d",3:"c",2:"b",1:"a"}

        arduino_port = '/dev/cu.usbmodem1411'
        self.ser = serial.Serial(arduino_port, baud_rate)

        all_ports = list(list_ports.comports()) # list of a 3-tuple for each port
        ports = [(port, desc) for port, desc, hwid in all_ports if "Arduino" in desc]
        if len(ports) > 0:
            arduino_port, arduino_desc = ports[0]

        else:
            pass
            #raise Exception('Arduino not detected.')

        # button convention: name: [obj, callback, label]
        self.buts = collections.OrderedDict([   
                    ('Go', [None,self.evt_go,'Go']),
                        ]) 
        # sliders convention: name : [obj, min, max, init]
        self.sliders = collections.OrderedDict([   
                    ('Speed', [None,0,6,1]),
                    ('Displacement', [None,0,9,0]),
                        ]) 
        
        # figure & layout
        self.fig = pl.figure('Interface', figsize=[7,2])
        self.fig.canvas.mpl_connect('close_event', self.on_close)
        self.gs = GridSpec( max(len(self.buts), len(self.sliders)), 
                            2,
                            left=.1, 
                            bottom=0.05, 
                            top=.95, 
                            right=.9, 
                            width_ratios=[1,5], 
                            wspace=0.25, 
                            hspace=0.2)
        
        # add buttons
        for bi,(name,(obj,cb,lab)) in enumerate(self.buts.items()):
            ax = self.fig.add_subplot(self.gs[bi,0])
            but = Button(ax, lab)
            but.on_clicked(cb)
            self.buts[name][OBJ] = but
        
        # add sliders
        for si,(name,(obj,minn,maxx,init)) in enumerate(self.sliders.items()):
            ax = self.fig.add_subplot(self.gs[si,1])
            sli = IntSlider(ax, name, minn, maxx, init, facecolor='gray', edgecolor='none', alpha=0.5, valfmt='%0.0f')
            sli.label.set_position((0.5,0.5))
            sli.label.set_horizontalalignment('center')
            sli.vline.set_alpha(0)
            sli.on_changed(self.evt_slide)
            self.sliders[name][OBJ] = sli # hold onto reference to avoid garbage collection

    def evt_go(self, *args):
        dx = self.sliders['Displacement'][OBJ].val
        v = self.sliders['Speed'][OBJ].val
    
        if v == 0:
            return

        self.move(dx, v)

    def evt_slide(self, *args):
        pass

    def move(self, dx, v):
        """
        dx : int, displacement value
        v : int 1-9, speed
        """
        msg = '{}{}'.format(dx, self.speeds[v])
        print(msg)
        self.ser.write(msg)

    def on_close(self, *args):
        try:
            self.ser.close()
        except:
            pass

if __name__ == '__main__':
    interface = Interface()
