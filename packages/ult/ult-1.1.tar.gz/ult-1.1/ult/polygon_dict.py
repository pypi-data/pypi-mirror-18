import pandas as pd 
import numpy as np 
import itertools
import time
import os
import simplejson as json
from pipegeohash import map_table,random_points_extrema,lint_values
from polygon_ind import make_ring_index
import geohash
import kyoto as kt
import deepdish as dd

def split_frame(data,minsize,maxsize):

	newlist = []
	bs = []
	cs = []
	generdata = gener(data)
	ind = 0
	count = 0
	while ind == 0:
		try:
			row = next(generdata)
			count += 1
			print '[%s/%s] Uniques' % (count,len(data))
			a,b,c = reduce_to_min(row,minsize=minsize)
			newlist.append(a)
			bs.append(b)
			cs.append(c)
		except StopIteration:
			ind = 1

	data = sum(newlist,[])
	return np.unique(data).tolist(),maxsize,minsize


# sringify the output of a line segment
def stringify(coords):
	newlist = []
	for long,lat in coords:
		newlist.append('[%s, %s]' % (long,lat))
	return '[' + ', '.join(newlist) + ']'

# given a dataframe and minimum size 
# returns the uniques within the dataframe
# that exist in between the minsizie and lowest
# level values
def reduce_to_min(data,**kwargs):
	maxsize = data['total'].str.len().max()
	minsize = data['total'].str.len().min()
	for key,value in kwargs.iteritems():
		if key == 'minsize':
			minsize = value
	current = maxsize - 1
	uniques = []
	count = 0
	while not current == minsize - 1:
		current = current - 1

		tempuniques = np.unique(data['total'].str[:current+1]).tolist()
		uniques = np.unique(uniques + tempuniques).tolist()	
	
	return uniques,maxsize,minsize


def merge_dicts(*dict_args):
    '''
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    '''
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

# makes a dictionary out of upper level uniques
# and lower level data
def make_dict(data,upperuniques,maxsize,minsize,filename):
	# making upper uniques into a datarame
	upperuniques = pd.DataFrame(upperuniques,columns=['total'])
	upperuniques['STRING'] = '"' + upperuniques['total'] + '":"na"'
	upperuniques = upperuniques['STRING'].values.tolist()
	print 'done upper uniques'

	# concatenating data
	print 'done concatenating data'


	data['STRING'] = '"' + data['total'] + '":"' + data['AREA'] + '"'

	minsize = '"min":%s' % minsize
	maxsize = '"max":%s' % maxsize

	data = upperuniques + data['STRING'].values.tolist()

	data = data + [minsize,maxsize]

	string = ', '.join(data)
	string = '{%s}' % string
	print 'string made'

	with open(filename,'wb') as f:
		f.write(string)


# makes a dictionary out of upper level uniques
# and lower level data
def make_dict_files(dfs,upperuniques,maxsize,minsize,filename):
	# making upper uniques into a datarame
	upperuniques = pd.DataFrame(upperuniques,columns=['total'])
	upperuniques['AREA'] = 'na'
	upperuniques = upperuniques.set_index('total')

	print 'done upper uniques'

	# concatenating data
	print 'done concatenating data'

	total =[upperuniques]
	generdata = gener(dfs)
	ind = 0
	count = 0
	while ind == 0:
		try:
			temp = next(generdata)
			temp = temp.set_index('total')
			count += 1
			print '[%s/%s] Combing Strings' % (count,len(dfs))
			total.append(temp)
			
		except StopIteration:
			ind = 1

	count = 0
	d = {'min':minsize,'max':maxsize}
	for row in total:
		count += 1
		d['df%s' % count] = row['AREA']

	dd.io.save(filename, d)


# makes and polygon index for 
# the total dataframe given
def make_polygon_index(data):
	# reducing the uniques and getting min and max size
	uniques,maxsize,minsize = reduce_to_min(data)

	return make_dict(data,uniques,maxsize,minsize)

