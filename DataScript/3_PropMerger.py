from __future__ import division
import csv
import pandas as pd
import statistics
import fileinput
import math
import sys

class PropMerger:
	
	def __init__(self, batchCnt, sensorCnt, sampleCnt, propCnt):
		self.batchCnt=batchCnt
		self.sensorCnt=sensorCnt
		self.sampleCnt=sampleCnt
		self.propCnt=propCnt
		self.batchSize=0
		self.file_list = []
		
		self.FProp = [[0 for x in range(sensorCnt)] for y in range(propCnt)]
		for prop in range (propCnt):
			for sensor in range(sensorCnt):
				self.FProp[prop][sensor] = []
	
	def loadData(self, inputFile):
		###printing file data
		print("\nFile data is:")
		
		filereader = csv.reader(open(inputFile), delimiter =',')
		for row in filereader:
			self.file_list.append(row)
		
		total_rows = len(self.file_list)
		total_cols = len(self.file_list[0])
		self.batchSize =  total_rows/(self.batchCnt*self.sampleCnt)
		
		print(self.file_list)
		print(self.file_list[0])
		print(total_rows)
		print(total_cols)
		
		for prop in range (self.propCnt):
			for sensor in range(self.sensorCnt):
				for batch in range(self.batchCnt):
					self.FProp[prop][sensor].append(self.file_list[batch*self.sensorCnt+sensor+1][prop])
	
	def netMean(self):
		# Net Mean
		for sensor in range(self.sensorCnt):
			temp = 0.0
			for batch in range(self.batchCnt):
				temp += float(self.FProp[0][sensor][batch])
			self.FProp[0][sensor].append(temp/self.batchCnt)
	
	def findMedian(self):
		# Median
		median = []
		for sensor in range(self.sensorCnt):
			for batch in range(self.batchCnt):
				median.append(self.FProp[1][sensor][batch])
			median.sort()
			mid_point = int(self.batchCnt/2)
			if(mid_point%2==0):       
				final_median = (float(median[mid_point-1])+float(median[mid_point]))/2
				self.FProp[1][sensor].append(float(final_median))
			else:
				self.FProp[1][sensor].append(float(median[mid_point]))
			median = []
	
	def fingSTD(self):
		# Standard deviation
		for sensor in range(self.sensorCnt):
			Stemp=0.0
			for batch in range(self.batchCnt):
				Stemp+=math.pow(float(self.FProp[4][sensor][batch]), 2)*(self.batchSize)
			if (self.batchSize*self.batchCnt) > 0:
				self.FProp[4][sensor].append(math.sqrt(Stemp/(self.batchSize*self.batchCnt)))
	
	def findVariance(self):
		# Variance = math.pow(std_dev, 2)
		for sensor in range(self.sensorCnt):
			self.FProp[5][sensor].append(math.pow(self.FProp[4][sensor][7], 2))
	
	def findRange(self):
		# Range
		for sensor in range(self.sensorCnt):
			self.FProp[6][sensor].append(float(self.FProp[2][sensor][7])-float(self.FProp[3][sensor][7]))
	
	def findSkewness(self):
		# Skewness = (3*(net_mean - final_median))/std_dev
		for sensor in range(self.sensorCnt):
			self.FProp[7][sensor].append((3*(float(self.FProp[0][sensor][7]) - float(self.FProp[1][sensor][7])))/float(self.FProp[4][sensor][7]))
	
	def findKurtosis(self):
		# Kurtosis = kurtosis_sum / math.pow(std_dev, 4)
		for sensor in range(self.sensorCnt):
			Ktemp=0.0
			for batch in range(self.batchCnt):
				Ktemp += float(self.FProp[8][sensor][batch])*self.batchSize*math.pow(float(self.FProp[4][sensor][batch]),4)
			self.FProp[8][sensor].append(Ktemp/(math.pow(float(self.FProp[4][sensor][7]),4)*self.batchCnt*self.batchSize))
	
	def saveData(self, outputFile):
		# Copy final data (self.FProp[Prop][sensor][batch]) into a .csv file
		with open(outputFile,"w") as my_final_file:
			writer = csv.writer(my_final_file)
			writer.writerow(["Batch1","Batch2","Batch3","Batch4","Batch5","Batch6","Batch7","TotalAvg"])
			for sensor in range(self.sensorCnt):
				for prop in range(self.propCnt):
					writer.writerow(self.FProp[prop][sensor])
	
	def calAvgProp(self, inputFile, outputFile):
		self.loadData(inputFile)
		self.netMean()
		self.findMedian()
		# Max
		for sensor in range(self.sensorCnt):
			self.FProp[2][sensor].append(max(list(map(float,self.FProp[2][sensor]))))

		# Min
		for sensor in range(self.sensorCnt):
			self.FProp[3][sensor].append(min(list(map(float,self.FProp[3][sensor]))))
		
		self.fingSTD()
	
		self.findVariance()
		self.findRange()
		self.findSkewness()
		self.findKurtosis()
		self.saveData(outputFile)

def main():
	inputFilePath = sys.argv[1] # "Output_data.csv"
	outputFilePath = sys.argv[2] # "Final_data.csv"
	
	batchCnt=7
	sensorCnt=40
	sampleCnt=40
	propCnt=9
	
	prop = PropMerger(batchCnt, sensorCnt, sampleCnt, propCnt)
	prop.calAvgProp(inputFilePath, outputFilePath)

main()