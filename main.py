from __future__ import division
import pylab
import scipy
from scipy.ndimage import filters
import pylab
import numpy as np
from resample import resample
from splinedraw import *
import matplotlib.pyplot as plt
from PIL import Image

plt.gray() #print everything gray

#-------------------------------------------------------------------------
img1 = np.array(Image.open("images/blacksquare.png"))
img2 = np.array(Image.open("images/kanizsa_triangle.gif"))


def IniCurveDraw(im, num):
	"""
	This function takes an image and gives you 5 sec to select some points. 
	From these it draws an interpolated closed spline of num points. 
	It calls Francois' functions to get initial curve and to draw it. 
	The interpolated points are plotted using green circles
	"""
	plt.imshow(im)
	x, y, points = getInitialCurve(im, num)
	plt.figure()
	drawCurve(x,y,im)
	plt.show()


LoG = filters.gaussian_laplace



def E1(t,N):
	g = np.linalg.norm(LoG(t,1.4))**2
	result = -0.5 * scipy.integrate.quad(g,0,N)

	return result




def E2(t,N):
	g = -(LoG(t,1.4))**2
	result = scipy.integrate.quad(g,0,N)

	return result

#--------------------------------------------------------------------------
#Interface
##Settings 
"""step-by-step()
This function allows the user to select whether the segmentation i performed step-by-step or not.
The  

"""
def step_by_step():
	legal = ["y", "n"]
	print "-"*45
	print "Do you want to perform the analysis step by step?"
	print "-"*45
	usercmd = raw_input("y or n:")

	if usercmd == "y":
		print "You perform step-by-step." 
		return True
		
	if usercmd == "n":
		print "You do not perform step-by-step."
		return False
	
	if usercmd not in legal:
		print "invalid input"
		userinput()
		


"""nbr_points()
This functions allows the user to choose number of points in the snake. 
If the submitted string contains only digits, it is turned into int, validated and returned from the function.
"""
def nbr_points():
	print "-"*45
	print "Select number of points in the curve.\n"
	nbr_points = raw_input("Write an integer between 5 and 50:")
	if nbr_points.isdigit():
		nbr_points = int(nbr_points)
		if nbr_points < 51 and nbr_points > 4:
			return nbr_points
		else:
			print "Invalid input"
			userinput()
	else:
		print "Invalid input"
		userinput()


## Menu 

"""userinput()
This function is called at the beginning and takes a user input.
The input is then used as an ouput to call the commands(cmd) function.
"""
def userinput():
	print "="*60
	print "Choose between 2 images. \n"
	print "-"*45
	print "1. Black square"
	print "2. Kanizsa triangle"
	print "3. Exit"
	print "-"*45
	usercmd = raw_input("Choose an option: ")
	commands(usercmd)
	

"""commands(cmd)
This function takes an integer as input, which is validated.
It then calls settings-functions which promps the user for entering settings for the snake or SystemExit().
When that function is done, it will call userinput() again.
"""
def commands(cmd):
	legal = ["1","2","3"]

	if cmd not in legal:
		print "Invalid input. Please enter one of the possible values.\n"
		userinput()

	elif cmd == "1":
		points = nbr_points()
		step = step_by_step()
		print "You have 5 seconds to choose points for the initial curve"
		IniCurveDraw(img1, points)
		userinput()

	elif cmd == "2":
		points = nbr_points()
		step = step_by_step()
		print "You have 5 seconds to choose points for the initial curve"
		IniCurveDraw(img1, points)
		userinput()

	elif cmd == "3":
		print "Quit succesfully."
		raise SystemExit()


"""main()
Starts the programme by calling the userinput-function
"""
def main():
    print ">>> Segmentation: Snakes by Maria, Guangliang and Alexander \n Vision and Image Processing assignment 3 \n";
    userinput();

if __name__ =='__main__':
    main(); 