# makes a polygon index from a list of csv files
def make_polygon_index_files(filenames,outfilename):
	newlist = []
	totalmin = 100
	totalmax = 0
	count = 0
	for row in filenames:
		temp = pd.read_csv(row)
		minsize = temp['total'].str.len().min()
		maxsize = temp['total'].str.len().max()
		if minsize < totalmin:
			totalmin = minsize
		if maxsize > totalmax:
			totalmax = maxsize
		newlist.append(temp)
		count += 1
		print '[%s/%s] Reading' % (count,len(filenames))
	uniques,totalmax,totalmin = split_frame(newlist,totalmin,totalmax)

	make_dict_files(newlist,uniques,totalmax,totalmin,outfilename)

# opens a file and parse lines
def openfile(filename):
	with open(filename,'rb') as f:
		return str.split(f.read(),'\n')

# combines csv files to a big csv much much faster
def combine_csvs(files,outfilename,**kwargs):
	min = False
	for key,value in kwargs.iteritems():
		if key == 'min':
			min = value


	count = 0
	totalcount = 0
	for filename in files:
		data = openfile(filename)

		if count == 0:
			count = 1
			total = data
		else:
			count+= 1
			total += data[1:]
		if count == 1000:
			count = 1
			totalcount += 1000
			print '[%s/%s]' % (totalcount,len(files))
	total = '\n'.join(total)

	with open(outfilename,'wb') as f:
		f.write(total)


# makes a test block and returns the points for the index
def make_test_block(ultindex,number):
	from mapkit import unique_groupby
	#indexdict = read_json('states_ind.json')
	extrema = {'n': 50.449779,'s': 20.565774,'e':-64.493017,'w':-130.578836}
	data = pg.random_points_extrema(number,extrema)
	data = ult.map_table(data,12,map_only=True)
	s = time.time()
	data = area_index(data,ultindex)
	print 'Time for just indexing: %s' % (time.time() - s)
	data = data[data['AREA'].str.len() > 0]
	data = unique_groupby(data,'AREA',hashfield=True,small=True)
	data['color'] = data['COLORKEY']
	return data

# maps one geohash to what it needs to be
def one_polygon_index(ghash):
	global minsize
	global maxsize
	global ultindex
	global areamask

	current = minsize
	while current < maxsize:
		output = ultindex.get(ghash[:current],'')
		# logic for continuing or not
		if output == 'na':
			current += 1
		elif output == '':
			return ''
		else:
			return areamask.get(output,'')

# maps one geohash to what it needs to be
def one_polygon_index_regions(ghash):
	global minsize
	global maxsize
	global ultindex
	global areamask
	global current 
	currentindex = ultindex.get(ghash[:2],{})
	if currentindex == {}:
		return ''
	current = minsize
	while current < maxsize:
		output = currentindex.get(ghash[:current],'')
		#print output,ghash,current,ghash[:current]
		# logic for continuing or not
		if output == 'na':
			current += 1
		elif output == '':
			return ''
		else:
			return areamask.get(output,'')

# maps a geohash to a given area index
# will again use global dict instead of function input
def area_index(data,index):
	global minsize
	global maxsize
	global ultindex
	global areamask
	ultindex = index['ultindex']
	areamask = index['areamask']
	minsize = index['metadata']['minsize']
	maxsize = index['metadata']['maxsize']
	output_type = index['metadata']['output_type']

	# mapping all geohashs to areas
	if output_type == 'single':
		data['AREA'] = data['GEOHASH'].map(one_polygon_index)
	elif output_type == 'regions':
		data['AREA'] = data['GEOHASH'].map(one_polygon_index_regions)
	return data


# kwargs for arguments that will all be completed 
# at teh same time
def ult_index(data,**kwargs):
	line_index = False
	latlongheaders = False
	seg_index = False
	for key,value in kwargs.iteritems():
		if key == 'line_index':
			line_index = value
		if key == 'latlongheaders':
			latlongheaders = value
		if key == 'seg_index':
			seg_index = value

	lats,lngs,data = lint_values(data,latlongheaders)

	if seg_index == False and not line_index == False:
		# execute line index code here
		#data[['GEOHASH','LINEID']] = gener_vals(lats,lngs,line_index,polygon_index)
		data['GEOHASH'],data['LINEID'] = gener_vals(lats,lngs,line_index,seg_index)
		return data
	elif not seg_index == False and not line_index == False:
		data['GEOHASH'],data['LINEID'],data['DISTANCE'],data['PERCENT'] = gener_vals(lats,lngs,line_index,seg_index)
		return data


