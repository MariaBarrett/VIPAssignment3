import scipy
from scipy.ndimage import filters
import pylab
import numpy as np


LoG = filters.gaussian_laplace



def E1(t,N):
	g = np.linalg.norm(LoG(t,1.4))**2
	result = -0.5 * scipy.integrate.quad(g,0,N)

	return result




def E2(t,N):
	g = -(LoG(t,1.4))**2
	result = scipy.integrate.quad(g,0,N)

	return result