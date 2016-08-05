from numpy import genfromtxt
import numpy as np
import sys
from math import atan2, degrees, pi
import os
import glob

##plt.ion()

#'ThunderSTORM results_647_84A_primary_secondary.csv'
#'ThunderSTORM results_647_91E_nanobodies.csv'

FolderName = sys.argv[1]
CfgFile = 'Cfg.tmp' 

os.chdir(FolderName)

f = open(CfgFile, 'r')
FileName = f.readline()
f.close()

os.remove(CfgFile)
print(FileName)

my_data = np.loadtxt(FileName, delimiter=',', skiprows = 1, usecols = (1,2,7))


#plt.plot(my_data[:,0],my_data[:,1],'b+')

if (my_data.shape[0] == 3):
    my_data = np.transpose(my_data)

DataBase = my_data

del my_data

#Dmax = 200

if 1:
    DistData = np.zeros([DataBase.shape[0],5])+np.nan 
    print "\n//////////////////////////\nAnalysis in Progress\n"
    print "\n///////////"
    for kat in np.arange(len(DataBase)):#range(10):#
        Temp = np.copy(DataBase)
        TempI = DataBase[kat,:]
        Temp[kat,:] = np.zeros(DataBase.shape[1])+np.nan
        Temp = Temp[~np.isnan(Temp[:,1])]
        Dist = Temp - TempI
        Dist = (Dist[:,1]**2 + Dist[:,0]**2)**0.5
        MinDistPos = Dist.argmin()
        ##MinDist = Dist.min()
        if 1:
            DistData[kat,:] = [TempI[0],TempI[1],Temp[MinDistPos,0],Temp[MinDistPos,1],Dist.min()]
            
        del Dist
        if np.mod(kat,len(DataBase)*10/100) == 0:
            sys.stdout.write('.')
            sys.stdout.flush()
            
    dx = DistData[:,2]-DataBase[:,0]
    dy = DistData[:,3]-DataBase[:,1]
    Angs = np.arctan2(-dy,dx)* 180 / np.pi
    
    DistData = DistData[~np.isnan(DistData[:,1])]
    Angs = Angs[~np.isnan(Angs)]
 
#np.append(DistData,Angs)
SaveName = FileName + '_0_DistData.dat'
NoDupCnt = 0
while os.path.isfile(SaveName):
    NoDupCnt += 1
    SaveName = FileName + '_' + str(NoDupCnt) + '_DistData.dat'


print '\n FilenName = ' + SaveName
SaveData = np.zeros([DistData.shape[0],6])
SaveData[:,0:5] = DistData
SaveData[:,5] = Angs
f = open(SaveName,'w')
f.write(" %s , %s ,%s , %s , %s, %s  \n" % (" X1 [nm]", "Y1 [nm]" ," X2 [nm]", "Y2 [nm]" , "Dist [nm]", "Ang [rad]"))
for item in SaveData:f.write(" %s , %s, %s , %s , %s , %s \n" % (str(item[0]),str(item[1]),str(item[2]),str(item[3]),str(item[4]),str(item[5])))
f.close()
print "\n"
print "All done!"


