from __future__ import division
import pylab
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

pylab.gray()

img = np.array(Image.open("images/blacksquare.jpg"))
print img
#img = np.array("images/blacksquare.jpg",dtype="float32")

pylab.imshow(img)

#plt.gray()
#plt.imshow(img)

pylab.axis([-1, 1, -1, 1])
print "Please click four times"
pts = pylab.ginput(4) # it will wait for three clicks
print "The point selected are"
print pts # ginput returns points as tuples
x=map(lambda x: x[0],pts) # map applies the function passed as 
y=map(lambda x: x[1],pts) # first parameter to each element of pts
pylab.plot(x,y,'-o')
pylab.axis([-1, 1, -1, 1])
pylab.show()