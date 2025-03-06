print("starting")
import ussa1976
import matplotlib
import numpy as np
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

volume = 13.74
#1.225
massBase = 5

vList = []
aList = []
hList = []
volumeList = []
maxList = []
massList = []

ds = ussa1976.compute(z=np.arange(0.0, 100001.0, 1.0), variables=["rho", "p", "t", "mu"])

EARTHMASS = 5.97219*10**24
G = 6.6743*10**-11
EARTHRADIUS = 6.378*10**6
# ideal gas constant using kPa
R = 8.31446
# molar mass of helium (g)
HMOLE = 4.002602
# mass is the amount of helium we have. i am ignoring helium leakages for now because i want to and there are about 30 other variables.
# in grams, 178.4 is a cubic meter of He
MASS = 629.753
N = MASS/HMOLE

# boltzmann constant
boltz = 1.3806*10**-23
# molar mass of dry air
airMass = 0.0289652



#finds volume at a certain height, but pluging this derectly into the altitude equation doesn't work, probably bc calc
def volumeAt(height):
    h = int(height) 
    # kelvin
    temp = ds["t"].values[h]
    # kPa
    # add random constant for elasticity of balloon. this fixes things for some reason.
    pressure = ds["p"].values[h] /1000 
    v = (N*R*temp)/pressure
    #print("P = ")
    #print(pressure)
    v = v/1000
    return(v)
bfo = []

def acceleration(height, mass, velocity):
    # accurate but super slow compute 
    #rhoDens = ussa1976.compute(z=np.arange(height, height+1, 1), variables=["rho"])
    #rhoDens = rhoDens["rho"].values[0]

    # slightly less accurate because it sets height as a int, should be good enough though. 
    h = int(height) 
    rhoDens = ds["rho"].values[h]
    mu = ds["mu"].values[h]
    
    #Theoretically accurate, though seems more impactful than it should, and gives out a 1m heigher number at v1 m1.22.
    #at v1 m1.2, the difference is about 0.09 meters lower with g calculation, which seems potentially promising. this is without advanced volume math.
    g = ((G*EARTHMASS)/(h+EARTHRADIUS)**2)
    #v = volumeAt(h)
    #print("volume = " + str(v))
    #volumeList.append(v)
    bForce = rhoDens * volume * g
    bfo.append(bForce)
    
    Area = 18
    Cd = 0.145
    D = 4.8
    mu = mu * 10**-12
    Re = rhoDens*velocity*D/mu 
    #print("re")
    #print(Re)
    
    dragForce = Cd*rhoDens*abs(velocity)*velocity*Area*1/2
    #print(dragForce)
    netForce = bForce - (mass * g) -dragForce
    a = netForce/mass 
    
    #print("rho= " + str(rhoDens))
    #print("g="+str(g))
    #print("fb=" + str(bForce))
    #print("fn=" + str(netForce))
    #print("w=" + str(mass*g))
    #print("a=" + str(a))
    #print("temp= "+ str(ds["t"].values[h]))
    #print("mu= "+ str(mu))
    #print("Re= "+str(Re))

    return(a)
  
def currentHeight(mass):
    vHold = 0
    yHold = 1
    deltaT = 0.04
    for t in range(100000):
       # stop if balloon crashes
        if(yHold < 0):
            print("crashed")
            #break
        a = acceleration(yHold, mass,vHold) 
        v = (a*deltaT) + vHold
        y =  (v*deltaT) + yHold
        
        vHold = v
        yHold = y
        aList.append(a)
        vList.append(v)
        hList.append(y)

    print(yHold)
    print(vHold)
    print(aList[len(aList)-1])
    maxList.append(yHold)

currentHeight(massBase)

# graph for generated data

fig, ax = plt.subplots()
#print(len(hList))
#ax.plot(bfo, c = "red")
ax.plot(vList, c="red")
ax.plot(hList, c="purple")
#ax.plot(aList, c="blue")
#ax.plot(volumeList, c="orange")
#ax.scatter(massList, maxList, c= "red")
#ax.plot(ar, c="green")
plt.show()
