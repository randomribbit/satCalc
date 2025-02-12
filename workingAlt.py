print("starting")
import ussa1976
import matplotlib
import numpy as np
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

volume = 1.05
massBase = 1

vList = []
aList = []
hList = []
volumeList = []
ds = ussa1976.compute(z=np.arange(0.0, 100001.0, 1.0), variables=["rho", "p", "t"])

EARTHMASS = 5.97219*10**24
G = 6.6743*10**-11
EARTHRADIUS = 6.378*10**6
# ideal gas constant using kPa
R = 8.314
# molar mass of helium (g)
HMOLE = 4.002602
# mass is the amount of helium we have. i am ignoring helium leakages for now because i want to and there are about 30 other variables.
# in grams
MASS = 178.4
N = MASS/HMOLE

#finds volume at a certain height, but pluging this derectly into the altitude equation doesn't work, probably bc calc
def volumeAt(height):
    h = int(height) 
    # kelvin
    temp = ds["t"].values[h]
    # kPa
    # add random constant for elasticity of balloon. this fixes things for some reason.
    pressure = ds["p"].values[h] /1000 +10
    v = (N*R*temp)/pressure
    v = v/1000
    return(v)

def acceleration(height):
    # accurate but super slow compute 
    #rhoDens = ussa1976.compute(z=np.arange(height, height+1, 1), variables=["rho"])
    #rhoDens = rhoDens["rho"].values[0]
    
    # test case, fast but less accurate
    h = int(height) 
    rhoDens = ds["rho"].values[h]

    #Theoretically accurate, though seems more impactful than it should, and gives out a 1m heigher number at v1 m1.22.
    #at v1 m1.2, the difference is about 0.09 meters lower with g calculation, which seems potentially promising. this is without advanced volume math.
    g = G*((EARTHMASS*massBase)/(h+EARTHRADIUS)**2)
    v = volumeAt(h)
    volumeList.append(v)
    g = 9.81
    bForce = rhoDens * volume * g
    netForce = bForce - massBase * g
    #mass base or weight?
    a = netForce/massBase
    return(a)
  
#testing
#ar = list(range(100000))
#ar = list(map(acceleration, ar)) 

def currentHeight():
    vHold = 0
    yHold = 1
    deltaT = 4
    for t in range(10000):
       # stop if balloon crashes
        if(yHold <0):
            break
        a = acceleration(yHold)        
        v = a*deltaT + vHold
        y = (1/2) * a * deltaT**2 + yHold
        #y = a*deltaT + vHold
        vHold = v
        yHold = y
        aList.append(a)
        vList.append(v)
        hList.append(y)
    print(yHold)
currentHeight()

# graph for generated data
fig, ax = plt.subplots()
print(len(hList))
#ax.plot(vList, c="red")
ax.plot(hList, c="purple")
ax.plot(aList, c="blue")
print(volumeList[0])
ax.plot(volumeList, c="orange")

#ax.plot(ar, c="green")
plt.show()

# graph for pressure at height
#plt.figure(dpi=100)
#ds.rho.plot(y="z", xscale="linear")
#plt.grid()
#plt.show()