# the second part of the actual geohashing process
# where the actual geohashing occurs
def gener_vals(lats,lngs,line_index,seg_index):
	distances = []
	lines = []
	ghashs = []
	percents = []
	ds = []
	if seg_index == False and not line_index == False:
		size = line_index['size']
		for i in range(0,len(lats)):
			oi = (lats[i],lngs[i],12)
	 		#newlist.append(oi)
	 		ghash = geohash.encode(*oi)
	 		lineid = line_index.get(ghash[:size],'')
	 		ghashs.append(ghash)
	 		lines.append(lineid)
	 		
	 		#ds.append([ghash,lineid])
	 	return ghashs,lines
	 	#return pd.DataFrame(ds,columns=['GEOHASH','LINEID'])
	elif not seg_index == False and not line_index == False:
		size = line_index['size']
		for i in range(0,len(lats)):
			oi = (lats[i],lngs[i],12)
	 		#newlist.append(oi)
	 		ghash = geohash.encode(*oi)
	 		lineid = line_index.get(ghash[:size],'')
	 		if not lineid == '':
	 			distance,percent = kt.get_distance(oi[0],oi[1],ghash[:size],lineid,seg_index[str(lineid)])
	 		if lineid == '' or percent > 100 or percent < 0:
	 			distance,percent = '',''

	 		ghashs.append(ghash)
	 		lines.append(lineid)
	 		distances.append(distance)
	 		percents.append(percent)
	 	return ghashs,lines,distances,percents


# makes a test block and returns the points for the index
def make_test_block(ultindex,number):
	from mapkit import unique_groupby
	#indexdict = read_json('states_ind.json')
	extrema = {'n': 80.449779,'s': 10.565774,'e':-60.493017,'w':-150.578836}
	data = random_points_extrema(number,extrema)
	data = map_table(data,12,map_only=True)
	s = time.time()
	data = area_index(data,ultindex)
	print 'Time for just indexing: %s' % (time.time() - s)
	data = data[data['AREA'].str.len() > 0]
	data = unique_groupby(data,'AREA',hashfield=True,small=True)
	data['color'] = data['COLORKEY']
	return data


def gener(list):
	for row in list:
		yield row

# trading memory overhead for one 
# dictionary method per found area
def construct_area_mask(uniqueareas):
	newdict = {}
	newdict2 = {}
	for i,area in itertools.izip(range(len(uniqueareas)),uniqueareas):
		hexi = str(hex(i))[2:]
		newdict[hexi] = area
		newdict2[area] = hexi
	return newdict,newdict2		  


#returns a list with geojson in the current directory
def get_filetype(src,filetype):
	filetypes=[]
	for dirpath, subdirs, files in os.walk(os.getcwd()+'/'+src):
	    for x in files:
	        if x.endswith('.'+str(filetype)):
	        	filetypes.append(src+'/'+x)
	return filetypes

# wrapper for spark functionality
def set_wrapper(arg):
	data,field,filename,folder = arg
	make_set(data,field,filename,folder=folder,csv=True)
	return []

# creates a bounds dataframe taht can be used to display
# boundries, input is the total boundry df
def stringify_bounds(data):
	newlist = []
	for name,group in data.groupby(['AREA','PART']):
		group = group.reset_index()
		coords = group[['LONG','LAT']].values.tolist()
		coords = stringify(coords)
		newlist.append([name[0],name[1],coords])
	newlist = pd.DataFrame(newlist,columns=['AREA','PART','coords'])
	return newlist

# creates metadata dictionary for polygon h5 outputs
# type is the output type
# min and max is the size of polygon steps
# size is the size of areamask
def make_meta_polygon(type,min,max,size):
	return {'type':'polygons','output_type':type,'minsize':min,'maxsize':max,'size':size}


