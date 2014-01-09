from __future__ import division
from scipy.ndimage.filters import gaussian_filter as gaus
from resample import resample
from splinedraw import *
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import interpimage as interp


plt.gray() #print everything gray
plt.ion() #interactive mode

#-------------------------------------------------------------------------
img1 = np.array(Image.open("images/blacksquare.png"))
img2 = np.array(Image.open("images/kanizsa_triangle.gif"))
img3 = np.array(Image.open("images/coins.jpg"))


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



"""sysmatrix(N,alpha,beta,tau)
This function takes 5 different inputs, which can be specified by the user.
It then solves the segmentation by creating a matrix of a linear system.
It then returns the inverse of said matrix.
"""
def sysmatrix(N,alpha,beta,tau):
	A = tau*beta
	B = -tau*(alpha+4*beta)
	C = 1 + tau*(2*alpha+6*beta)

	#fill system matrix
	M = np.zeros((N,N))
	M[0][0], M[0][1], M[0][2], M[0][-2], M[0][-1] = C, B, A, A, B
	for p in xrange(1, len(M)):
	    M[p] = np.roll(M[p-1],1)
	M = np.linalg.inv(M) 
	Matrix = np.matrix(M)
	return Matrix

def extenergy(im):
	sigma = 1.4
	fx = np.array(gaus(im,sigma,order=(1,0)))
	fy = np.array(gaus(im,sigma,order=(0,1)))
	fxy = np.array(gaus(im, sigma,order=(1,1)))
	fxx = np.array(gaus(im, sigma,order=(2,0)))
	fyy = np.array(gaus(im,sigma,order=(0,2)))


	FX = -2*(fx*fxx + fy*fxy)
	FY = -2*(fx*fxy + fy*fyy)

	IX = interp.InterpImage(FX)
	IY = interp.InterpImage(FY)

	return IX,IY

"""
def vari()
This function prompts the user for alpha, beta, tau en gamma values. It validates the number and type of the input
"""
def vari():
	print "Please select the numerical values for alpha, beta, tau and gamma seperated by comma"
	v = raw_input("Alpha,beta,tau,gamma: ")
	v = v.split(',')

	if len(v) == 4:
		for elem in v:
			try:
    				float(elem) #don't know why it only accepts double indentation
			except ValueError:
    				print "Invalid input. Only int and floats allowed"
    				userinput()
	else: 
		print "Invalid input. Enter exactly 4 values separated by comma"
		userinput()

	
	alpha,beta,tau,gamma = float(v[0]),float(v[1]),float(v[2]),float(v[3])
	return alpha, beta, tau, gamma


	"""
	@TODO: Utilize the new_x and new_y so that our coordinates update correctly.
	Currently we are rewriting the x variable as soon as the calculation for x is done, meaning the y calculation is done with the old y but a new x, which is not correct!
	It should then compute with these updated x and y values (like the dot product of M*x and M*y).
	If you are confused, check the slides on the LINEAR SYSTEM (not system matrix).
	Hint: you can use new_x and new_y or just a zero array.
	"""
"""
def calculate(x, y, Fp, alpha, beta, tau, gamma)
This function calls the systemmatrix function to calculate the inv matrix
From the array of x and y coordinates it updates the values and plots a fraction of them onto the image
"""
def calculate(x, y, Fp, alpha, beta, tau, gamma):
	new_x = np.copy(x)
	new_y = np.copy(y)	

	Minv = sysmatrix(len(x),alpha,beta,tau)

	for c in xrange(100): # number of iterations
	    for i in range(len(x)):
	        bx = Fp[0].bilinear(x[i],y[i]) #Wrong
	        new_x[i] = x[i]-gamma*bx
	        
	        by = Fp[1].bilinear(x[i],y[i]) #Wrong
	       	new_y[i] = y[i]-gamma*by

	    x = new_x
	    y = new_y

	    x = np.matrix(x)
	    y = np.matrix(y)

	    x = np.dot(Minv, np.transpose(x)) #which to use?
	    y = np.dot(Minv, np.transpose(y))

	    #x = np.dot(x, Minv) #or this one? Neither is really good
	    #y = np.dot(y, Minv)
	    
	    x = np.squeeze(np.asarray(x)) 
	    y = np.squeeze(np.asarray(y)) 
	    	
	    if c % 10 == 0: 
	    	print x
	    	plt.plot(np.append(x,[x[0]]), np.append(y,[y[0]]), "r-")

	plt.show()
	userinput()

#--------------------------------------------------------------------------
#Interface
##Settings 


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
	print "3. Coins"
	print "4. Exit"
	print "-"*45
	usercmd = raw_input("Choose an option: ")
	commands(usercmd)
	

"""commands(cmd)
This function takes an integer as input, which is validated.
It then calls settings-functions which promps the user for entering settings for the snake or SystemExit().
When that function is done, it will call userinput() again.
"""
def commands(cmd):
	plt.close()
	legal = ["1","2","3","4"]

	if cmd not in legal:
		print "Invalid input. Please enter one of the possible values.\n"
		userinput()

	elif cmd == "1":
		print "You have 5 seconds to choose points for the initial curve \n"
		x,y = IniCurveDraw(img1, 100)
		Fp = extenergy(img1)
		alpha, beta, tau, gamma = vari()
		calculate(x, y, Fp, alpha, beta, tau, gamma)

	elif cmd == "2":
		print "You have 5 seconds to choose points for the initial curve \n"		
		x,y = IniCurveDraw(img2, 100)
		Fp = extenergy(img2)
		alpha, beta, tau, gamma = vari()
		calculate(x, y, Fp, alpha, beta, tau, gamma)

	elif cmd == "3":
		print "You have 5 seconds to choose points for the initial curve \n"		
		x,y = IniCurveDraw(img3, 100)
		Fp = extenergy(img3)
		alpha, beta, tau, gamma = vari()
		calculate(x, y, Fp, alpha, beta, tau, gamma)

	elif cmd == "4":
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


"""
alpha :      elasticity parameter (membrane)
beta :       rigidity parameter (thin plate)
"""