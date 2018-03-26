##

import os
from pseyepy import Camera, Stream, Display

path = '/Users/ben/Desktop'
file_name = '20180107_crayfish0'
file_name += os.path.join(path, file_name+'.avi')

##

c = Camera([0,1], resolution=Camera.RES_LARGE, fps=15)
d = Display(c)

## 

s = Stream(c, file_name=file_name, codec='png')

##

s.end()
c.end()

##