def make_files(dflist):
	files = []
	with pd.HDFStore('progress.h5') as progress:
		for alist in dflist:
			print alist
			files.append(progress[str(alist)])			
	print 'read files'
	return files

# this function creates an hdf5 output that contains
# an ultindex dictionary the actual output
# assumes input will be progress h5 in the current directroy
# kwargs will control how the output is handle mutliple dict etc.
def make_h5_output(filename,**kwargs):
	output = 'single'
	for key,value in kwargs.iteritems():
		if key == 'output':
			output = value


	# reading in progress h5 file 
	with pd.HDFStore('progress.h5') as progress:
		completed = progress.keys()
		newcompleted = []

		# getting alignment df input into make_set
		alignment = progress['/initial']
		areamask,m2 = construct_area_mask(np.unique(alignment['AREA'].astype(str)).tolist())


		# getting all completed dfs
		for row in completed:
			if not row == '/initial' and not row == '/areamask':
				newcompleted.append(row)
		
		dflist = []
		for row in newcompleted:
			if output == 'single':
				dflist.append(progress[str(row)])
			else:
				dflist.append(str(row))
	
	# logic for a single output dictionary for either progress
	# or completion should be used with smaller indexs
	if output == 'single':
		# stringify bounds
		bounds = stringify_bounds(alignment)

		# concatenating all the dataframes
		dflist = pd.concat(dflist)

		# getting the min and maximum
		minsize = dflist['total'].str.len().min()
		maxsize = dflist['total'].str.len().max()


		# creating the drilled dataframe 
		uniques,b,c = reduce_to_min(dflist)
		total2 = pd.DataFrame(np.unique(uniques).tolist(),columns=['total'])
		total2['AREA'] = 'na'

		# setting up dictionaries (combing the finished dataframes)
		dflist = dflist.set_index('total')
		total2 = total2.set_index('total')
		dflist = dflist['AREA'].to_dict()
		total2 = total2['AREA'].to_dict()

		# making total dict
		totaldict = merge_dicts(*[total2,dflist])

		# making meta dictioanry
		metadict = make_meta_polygon(output,minsize,maxsize,len(areamask))
		
		d = {'ultindex':totaldict,
			'alignmentdf':bounds,
			'areamask':areamask,
			'metadata':metadict}

		dd.io.save(filename,d)



	if output == 'regions':
		# stringify bounds
		bounds = stringify_bounds(alignment)

		dflist = make_files(dflist)
		newdict = {}
		mins = []
		maxs = []
		for row in dflist:
			minsize = row['total'].str.len().min()
			maxsize = row['total'].str.len().max()
			mins.append(minsize)
			maxs.append(maxsize)
			row['G1'] = row['total'].str[:2]
			for name,group in row.groupby('G1'):
				try:
					newdict[name].append(group)
				except KeyError:
					newdict[name] = [group]

		size = len(newdict.keys())
		count = 0
		ultindex = {}
		minsize = min(mins)
		maxsize = max(maxs)
		for i in newdict.keys():
			count += 1
			df = pd.concat(newdict[i])
			df = df[['total','AREA']]
			uniques,b,c = reduce_to_min(df,minsize=minsize)
			df1 = pd.DataFrame(uniques,columns=['total'])
			df1['AREA'] = 'na'
			df = pd.concat([df1,df])
			df = df.set_index('total')
			df = df['AREA'].to_dict()
			# adding min and max to ultindex
			df['min'] = min(mins)
			df['max'] = max(maxs)

			ultindex[str(i)] = df

			#df.to_csv(str(i)+'.csv',index=False)
			print '[%s / %s]' % (count,size)
		


		# making meta dictioanry
		metadict = make_meta_polygon(output,minsize,maxsize,len(areamask))
		
		d = {'ultindex':ultindex,
			'alignmentdf':bounds,
			'areamask':areamask,
			'metadata':metadict}

		dd.io.save(filename,d)



