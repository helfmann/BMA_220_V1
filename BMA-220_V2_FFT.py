import numpy as np
import pandas as pd
import datetime
from scipy import interpolate
from scipy import signal
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.ticker as mtick
from mpl_toolkits.axes_grid.inset_locator import inset_axes
import matplotlib

#directory = r'D:\Priyesh\Arduino\Accelerometer\\' + str(datetime.date.today()) + '\\'
#directory = r'D:\Priyesh\Arduino\Accelerometer\2017-05-07\\'
#D:\Priyesh\Arduino\Accelerometer\\2017-04-21\2017-04-211492824233.38
directory = r'C:\Users\Priyesh\OneDrive - ualberta.ca\Thesis\Chapter 1\Result\Accelerometer\2017-05-07\\'

font = { 'family': 'Times New Roman',
         'weight': 'bold',
         'size': 16}
matplotlib.rc('font', **font)


matplotlib.rcParams['text.latex.unicode'] = True
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'

file2 = open(directory + 'filename.txt', 'r')

filename = file2.read().splitlines()


def interpolation(time, read):
    func = interpolate.interp1d(time, read, kind = 'nearest')
    uni_time = np.linspace(time[0], time[-1], len(time))

    func_data = func(uni_time)

    fourier = np.fft.fft(func_data)/len(func_data)

    steps = (uni_time[-1]-uni_time[0])/len(uni_time)
    n = uni_time.size
    func_fr = np.fft.fftfreq(n, d = steps)
    ind = np.arange(1, n/2)
    psd = abs(fourier[ind]**2 ) + abs(fourier[-ind]**2)
    #fr = np.linspace(0, 1./(uni_time[1]*2), len(fourier))
    #print len(fr), uni_time[1]

    return (func_fr[ind], psd)

    #fr = np.fft.fftfreq(time[-1], steps)

def subplot(ax, rect):
    fig = plt.gcf()
    box = ax.get_position()
    width = box.width
    height = box.height
    inax_position  = ax.transAxes.transform(rect[0:2])
    transFigure = fig.transFigure.inverted()
    infig_position = transFigure.transform(inax_position)
    x = infig_position[0]
    y = infig_position[1]
    width *= rect[2]
    height *= rect[3]  # <= Typo was here
    subax = fig.add_axes([x,y,width,height])
    x_labelsize = subax.get_xticklabels()[0].get_size()
    y_labelsize = subax.get_yticklabels()[0].get_size()
    print y_labelsize
    x_labelsize *= rect[2]**0.5
    y_labelsize *= rect[3]**0.5
    subax.xaxis.set_tick_params(labelsize=x_labelsize)
    subax.yaxis.set_tick_params(labelsize=y_labelsize)
    return subax

def plotting(data, pos, freq_idx, row):
    freq, amp = interpolation(data[:,-1], data[:,0])
    freq2, amp2 = interpolation(data[:,-1], data[:,1])
    freq3, amp3 = interpolation(data[:,-1], data[:,2])
    rect =[0.25,0.6,0.3,0.3]
    idx = np.where(freq3>=freq_idx)
    fig4 = plt.figure(1)
    #plt.rc('font', weight='bold')
    ax = fig4.add_subplot(row, 1, pos)
    ax.plot(freq[4:idx[0][0]], amp[4:idx[0][0]], 'C0')
    #ax.plot(freq2[4:idx[0][0]], amp2[4:idx[0][0]], 'C1')

    #ax.plot(freq3[4:idx[0][0]], amp3[4:idx[0][0]], 'C2')
    #subax = subplot(ax, rect)
    #ax.xaxis.set_tick_params(labelsize=14)
    #ax.yaxis.set_tick_params(labelsize=14)
    #print subax

    #subax.plot(freq[4:], amp[4:])
    #ax2 = fig4.add_subplot(row,3, pos+1, sharey = ax)
    #
    #ax2.plot(freq2[4:idx[0][0]], amp2[4:idx[0][0]])
    #
    #plt.setp(ax2.get_yticklabels(), visible=False)
    #
    #subax2 = subplot(ax2, rect)
    #
    #subax2.plot(freq2[4:], amp2[4:])
    #
    #ax3 = fig4.add_subplot(row, 3, pos+2, sharey = ax)
    #
    #ax3.plot(freq3[4:idx[0][0]], amp3[4:idx[0][0]])
    #
    #plt.setp(ax3.get_yticklabels(), visible=False)
    #
    #subax3 = subplot(ax3, rect)
    #
    #subax3.plot(freq3[4:], amp3[4:])
    #
    #plt.subplots_adjust(wspace = 0)
    #if row ==4:
    fig4.text(0.04, 0.53, '$ASD,\ g^2/Hz$', ha = 'center', va = 'center', rotation = 'vertical')
    fig4.text(0.53, 0.04, '$Frequency,\ Hz$', ha = 'center', va = 'center')
    fig4.text(0.53, 0.84, 'Bridge', ha = 'center', va = 'center')


#data = np.loadtxt(filename + '.txt', delimiter = ',')
find_idx = [20, 5, 15, 100]
cnt = 1
for name in filename:
    #data = np.loadtxt(name+ '.txt', delimiter = ',')
    data = np.loadtxt(name, delimiter = ',')
    plotting(data, cnt, find_idx[(cnt-1)/3], len(filename))
    cnt +=3

