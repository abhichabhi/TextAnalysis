import sys, os, csv
import getpass
from os.path import isfile, join
class PrefixSuffixGenerator():
	def __init__(self, category):
		self.category = category
		self.ReviewsFileLocation = "/home/" + getpass.getuser() + "/ScrapperOutput/ReviewScrapper/"+ category + "/UnifiedReviews/"
		self.keyWordList = self.__getListFromCSV("./csvFiles/Keywords.csv")
		self.prefixfile = "./csvFiles/" + category + "/" + "prefix.csv"
		self.suffixfile = "./csvFiles/" + category + "/" + "suffix.csv"
		self.puntuationList = ['.', ';', '!', '<br>', '<p>', '</br>', '</p>', '?']

	def storePrefixandSuffix(self):
		reviewFileList = self.__getReviewFileList()
		for files in reviewFileList:
			reviewBlobFromFile = self.__getListFromCSV(self.ReviewsFileLocation + files)
			self.__storePrefixSuffixFromReviewBlob(reviewBlobFromFile)

	def __storePrefixSuffixFromReviewBlob(self, reviewBlob):		
		reviewLineList = self.getReviewBlockPuntuated(reviewBlob)
		for reviewLine in reviewLineList:
			
			for keyword in self.keyWordList:
				keyword = keyword[0]
				if " " + keyword + " " in reviewLine:
					Prefix,Suffix = self.getPrefixSuffixFive(reviewLine.lower().split(keyword.lower())[0], reviewLine.lower().split(keyword.lower())[1])
					self.writeToFile([Prefix, keyword],self.prefixfile)
					self.writeToFile([Suffix, keyword],self.suffixfile)
					# print Prefix, keyword.upper(), Suffix
		return None, None

	def getPrefixSuffixFive(self,Prefix,Suffix):
		Prefix = Prefix.split(" ")
		Prefix = Prefix[-6:]
		Prefix = " ".join(Prefix)
		Suffix = Suffix.split(" ")
		Suffix = Suffix[0:6]
		Suffix = " ".join(Suffix)
		return Prefix,Suffix

	def getReviewBlockPuntuated(self,allReviewsForFile):		
		allReviewStringForFile = []
		reviewSring = ""
		for allReview in allReviewsForFile:
			try:
				reviewSring = allReview[1]
			except:
				print "Error getting review from row ", reviewSring
			for puntuation in self.puntuationList:
				# try:
				# 	reviewSring = "".join(reviewSring)
				# except:
				# 	pass
				reviewSring = reviewSring.replace( puntuation, "#")
			reviewSring = reviewSring.split("#")
			allReviewStringForFile.extend(reviewSring)
		allReviewStringForFile = [reviews.strip() for reviews in allReviewStringForFile]
		allReviewStringForFile = list(set(allReviewStringForFile))
		return allReviewStringForFile		

	def __getReviewFileList(self):
		fileNameList = [file for file in os.listdir(self.ReviewsFileLocation) if isfile(join(self.ReviewsFileLocation,file))]
		return fileNameList

	def __getListFromCSV(self, filename):
	        profileLinks = []
	        with open(filename, 'r') as f:
	            readColumns = (csv.reader(f, delimiter=','))
	            iter = 0
	            for row in readColumns:
	                profileLinks.append(row)
	            return profileLinks

	def writeToFile(self,row,filename):
		
	        fileName = filename
	        if not os.path.exists(os.path.dirname(fileName)):
	            os.makedirs(os.path.dirname(fileName))
	            # with open(filename, 'a') as outcsv:
	            # #configure writer to write standart csv file
	            #     writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')            
	            #     writer.writerow(self.amazon_HeadingList)
	            
	        with open(filename, 'a') as outcsv:   
	            #configure writer to write standart csv file
	            
	            writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')            

if __name__ == "__main__":
	PrefixSuffixGenerator(sys.argv[1]).storePrefixandSuffix()
	# try:
	# 	PrefixSuffixGenerator(sys.argv[1]).storePrefixandSuffix()
	# except:
	# 	print "dude fuck you;  cmd: python PrefixSuffixGenerator.py mobile"

