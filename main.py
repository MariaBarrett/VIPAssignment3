from __future__ import division
from scipy.ndimage import filters
from resample import resample
from splinedraw import *
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


plt.gray() #print everything gray
plt.ion() #interactive mode

#-------------------------------------------------------------------------
img1 = np.array(Image.open("images/blacksquare.png"))
img2 = np.array(Image.open("images/kanizsa_triangle.gif"))


"""IniCurveDraw(image,number of points)
This function takes an image and gives you 5 sec to select some points. 
From these it draws an interpolated closed spline of num points. 
It calls Francois' functions to get initial curve and to draw it. 
The interpolated points are plotted using green circles
"""
def IniCurveDraw(im, num):

	plt.imshow(im)
	x, y, points = getInitialCurve(im, num)
	drawCurve(x,y,im)
	return x, y



"""sysmatrix(N,alpha,beta,tao)
This function takes 5 different inputs, which can be specified by the user.
It then solves the segmentation by creating a matrix of a linear system.
It then returns the inverse of said matrix.
"""
def sysmatrix(N,alpha,beta,tao):
	A = tao*beta
	B = -tao*(alpha+4*beta)
	C = 1 + tao*(2*alpha+6*beta)

	#fill system matrix
	M = np.zeros((N,N))
	M[0][0], M[0][1], M[0][2], M[0][-2], M[0][-1] = C, B, A, A, B
	for p in xrange(1, len(M)):
	    M[p] = np.roll(M[p-1],1)
	M = np.linalg.inv(M) 

	return M



def extenergy(im):
	iters = 50

	gaus = filters.gaussian_filter()
	LoG = filters.gaussian_laplace()

	sigma = 3
	fx = np.array(gaus(im,sigma,order=(1,0)))
	fy = np.array(gaus(im,sigma,order=(0,1)))
	fxy = np.array(gaus(fx, sigma,order=(0,1)))
	fxx = np.array(gaus(fx, sigma,order=(1,0)))
	fyy = np.array(gaus(fy,sigma,order=(0,1)))

	FX = -2*(fx*fxx + fy*fxy)
	FY = -2*(fx*fxy + fy*fyy)
	FI = -(LoG(im,sigma))**2

	IX = interp.InterpImage(FX)
	IY = interp.InterpImage(FY)
	II = interp.InterpImage(FI)

	return IX,IY,II

def calculate():
	print "ssomething something"


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
		print "You have 5 seconds to choose points for the initial curve \n"
		x = IniCurveDraw(img1, points)

	elif cmd == "2":
		points = nbr_points()
		step = step_by_step()
		print "You have 5 seconds to choose points for the initial curve \n"		
		x = IniCurveDraw(img2, points)
		

	elif cmd == "3":
		print "Quit succesfully."
		raise SystemExit()


	print "Please select the numerical values for alpha, beta and tao seperated by comma"
	v = raw_input("Alpha,beta,tao: ")
	v = v.split(',')

	for elem in v:
		if elem.isdigit() == False:
			break
			userinput()
	
	alpha,beta,tao = float(v[0]),float(v[1]),float(v[2])

	M = sysmatrix(len(x[1]),alpha,beta,tao)

	userinput()

"""main()
Starts the programme by calling the userinput-function
"""
def main():
    print ">>> Segmentation: Snakes by Maria, Guangliang and Alexander \n Vision and Image Processing assignment 3 \n";
    userinput();

if __name__ =='__main__':
    main(); 