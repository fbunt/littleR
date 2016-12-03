import matplotlib.pyplot as plt
import numpy as np
import os


ITIME = 0
IPRES = 1
ITEMP = 2
IRH = 3
IWS = 4
IWD = 5
ILAT = 6
ILON = 7


# fdin = open(os.path.abspath('../../GrawProfile_7_14_SLU.txt'), encoding='latin-1')
# fdout = open(os.path.join(os.path.abspath('../../'), 'out.r'), 'w')
data = np.genfromtxt('../../GrawProfile_7_14_SLU.txt', skip_header=3, skip_footer=10, unpack=1)

lat = data[ILAT]
lon = data[ILON]
