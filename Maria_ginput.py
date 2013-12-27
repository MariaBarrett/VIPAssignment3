from __future__ import division
import pylab
from PIL import Image

img = pylab.imread("images/blacksquare.jpg")
pylab.imshow(img)
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