def make_wrapper(args):
	data,areamask2,process = args
	totals = []
	count = 0
	totalcount = 0
	current = 0
	make_json({'status':False},'ind.json')
	size = len(np.unique(data['AREA']))
	for name,group in data.groupby('AREA'):
		# making ring index for each alignment
		s = time.time()
		total = make_ring_index(group)
		total['AREA'] = areamask2[str(name)]
		#total['AREA'] = areamask2[str(name)]


		minval = total['total'].str.len().min()
		maxval = total['total'].str.len().min()
		totals.append(total)
		totalcount += 1
		current += 1
		if current == 50 or totalcount >= size:
			current = 0
			totals = pd.concat(totals)
			ind = 0
			while ind == 0:
				time.sleep(1)
				if read_json('ind.json')['status'] == False:
					make_json({'status':True},'ind.json')
					with pd.HDFStore('progress.h5') as progress:
						progress[str(name)] = totals
					ind = 1
			make_json({'status':False},'ind.json')
			totals = []
		print '[%s/%s] for Process:%s in %s' % (totalcount,size,process,time.time() - s)		
	return []


# constructs a ult-index that can be used in 
# functions like area_index to quickly geofence polygons
def make_set(data,field,**kwargs):
	csv = False
	folder = False
	resume = False
	sc = False
	
	for key,value in kwargs.iteritems():
		if key == 'folder':
			folder = value


	# constructing areas mask
	areamask1,areamask2 = construct_area_mask(np.unique(data[field].astype(str)).tolist())
	sizeareas = len(np.unique(data[field])) + 2
	try:
		with pd.HDFStore('progress.h5') as progress:
			try:
				progress['initial'] = data
			except:
				progress = pd.HDFStore('progress.h5')
				progress['initial'] = data
				
			completed = progress.keys()
			startcount = len(completed)
			completed = [row[1:] for row in completed]
			data['BOOL'] = data[field].isin(completed)
			data = data[data['BOOL'] == False]
	except:
		print 'here'
		progress = pd.HDFStore('progress.h5')
		progress.close()
		startcount = 0

	for key,value in kwargs.iteritems():
		if key == 'sc':
			sc = value

	# logic for handling spark context
	if not sc == False:
		#splits = np.array_split(data['COMB'].values,8)
		areas = np.unique(data['AREA'])
		data = data.set_index('AREA')
		count = 0
		args = []
		for i in np.array_split(areas,8):
			split = data.loc[i].reset_index()
			args.append([split,areamask2,count])
			count += 1
		#data['COMB'].to_dict()
		

		instance = sc.parallelize(args)
		instance.map(make_wrapper).collect()
		return []

	mintotal = 100
	maxtotal = 0
	totals = []
	
	sizedisplay = len(np.unique(data[field]))
	# grouping each area on the big df
	# so that analysi and indexs for each polygon
	# can be made
	count = startcount
	totaltime = 0
	count2 = 0
	totals = []
	if not folder == False:
		files = get_filetype(folder,'csv')
		for row in files:
			s = time.time()
			total = pd.read_csv(row)
			name = str.split(row,'.')[0]
			name = str.split(name,'/')[1]
			print name
			try:
				total['AREA'] = total['AREA'].astype(int)
			except:
				pass
			if not len(total) == 0:
				totals.append(total)
				count2 += 1
				if count2 == 1000:
					totals = pd.concat(totals)
					count2 = 0
					with pd.HDFStore('progress.h5') as progress:
						progress[areamask2[str(name)]] = totals
					totals = []
				totaltime += time.time() - s
				count += 1
				avg = round(totaltime / float(count - startcount),2)
				print 'Areas Complete: [%s / %s], AVGTIME: %s s' % (count,sizeareas,avg)
	else:
		for name,group in data.groupby(field):
			# making ring index for each alignment
			s = time.time()
			total = make_ring_index(group)
			total['AREA'] = areamask2[str(name)]
			#total['AREA'] = areamask2[str(name)]

			# logic for writing csv out to file/folder
			if csv == True:
				csvfilename = prefix + str(name) + '.csv'
				total.to_csv(csvfilename,index=False)

			minval = total['total'].str.len().min()
			maxval = total['total'].str.len().min()

			if minval < mintotal:
				mintotal = minval
			if maxval > maxtotal:
				maxtotal = maxval
			totaltime += time.time() - s
			count += 1
			avg = round(totaltime / float(count - startcount),2)
			print 'Areas Complete: [%s / %s], AVGTIME: %s s' % (count,sizeareas,avg)
			
			with pd.HDFStore('progress.h5') as progress:
				progress[str(name)] = total


	return areamask1,mintotal,maxtotal


