#Analyzing Stock Price Data:

import concurrent.futures
import os
import numpy as np
import threading
import time
from datetime import datetime
import matplotlib.pyplot as plt
import pylab
#needed otherwise the figures do not print out right
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

#Function to read in the files into a multi-dimensional array and return a tuple (key,data)
#Note when using threading better to have locks, if using multiprocessing it is not as necessary.
def format_file1(filename):
    #lock.acquire()
    with open(filename, 'r') as f:
		#strip removes all white space as well as \t,\n etc. from begging and end of file content
        data = f.read().strip()
    key = filename.rstrip(".csv").strip("prices/")
    #key = filename.replace(".csv", "").replace("prices/", "")
    data = data.split("\n")
    data = [d.split(",") for d in data]
    time.sleep(0.1)
    #lock.release()
    return (key, data)
	
def getKey(item):
	return item[1]
	
#Function aggregates of columns over all stocks (assumption is that time period is same for all stocks)
def compute_aggregates(stockdata):
	stockdata2 = {}
	for key,data in stockdata.items():
		colnames = data[0]
		#initialize a new dictionary to each stock in stockdata2
		stockdata2[key]={}
		#initialize each key, col pair to point to a list
		for col in colnames:
			stockdata2[key][col]=[]
		#now read the data into the lists
		for row in data[1:]:
			for i, item in enumerate(row):
				#note that we can the colnames based on above
				if colnames[i] == "date":
					#stockdata2[key][colnames[i]].append(datetime.strptime(item,"%Y-%m-%d"))
					stockdata2[key][colnames[i]].append(item)
				elif colnames[i]=="volume":
					stockdata2[key][colnames[i]].append(int(item))
				else:
					#turn the value into a number
					stockdata2[key][colnames[i]].append(float(item))

	#make sure all variables are stored correctly
	print("Item 1 of aapl stock, date list: ", stockdata2["aapl"]["date"][0])
	print("Item 1 of aapl stock, close list: ", stockdata2["aapl"]["close"][0])
	print("Item 1 of aapl stock, volume list: ", stockdata2["aapl"]["volume"][0])
	
	#Compute average of all stocks over the time period
	vars = ["open","close","high","low","volume"]
	meanvar = {}
	for key,data in stockdata2.items():
		for v in vars:
			if v not in meanvar:
				meanvar[v]=[]
			meanvar[v].append(np.mean(np.array(stockdata2[key][v])))
	npmeanvar={}
	for v, val in meanvar.items():
		if not v in npmeanvar:
			npmeanvar[v] = {}
		npmeanvar[v] = np.array(meanvar[v])
		print("Average {} of all stocks: {}".format(v,round(np.mean(npmeanvar[v]),2)))
		#print(npmeanvar[v])
	
	diff_close_open = np.mean(npmeanvar["close"])-np.mean(npmeanvar["open"])
	diff_high_low = np.mean(npmeanvar["high"])-np.mean(npmeanvar["low"])
	print("Average difference between close and open of all stocks: {}".format(round(diff_close_open,2)))
	print("Average difference between high and low of all stocks: {}".format(round(diff_high_low,2)))	
	return(stockdata2)
	
#This function computes the most traded stock each day
def most_traded(stockdata2):
	#place stockdata2 into a new data structure where we have date pointing to array of [volume,stock] pairs.
	stockdata3 = {}
	for key,data in stockdata2.items():
		for i, dt in enumerate(stockdata2[key]["date"]):
			if dt not in stockdata3:
				stockdata3[dt]=[]
			#append the tuple of stock,volume pairs to each date variable
			stockdata3[dt].append([key,stockdata2[key]["volume"][i]])
	#sort in descending order the stockdata3[dt] on volume

	stockdata3[dt] = sorted(stockdata3[dt],key=getKey, reverse=True)
	#print(stockdata3[dt])
	print("Most traded stock on {}: ({})".format(dt,stockdata3[dt][0]))
	return stockdata3
	