plt.subplots_adjust(left = 0.15, bottom = 0.15)
plt.show()
#plt.savefig(directory + 'Bridge_1.tiff', dpi = 600, transparent=True)
#d = np.concatenate(d)
#data[:,-1] = data[:,-1]-data[0,-1]
#host = host_subplot(111, axes_class=AA.Axes)
#plt.subplots_adjust(right=0.75)
#
#ax2= host.twinx()
#ax3 = host.twinx()
#offset = 60
#new_fixed_axis = ax3.get_grid_helper().new_fixed_axis
#ax3.axis["right"] = new_fixed_axis(loc="right",
#                                        axes=ax3,
#                                        offset=(offset, 0))
#
#ax3.axis["right"].toggle(all=True)
#factor = 3.94/63
#cnt = 10
#
#data[:, 0] = data[:, 0]*factor*1000
#data[:, 1] = data[:, 1]*factor*1000
#data[:, 2] = data[:, 2]*factor*1000
#
#data[:, 0] = data[:, 0]-np.mean(data[:, 0])
#data[:, 1] = data[:, 1]-np.mean(data[:, 1])
#data[:, 2] = data[:, 2]-np.mean(data[:, 2])
#
#
#host.plot(data[cnt:,-1], data[cnt:,0], 'k', label = 'X-Axis')
#ax2.plot(data[cnt:,-1], data[cnt:,1], 'r', label = 'Y-Axis')
#ax3.plot(data[cnt:,-1], data[cnt:,2], 'g', label = 'Z-Axis')
#host.legend()
#
#plt.draw()
##plt.plot(data[:,2], data[:,1])
#
#freq, amp = interpolation(data[:,-1], data[:,0])
#freq2, amp2 = interpolation(data[:,-1], data[:,1])
#freq3, amp3 = interpolation(data[:,-1], data[:,2])
#
#fig2 = plt.figure(2)
#
##plt.loglog(freq, amp, label = 'X-Axis')
##plt.loglog(freq2, amp2, label = 'Y-Axis')
##plt.loglog(freq3, amp3, label = 'Z-Axis')
#
#plt.plot(freq, amp, label = 'X-Axis')
#plt.plot(freq2, amp2, label = 'Y-Axis')
#plt.plot(freq3, amp3, label = 'Z-Axis')
#plt.legend()
#
#fig3 = plt.figure(3)
#
##np.append(data[:,4], np.sqrt(data[:, 0]**2 + data[:, 1]**2 + data[:, 2]**2))
##data[:, 0] = data[:, 0]-min(data[:, 0])
##data[:, 1] = data[:, 0]-min(data[:, 1])
##data[:, 2] = data[:, 0]-min(data[:, 2])
#
##data[:, 0] = data[:, 0]-np.median(data[:, 0])
##data[:, 1] = data[:, 0]-np.median(data[:, 1])
##data[:, 2] = data[:, 0]-np.median(data[:, 2])
#
#d_bar = np.sqrt(data[:, 0]**2 + data[:, 1]**2 + data[:, 2]**2)
#
#freq4, amp4 = interpolation(data[:, -1], d_bar)
#
#plt.rc('font', family='Times New Roman', serif='cm10', weight = 'bold', size = 14)
##plt.plot(data[:, 3], data[:, 1])
##plt.loglog(freq4[5:], amp4[5:])
#idx = np.where(freq4>=50)
#plt.plot(freq4[5:idx[0][0]], amp4[5:idx[0][0]])
##plt.loglog(freq4[5:], amp4[5:])
#
##plt.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]
#
##plt.rcParams['text.latex.preamble'] = [r'\boldmath']
#
#plt.xlabel('Frequency, Hz', fontsize = 14, weight= 'bold')
##plt.xaxis.set_tick_params(fontweight = 'bold')
#
##plt.rc('text', usetex=True)
#
#plt.ylabel(r'ASD, mg$^2$/Hz', fontsize = 14, fontweight= 'bold')
##plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
#a = plt.axes([0.55, 0.65, 0.3, 0.2])
##
#plt.rc('font', family='Times New Roman', serif='cm10', weight = 'bold', size = 10)
#plt.plot(freq4[5:], amp4[5:])
#plt.yticks(np.arange(0, 300, 100), size = 10)
#plt.xticks(np.arange(0, 201, 100), size = 10)
#plt.xlabel('Frequency, Hz', fontsize = 10, fontweight = 'bold')
#plt.ylabel(r'ASD, mg$^2$/Hz', fontsize = 10, fontweight= 'bold')
##plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
#plt.tight_layout()
#
#idx = np.where(freq>=15)
#fig4 = plt.figure(4, figsize = (10, 10))
#
#ax = fig4.add_subplot(3, 3, 1)
#
#ax.plot(freq[:idx[0][0]], amp[:idx[0][0]])
#
#inset_ax = inset_axes(ax, width= "50%", height = 0.5)
#
#inset_ax.plot(freq, amp)
#
#ax2 = fig4.add_subplot(3, 3, 2, sharey = ax)
#
#ax2.plot(freq2[:idx[0][0]], amp2[:idx[0][0]])
#
#plt.setp(ax2.get_yticklabels(), visible=False)
#
#inset_ax2 = inset_axes(ax2, width= "50%", height = 0.5, loc = 1)
#
#inset_ax2.plot(freq2, amp2)
#
#ax3 = fig4.add_subplot(3, 3, 3, sharey = ax)
#
#ax3.plot(freq3[:idx[0][0]], amp3[:idx[0][0]])
#
#plt.setp(ax3.get_yticklabels(), visible=False)
#
#inset_ax3 = inset_axes(ax3, width= "50%", height = 0.5, loc = 1)
#
#inset_ax3.plot(freq3, amp3)
#
#plt.subplots_adjust(wspace = 0, hspace = 0)
##plt.savefig(directory + 'Walk.tiff', dpi = 600, transparent = True)
#plt.show()