# makes a polygon index from a dataframe containing typical 
# polygon layout
# data - is the dataframe
# filename - is output h5 file that will be made
def make_polygon_index(data,filename,**kwargs):
	output = 'single'
	sc = False
	for key,value in kwargs.iteritems():
		if key == 'output':
			output = value
		if key == 'sc':
			sc = value
	make_set(data,'AREA',sc=sc)
	print 'Made progress h5 file now constructing ouput file.'
	make_h5_output(filename,output=output)
	print 'Made output h5 file containing datastructures:'
	print '\t- alignmentdf (type: pd.DataFrame)'
	print '\t- areamask (type: dict)'
	print '\t- ultindex (type: dict)'
	print '\t- metadata (type: dict)'

	os.remove('progress.h5')
	print 'Removed progress.h5 from directory'


# collecting geohashs
def collecthash(new,prefix,list):
	for key, value in new.items():
		if not isinstance(new[key],dict):
			list.append([str(prefix+key),str(value)])
		else:
			collecthash(new[key],prefix+key,list)

	return list

# creates a blocks dataframe from the ultindex
def make_blocks_polygons(index):
	# getting areamask
	areamask = index['areamask']
	
	# creating dataframe
	data = pd.DataFrame(index['ultindex'].items(),columns=['GEOHASH','AREA'])
	
	# filtering out upper hiearcharchy
	data = data[data.AREA != 'na']
	
	# applying area mask to get the areas
	data['AREA'] = data['AREA'].map(lambda x:areamask[x])
	return data


# creating the lines 
def make_blocks_lines(index):
	areamask = index['areamask']
	data = index['alignmentdf']
	return data

# creates a configuration for all types
def make_all_types_polygons(pointdata,index):
	from mapkit import make_config
	# getting the area,colorkey dict
	colordict = pointdata.set_index('AREA')['COLORKEY'].to_dict()

	# getting lines and blocks dataframes
	lines = make_blocks_lines(index)
	blocks = make_blocks_polygons(index)

	# filtering lines and blocks
	lines['BOOL'] = lines['AREA'].isin(colordict.keys())
	blocks['BOOL'] = blocks['AREA'].isin(colordict.keys())
	lines = lines[lines.BOOL == True]
	blocks = blocks[blocks.BOOL == True]

	# adding colorkey to lines and blocks
	lines['COLORKEY'] = lines['AREA'].map(lambda x:colordict[x])
	blocks['COLORKEY'] = blocks['AREA'].map(lambda x:colordict[x])

	a = make_config(pointdata,'points')
	a = make_config(lines,'lines',current=a)
	a = make_config(blocks,'blocks',current=a)
	return a

# given a point and line frame
def make_both(points,lines):
	from mapkit import make_config
	return make_config(points,'points',current=make_config(lines,'lines'))

# getting all geohashs 
# returns a dataframe of all areas and each geohashs associated with areas
def get_geohashs(b):
	totallist = []
	for row in b.keys():
		prefix = row
		if isinstance(b[row],dict):
			partlist = collecthash(b[row],prefix,[])
			totallist += partlist
	return pd.DataFrame(totallist,columns=['GEOHASH','AREA'])

# reads deepdish dd h5 file for ultindex outputs
def read_h5(filename):
	return dd.io.load(filename)

def make_json(dictionary,filename):
	with open(filename,'wb') as f:
		json.dump(dictionary,f)
	print 'Wrote Json.'

def read_json(filename):
	with open(filename,'rb') as f:
		return json.load(f)