def find_high_volume_days(stockdata2,stockdata):
	listvolume = {}
	totvolume = []
	#this stores the date, key, row combination (makes it easier for look up in stockdata2 data)
	daterow = {}
	for key,data in stockdata2.items():
		daterow[key]={}
		for i, dt in enumerate(stockdata2[key]["date"]):
			if dt not in listvolume:
				listvolume[dt]=[]
			listvolume[dt].append(stockdata2[key]["volume"][i])
			daterow[key][dt]=i

	for dt in listvolume:
		totvolume.append([dt,sum(listvolume[dt])])
	#now sort total volume list which is tuples
	totvolume = sorted(totvolume, key=getKey, reverse=True)
	highvolumetop10 = totvolume[0:10]
	print("High volume dates:")
	print(highvolumetop10)
	
	#Given the high volume dates and print out the stock data from these dates
	datahighvolumetop10={}
	datevals = []
	highvolume = []
	for pair in highvolumetop10:
		dt = pair[0]
		datevals.append(dt)
		highvolume.append(round(pair[1]/1000000,0))
		datahighvolumetop10[dt]=[]
		for key,data in stockdata2.items():
			#print(key, stockdata[key][daterow[key][dt]])
			try:
				datahighvolumetop10[dt].append([key,stockdata[key][daterow[key][dt]]])
			except KeyError:
				#not all stocks may have data for each date write in this exception
				pass
			
	#create graph
	y_pos = np.arange(len(highvolume))
	plt.bar(y_pos, highvolume,color="blue")
	plt.xticks(y_pos, datevals, rotation=45)
	plt.ylabel("Total Volume Traded (Millions)")
	plt.title("Highest Volume Days (Top 10)")
	pylab.savefig("HighVolumeDays.png")
	plt.close()
			
	#return highest volume date
	return (highvolumetop10,datahighvolumetop10)
	
def find_profitable_stocks(highvolumetop10,datahighvolumetop10):
	profit= []
	topvoldt = highvolumetop10[0][0]
	# get data list (stock, date-data pairs)
	for row in datahighvolumetop10[topvoldt]:
		stock = row[0]
		data = row[1]
		#profit = (close-open)/open price
		profit.append([stock,(float(data[1])-float(data[2]))/float(data[2])])
		
	#now sort to get the most profitable stock
	profit = sorted(profit, key=getKey, reverse=True)
	print("Most profitable stock for {} (date with highest volume) is:  {}".format(topvoldt,profit[0][0]))
	print("The stock had a profit gain of {} percent.".format(round(profit[0][1]*100,1)))
	
	stockname = []
	stockprofit = []
	for row in profit[0:10]:
		stockname.append(row[0])
		stockprofit.append(row[1])
	
	#create graph
	y_pos = np.arange(len(stockprofit))
	plt.bar(y_pos, stockprofit, color="red")
	plt.xticks(y_pos, stockname)
	plt.ylabel("Percent Growth")
	plt.title("Stocks with Highest Growth on {}".format(topvoldt))
	pylab.savefig("HighGrowthStocks.png")
	plt.close()
	
	
def main(casetype):

	#Examine one of the files to understand the structure
	with open("prices/aapl.csv", 'r') as f:
		aapl = f.read().strip()
		aapl = aapl.split("\n")
		aapl = [a.split(",") for a in aapl]
		print(aapl[0:10])

	#Read-in all of the files from the directory
	files = os.listdir("prices")
	filenames = ["prices/{}".format(f) for f in files]
	#uncomment the line below if interested only testing the code on a subset of data since the script takes too long to run
	#filenames = filenames[0:5]
	
	if casetype == 1:
		#have not got this one to work
		start = time.time()
		with concurrent.futures.ProcessPoolExecutor(max_workers=2)	as executor:
			output = [executor.submit(format_file1,file) for file in filenames]
			for future in concurrent.futures.as_completed(output):
				#stock = output[future]
				try:
					stockdata = future.result()
				except Exception as exc:
					print('Generated an exception at %s' % (stock))
				else:
					print('Success in reading in %s' % (stock))
			stockdata=list(stockdata)
			stockdata=dict(stockdata)
		print("Elapsed time Process Pool (w/ {} workers): {}".format(2,time.time()-start))
		print(stockdata["aapl"][0][0])
	elif casetype == 2:
		start = time.time()
		#Another to write with map function instead which greatly shortens the lines of code
		with concurrent.futures.ProcessPoolExecutor(max_workers=2)	as executor:
			result = executor.map(format_file1,filenames,timeout=9999)
			stockdata = list(result)
			stockdata = dict(stockdata)
		print("Elapsed time Process Pool (w/ {} workers): {}".format(2,time.time()-start))
		#Checking that the data has been read in correctly
		print("aapl line 1: ", stockdata["aapl"][0])
		print("aapl line 2: ", stockdata["aapl"][1])
	
	stockdata2 = compute_aggregates(stockdata)
	stockdata3=most_traded(stockdata2)
	highvolumetop10, datahighvolume = find_high_volume_days(stockdata2,stockdata)
	find_profitable_stocks(highvolumetop10, datahighvolume)

# This is used to ensure that this section code runs only when directly called from called line 
# As opposed to being called through another module.  Mainly needed when processing directly from windoes
if __name__ == '__main__':
	main(2)
	
