import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
#import numpy as np
#import matplotlib.pyplot as plt
import csv
import matplotlib.patches as patches
import sys

# main
file_name = "locations.csv"
plot_type = "latest"
index = 1
# if(len(sys.argv) < 2):
# 	print("Please specify file name")
# 	exit()
# elif(len(sys.argv) < 3):
# 	file_name= sys.argv[1] 
# 	plot_type= "latest"
# else:
# 	file_name= sys.argv[1] 
# 	plot_type= sys.argv[2] 
# 	if(len(sys.argv) < 4):
# 		print("Please specify index of path to plot")
# 		exit()
# 	else:
# 		index = int(sys.argv[3]) 


	
 

#fig2 = plt.figure(figsize=(7,7))
# fig2 = plt.figure()
# ax2 = fig2.add_subplot(111, aspect='equal')

f = open(file_name)
arena_size = (800,800)

df_x = []
df_y = []

if(plot_type=="latest"):
	last_row = list(csv.reader(f))[-1]
	for ind in range(1,len(last_row)):
	    data = last_row[ind][1:-1].split(",")
	    df_x.append(float(data[0]))
	    df_y.append(float(data[1]))
	

if(plot_type=="index"):
	last_row = list(csv.reader(f))[index]
	for ind in range(1,len(last_row)):
	    data = last_row[ind][1:-1].split(",")
	    df_x.append(float(data[0]))
	    df_y.append(float(data[1]))
	

if(plot_type=="all"):
	last_row = list(csv.reader(f))[index]
	for ind in range(1,len(last_row)):
	    data = last_row[ind][1:-1].split(",")
	    df_x.append(float(data[0]))
	    df_y.append(float(data[1]))

# #draw rectable of view
# ax2.add_patch(
#      patches.Rectangle(
#         (0, 0),
#         arena_size[0],
#         arena_size[0],
#         fill=False     
#      ) ) 

# plt.xlim(-10, arena_size[0]+10)  
# plt.ylim(-10, arena_size[0]+10) 
# #plt.figure(figsize=(10,10))

# t=np.linspace(0,len(df_x),len(df_x))
# plt.scatter(df_x, df_y, c=t,cmap=plt.get_cmap("viridis"))
# plt.plot(df_x, df_y)
# plt.colorbar()
# plt.show()



fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)
#t = np.arange(0.0, 1.0, 0.001)
#a0 = 5
#f0 = 3
#delta_f = 5.0
#s = a0*np.sin(2*np.pi*f0*t)
#l, = plt.plot(t, s, lw=2, color='red')
t=np.linspace(0,len(df_x),len(df_x))
l, = ax.plot(df_x,df_y,label='toto',ms=10,marker='o',ls='',c=t,cmap=plt.get_cmap("viridis"))
#l = plt.scatter(1, 1)
#plt.axis([0, 1, -10, 10])

axcolor = 'lightgoldenrodyellow'
#axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
axamp = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)

#sfreq = Slider(axfreq, 'Freq', 0.1, 30.0, valinit=f0, valstep=delta_f)
time_trail = len(df_x)
samp = Slider(axamp, 'Amp', 0.0, time_trail, valinit=0)


def update(index):

    #amp = samp.val
    #freq = sfreq.val
    #l.set_xdata(val)
    l.set_data(df_x[int(index)],df_y[int(index)])
    #l.set_ydata(val)
    fig.canvas.draw_idle()

#sfreq.on_changed(update)
samp.on_changed(update)


#def colorfunc(label):
#    l.set_color(label)
#    fig.canvas.draw_idle()
#radio.on_clicked(colorfunc)

plt.show()
