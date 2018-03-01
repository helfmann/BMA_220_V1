import serial
import numpy as np
from matplotlib import pyplot as plt
import datetime
import os
import time
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA


ser = serial.Serial("Com7", 230400)

directory = r'D:\Priyesh\Arduino\Accelerometer\\' + str(datetime.date.today()) + '\\'

if not os.path.exists(directory):
    os.makedirs(directory)

filen = str(datetime.date.today()) + str(time.time())

filename = open(directory + filen+ '.txt', 'a+')

file2 = open(directory + 'filename.txt', 'w')

file2.write(directory+filen)
 
#filename = directory + filen + '.txt'

finish = 20
plt.ion() # set plot to animated
 
acclX = []
acclY = []
t = []
data = np.array([])
cnt = 0
initial = time.time()
  
# start data collection
while True: 
    data = ser.readline().rstrip().split('\t') # read data from serial
                                   # port and strip line endings4
    
    current = time.time()-initial
    #data = data.split('\t')
    try:
        data = np.append(data, current).astype(np.float)
        if len(data) ==4:
            np.savetxt(filename, [data], delimiter = ',')
    except:
        pass
    #t = [data[0], data[1], current]
    cnt +=1
    #filename.write(str(data))
    
    #np.savetxt(filename, data)
    
    if (time.time()-initial) >= finish:
        print (cnt)
        break
    #data = data.split('\t')
    #if len(data) == 2:
    #    ymin = float(min(ydata1))-100
    #    ymax = float(max(ydata1))+100
    #    ax1.set_ylim([ymin,ymax])
    #    ydata1.append(data[0])
    #    del ydata1[0]
    #    line.set_xdata(np.arange(len(ydata1)))
    #    line.set_ydata(ydata1)  # update the data
    #    
    #    
    #    ymin = float(min(ydata2))-100
    #    ymax = float(max(ydata2))+100
    #    plt2.set_ylim([ymin,ymax])
    #    ydata2.append(data[1])
    #    del ydata2[0]
    #    line2.set_xdata(np.arange(len(ydata2)))
    #    line2.set_ydata(ydata2)  # update the data
    #    plt.draw() # update the plot
    #    plt.pause(1e-6)


#file2 = np.loadtxt(filename)
filename.close()

file2.close()

data = np.loadtxt(directory + filen + '.txt', delimiter = ',')

host = host_subplot(111, axes_class=AA.Axes)
plt.subplots_adjust(right=0.75)

ax2= host.twinx()
ax3 = host.twinx()
offset = 60
new_fixed_axis = ax3.get_grid_helper().new_fixed_axis
ax3.axis["right"] = new_fixed_axis(loc="right",
                                        axes=ax3,
                                        offset=(offset, 0))

ax3.axis["right"].toggle(all=True)

host.plot(data[:,-1], data[:,0], 'k', label = 'X-Axis')
ax2.plot(data[:,-1], data[:,1], 'r', label = 'Y-Axis')
ax3.plot(data[:,-1], data[:,2], 'g', label = 'Z-Axis')
host.legend()

#plt.draw()

plt.show()

