import matplotlib.pyplot as pl
from matplotlib.widgets import Button, Slider
from matplotlib.gridspec import GridSpec
import collections, serial
from serial.tools import list_ports
OBJ,CB,LAB = 0,1,2

class Interface():
    def __init__(self):

        # figure
        self.fig = pl.figure('Interface', figsize=[5,3])

        # button convention: name: [obj, callback, label]
        self.buts = collections.OrderedDict([   
                    ('Go', [None,self.evt_go,'Go']),
                    ('(nothing)', [None,self.evt_thing2,'(nothing)']),
                        ]) 
        # sliders convention: name : [obj, min, max, init]
        self.sliders = collections.OrderedDict([   
                    ('Speed', [None,0,9,1]),
                    ('Position', [None,1,6,1]),
                        ]) 

        # layout
        self.gs = GridSpec(len(self.buts), len(self.sliders), left=.1, bottom=0.05, top=.95, right=.9, width_ratios=[1,10], wspace=0.15, hspace=0.01)
        
        # buttons
        for bi,(name,(obj,cb,lab)) in enumerate(self.buts.items()):
            ax = self.fig.add_subplot(self.gs[bi,0])
            but = Button(ax, lab)
            but.on_clicked(cb)
            self.buts[name][OBJ] = but
        # sliders
        for si,(name,(obj,minn,maxx,init)) in enumerate(self.sliders.items()):
            ax = self.fig.add_subplot(self.gs[si,1])
            sli = Slider(ax, name, minn, maxx, init, facecolor='gray', edgecolor='none', alpha=0.5, valfmt='%0.0f')
            sli.label.set_position((0.5,0.5))
            sli.label.set_horizontalalignment('center')
            sli.vline.set_alpha(0)
            sli.on_changed(self.evt_slide)
            self.sliders[name][OBJ] = sli # hold onto reference to avoid garbage collection

        # arduino
        baud_rate = 9600
        all_ports = list(list_ports.comports()) # list of a 3-tuple for each port
        ports = [(port, desc) for port, desc, hwid in all_ports if "Arduino" in desc]
        if len(ports) > 0:
            arduino_port, arduino_desc = ports[0]
        else:
            print('debug error')
        self.ser = serial.Serial(arduino_port, baud_rate)

        self.speeds = {6:"f",5:"e",4:"d",3:"c",2:"b",1:"a"}

    def evt_go(self, *args):
        dx = self.sliders['Position'][OBJ].val
        v = self.sliders['Speed'][OBJ].val
        self.move(dx, v)
    def evt_thing2(self, *args):
        pass
    def evt_slide(self, *args):
        pass
    def move(self, dx, v):
        """
        dx : int, displacement value
        v : int 1-9, speed
        """
        msg = '{}{}'.format(dx, self.speeds[v])
        ser.write(msg)

if __name__ == '__main__':
    interface = Interface()
