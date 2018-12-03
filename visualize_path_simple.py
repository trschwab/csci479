import numpy as np
import matplotlib.pyplot as plt
import csv
import matplotlib.patches as patches
import sys


def visualize(file_name, plot_type, index):
	print("plot_type", plot_type)
	print("index", index)
	index = int(index)
	arena_size = (800,800)


	#fig2 = plt.figure(figsize=(7,7))

	fig2 = plt.figure()
	ax2 = fig2.add_subplot(111, aspect='equal')


	#plt.axis((ax2[0],ax2[1],ax2[3],ax2[2]))

	#ax2.set_facecolor('xkcd:salmon')

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

	#Get data
	opened_file = open(file_name)


	df_x = []
	df_y = []

	if(plot_type=="latest"):
		row_counter = -1		#initialize counter at -1 so row counter equals the number of indexs not len()
		list_of_rows = []
		with open(file_name, newline='') as csvfile:
			loc_reader = csv.reader(csvfile)
			for row in loc_reader:
				if row != []:
					row_counter += 1
					list_of_rows += [row]

			#print("num rows = ", row_counter)
			#print(list_of_rows[row_counter])

			locs = list_of_rows[-1]
			spots = eval(locs[-1])
			#print(spots)	#this is the key of the last list at the moment

			for loc in spots:				#spots is a list of tuples, each tuple is (x,y) coridnate of bee

				df_x.append(float(loc[0]))	#df_x is list of x cordinates
				df_y.append(float(loc[1]))	#df_y is list of y cordinates

			t = np.linspace(0,len(df_x),len(df_x))
			plt.scatter(df_x, df_y, c=t,cmap=plt.get_cmap("cool"), alpha=0.8)
			title_str = "Trial ID: " + str(locs[0])
			plt.title(title_str)
			plt.plot(df_x, df_y)
			plt.colorbar()
			plt.show()

	if(plot_type=="index"):

		with open(file_name, newline='') as csvfile:
			loc_reader = csv.reader(csvfile)
			for row in loc_reader:
				if row != []:

					if row[0] == str(index):
						#print("got to index")

						locs = list(row[1:])
						spots = eval(locs[0])

		for loc in spots:				#spots is a list of tuples, each tuple is (x,y) coridnate of bee

			df_x.append(float(loc[0]))	#df_x is list of x cordinates
			df_y.append(float(loc[1]))	#df_y is list of y cordinates

			t = np.linspace(0,len(df_x),len(df_x))
			plt.scatter(df_x, df_y, c=t,cmap=plt.get_cmap("cool"), alpha=0.8)
		title_str = "Trial ID: " + str(index)
		plt.title(title_str)
		plt.plot(df_x, df_y)
		plt.colorbar()
		plt.show()



	#plt.figure(figsize=(10,10))
	if(plot_type=="all"):

		with open(file_name, newline='') as csvfile:
			loc_reader = csv.reader(csvfile)
			plot_num = 321
			for row in loc_reader:
				df_x = []
				df_y = []
				if row != []:

					locs = list(row[1:])
					spots = eval(locs[0])

					for index in spots:				#spots is a list of tuples, each tuple is (x,y) coridnate of bee
						#print("index", index)
						df_x.append(float(index[0]))	#df_x is list of x cordinates
						df_y.append(float(index[1]))	#df_y is list of y cordinates

					t = np.linspace(0,len(df_x),len(df_x))


					#print(plot_num)
					plt.subplot(plot_num)
					title_str = "Trial ID: " + str(row[0])
					plt.title(title_str)
					plot_num += 1
					plt.scatter(df_x, df_y, c=t,cmap="cool", alpha=0.8)
					plt.plot(df_x, df_y)

					if plot_num == 326:
						plot_num = 421
					elif plot_num == 427:
						print("Too many graphs to display")
						break

			#plt.colorbar()
			plt.show()




def saveVisualization(file_name, plot_type, index):
	index = int(index)
	arena_size = (800,800)


	#fig2 = plt.figure(figsize=(7,7))

	fig2 = plt.figure()
	ax2 = fig2.add_subplot(111, aspect='equal')


	#plt.axis((ax2[0],ax2[1],ax2[3],ax2[2]))

	#ax2.set_facecolor('xkcd:salmon')

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

	#Get data
	opened_file = open(file_name)


	df_x = []
	df_y = []

	if(plot_type=="latest"):
		row_counter = -1		#initialize counter at -1 so row counter equals the number of indexs not len()
		list_of_rows = []
		with open(file_name, newline='') as csvfile:
			loc_reader = csv.reader(csvfile)
			for row in loc_reader:
				if row != []:
					row_counter += 1
					list_of_rows += [row]

			#print("num rows = ", row_counter)
			#print(list_of_rows[row_counter])

			locs = list_of_rows[-1]
			spots = eval(locs[-1])
			#print(spots)	#this is the key of the last list at the moment

			for loc in spots:				#spots is a list of tuples, each tuple is (x,y) coridnate of bee

				df_x.append(float(loc[0]))	#df_x is list of x cordinates
				df_y.append(float(loc[1]))	#df_y is list of y cordinates

			t = np.linspace(0,len(df_x),len(df_x))
			plt.scatter(df_x, df_y, c=t,cmap=plt.get_cmap("cool"), alpha=0.8)
			title_str = "Trial ID: " + str(locs[0])
			plt.title(title_str)
			plt.plot(df_x, df_y)
			plt.colorbar()
			new_file_name = "Trial" + str(locs[0]) + ".png"
			plt.savefig(new_file_name)

	if(plot_type=="index"):

		with open(file_name, newline='') as csvfile:
			loc_reader = csv.reader(csvfile)
			for row in loc_reader:
				if row != []:

					if row[0] == str(index):
						#print("got to index")

						locs = list(row[1:])
						spots = eval(locs[0])

		for loc in spots:				#spots is a list of tuples, each tuple is (x,y) coridnate of bee

			df_x.append(float(loc[0]))	#df_x is list of x cordinates
			df_y.append(float(loc[1]))	#df_y is list of y cordinates

			t = np.linspace(0,len(df_x),len(df_x))
			plt.scatter(df_x, df_y, c=t,cmap=plt.get_cmap("cool"), alpha=0.8)
		title_str = "Trial ID: " + str(index)
		plt.title(title_str)
		plt.plot(df_x, df_y)
		new_file_name = "Trial" + str(index) + ".png"
		plt.savefig(new_file_name)



	#plt.figure(figsize=(10,10))
	if(plot_type=="all"):

		with open(file_name, newline='') as csvfile:
			loc_reader = csv.reader(csvfile)
			plot_num = 321
			for row in loc_reader:
				df_x = []
				df_y = []
				if row != []:

					locs = list(row[1:])
					spots = eval(locs[0])

					for index in spots:				#spots is a list of tuples, each tuple is (x,y) coridnate of bee
						#print("index", index)
						df_x.append(float(index[0]))	#df_x is list of x cordinates
						df_y.append(float(index[1]))	#df_y is list of y cordinates

					t = np.linspace(0,len(df_x),len(df_x))


					#print(plot_num)
					plt.subplot(plot_num)
					title_str = "Trial ID: " + str(row[0])
					plt.title(title_str)
					plot_num += 1
					plt.scatter(df_x, df_y, c=t,cmap="cool", alpha=0.8)
					plt.plot(df_x, df_y)

					if plot_num == 326:
						plot_num = 421
					elif plot_num == 427:
						print("Too many graphs to display")
						break

			new_file_name =  "allVisuals.png"
			plt.savefig(new_file_name)
