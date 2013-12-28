from __future__ import division
import pylab
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from splinedraw import *
from resample import resample

plt.gray() #print everything gray

img = np.array(Image.open("images/blacksquare.png"))

def IniCurveDraw(im, num):
	"""
	This function takes an image and gives you 5 sec to select some points. 
	From these it draws an interpolated closed spline of num points. 
	It calls Francois' functions to get initial curve and to draw it. 
	The interpolated points are plotted using green circles
	"""
	plt.imshow(img)
	x, y, points = getInitialCurve(img, num)
	plt.figure()
	drawCurve(x,y,img)
	plt.show()

IniCurveDraw(img,20)