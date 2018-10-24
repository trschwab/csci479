import numpy as np
import matplotlib.pyplot as plt
import csv
import matplotlib.patches as patches
import sys

# main
if(len(sys.argv) < 2):
	print("Please specify file name")
	exit()
elif(len(sys.argv) < 3):
	file_name= sys.argv[1] 
	plot_type= "latest"
else:
	file_name= sys.argv[1] 
	plot_type= sys.argv[2] 
	if(len(sys.argv) < 4):
		print("Please specify index of path to plot")
		exit()
	else:
		index = int(sys.argv[3]) 


	


#fig2 = plt.figure(figsize=(7,7))
fig2 = plt.figure(g)
ax2 = fig2.add_subplot(111, aspect='equal')

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

#draw rectable of view
ax2.add_patch(
     patches.Rectangle(
        (0, 0),
        arena_size[0],
        arena_size[0],
        fill=False     
     ) ) 

plt.xlim(-10, arena_size[0]+10)  
plt.ylim(-10, arena_size[0]+10) 
#plt.figure(figsize=(10,10))

t=np.linspace(0,len(df_x),len(df_x))
plt.scatter(df_x, df_y, c=t,cmap=plt.get_cmap("viridis"))
plt.plot(df_x, df_y)
plt.colorbar()
plt.show()