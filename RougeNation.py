import pprint
import logging
from decimal import *
import json, csv, os
from os import listdir
from os.path import isfile, join
from dictGenerator.PrefixSuffixDictGenerator import PrefixSuffixDictGenerator
from difflib import SequenceMatcher
from operator import add
class RougeNation:
	LOG = "/home/stratdecider/ScrapperLogging/TextAnalysis.log"
	logging.basicConfig(filename=LOG, filemode="w", level=logging.DEBUG)
	AllReviewFolder = "/home/stratdecider/ScrapperOutput/ReviewScrapper/NewPhoneReviews/" 
	puntuationList = [".",";","!"]
	prefixSuffixDictGenerator = PrefixSuffixDictGenerator()
	keyWordList, keyWordAttributeDict = prefixSuffixDictGenerator.getAllKeywordsAndAttributes()
	keyWordPrefixDict = prefixSuffixDictGenerator.getPrefixDict()
	keyWordSuffixDict = prefixSuffixDictGenerator.getSuffixDict()
	keyWordActualDict = prefixSuffixDictGenerator.getkeywodToActual()
	attributeProsCons = prefixSuffixDictGenerator.getAttributeProsCons()
	def getAllFilesFromFolder(self):
			allCSVFiles = [ f for f in listdir(self.AllReviewFolder) if isfile(join(self.AllReviewFolder,f)) ]
			return allCSVFiles
	def primeAllFileTextAnalyzer(self):
		allCSVFiles  = self.getAllFilesFromFolder()

		for file in allCSVFiles:
			filename = self.AllReviewFolder + file
			allReviewsForFile = self.getListFromCSV(filename)
			
			allKeyWordScore = self.primeReviewFileAnalyzer(file, allReviewsForFile)
			# pprint.pprint(allKeyWordScore)
			self.prepareSentimentFile(allKeyWordScore, file)
			self.prepareProsAndConsFile(allKeyWordScore, file)

	def primeReviewFileAnalyzer(self, file, allReviewsForFile):
		reviewBlockPuntuated = self.getReviewBlockPuntuated(allReviewsForFile)
		allKeyWordScore = {}
		for reviewBlock in reviewBlockPuntuated:
			for keyword in  self.keyWordList:
				allKeyWordAttributeScore = {}
				finalAttr = ''
				finalIndex = 0
				pos = 0
				neg = 0
				neu = 0
				zer = 0
				if keyword.lower() in reviewBlock.lower().split():

					attributeScore = []
					Prefix,Suffix = self.getPrefixSuffixFive(reviewBlock.lower().split(keyword.lower())[0], reviewBlock.lower().split(keyword.lower())[1])
					SuffixTone, maxSuffixAttribute, sentimentIndexSuffix = self.getBestFitTone(keyword,Suffix,"Suffix")
					PrefixTone, maxPrefixAttribute, sentimentIndexPrefix = self.getBestFitTone(keyword,Prefix,"Prefix")
					# if maxPrefixAttribute == "" and maxPrefixAttribute == "":
					# 	continue
					if SuffixTone > PrefixTone:
						finalIndex = sentimentIndexSuffix
						finalAttr = maxSuffixAttribute
					else:
						finalIndex = sentimentIndexPrefix
						finalAttr = maxPrefixAttribute
					try:
						allKeyWordAttributeScore = allKeyWordScore[keyword]
						try:
							attributeScore = allKeyWordAttributeScore[finalAttr]
							pos = attributeScore[0]
							neg = attributeScore[1]
							if finalIndex == '1':
								neg = neg + 1
							elif finalIndex == '3':
								pos = pos + 1
							# elif finalIndex == '2':
							# 	neu = neu + 1
							# elif finalIndex == '0':
							# 	zer = zer + 1
							# attributeScore = [pos,neu,neg, zer]
							attributeScore = [pos,neg]
							allKeyWordAttributeScore[finalAttr] = attributeScore
						except:
							pos = 0
							neg = 0
							neu = 0
							zer = 0
							if finalIndex == '1':
								neg = neg + 1
							elif finalIndex == '3':
								pos = pos + 1
							# elif finalIndex == '2':
							# 	neu = neu + 1
							# elif finalIndex == '0':
							# 	zer = zer + 1
							# attributeScore = [pos,neu,neg, zer]
							attributeScore = [pos,neg]
							allKeyWordAttributeScore[finalAttr] = attributeScore
						allKeyWordScore[keyword] = allKeyWordAttributeScore
					except:
						pos = 0
						neg = 0
						if finalIndex == '1':
							neg = neg + 1
						elif finalIndex == '3':
							pos = pos + 1
						# elif finalIndex == '2':
						# 	neu = neu + 1
						# elif finalIndex == '0':
						# 	zer = zer + 1
						# attributeScore = [pos,neu,neg, zer]
						attributeScore = [pos,neg]
						allKeyWordAttributeScore[finalAttr] = attributeScore
						allKeyWordScore[keyword] = allKeyWordAttributeScore
		return  allKeyWordScore

	def prepareSentimentFile(self, sentimetDict,file):
		filePath = "/home/stratdecider/ScrapperOutput/TextAnalysis/Sentiment/Sentiment.csv"
		file = file.replace(".csv","")
		brand = file.split()[0]
		actualKeyWordSentimentDict = {}
		for actualKeywords in self.keyWordActualDict:
			actualKeyWordSentimentDict[self.keyWordActualDict[actualKeywords]] = [0,0,0]
		model = file
		totalPos = 0
		totalNeg = 0
		for keywords in sentimetDict:
			csvRow = []
			totalPos = 0
			totalNeg = 0
			totalNeu = 0
			attrDict = sentimetDict[keywords]
			for attr in attrDict:
				if attr != "":
					values = attrDict[attr]
					pos = values[0]
					neg = values[1]
					totalNeg = totalNeg + neg
					totalNeu = 0
					totalPos = totalPos + pos
			countList = [totalNeg,totalNeu,totalPos]
			actualKey = ""
			try:
				actualKey = self.keyWordActualDict[keywords]
			except:
				pass
			if actualKey:
				actualKeyWordSentimentDict[actualKey] = [a + b for a, b in zip(countList, actualKeyWordSentimentDict[actualKey])]

			# map(add, countList, actualKeyWordSentimentDict[actualKey])
		# pprint.pprint(actualKeyWordSentimentDict)
		for keywords in actualKeyWordSentimentDict:
			csvRow = []
			totalPos = actualKeyWordSentimentDict[keywords][2]
			totalNeg = actualKeyWordSentimentDict[keywords][0]
			totalNeu = 0
			totalAttendence = totalPos + totalNeg
			if totalAttendence != 0:
				rating = 0.00
				csvRow.append(brand)
				csvRow.append(file)
				csvRow.append(keywords)
				csvRow.append(totalNeg)
				csvRow.append(0)
				csvRow.append(totalPos)
				rating = totalPos*5/float(totalAttendence)
				rating = "{:.2f}".format(rating)
				csvRow.append(rating)
				self.writeToFile(csvRow,filePath)


	def prepareProsAndConsFile(self, sentimetDict,file):
		filePath = "/home/stratdecider/ScrapperOutput/TextAnalysis/ProsCons/ProsCons.csv"
		file = file.replace(".csv","")
		brand = file.split()[0]
		keywordsProsConsDict = {}
		prosDict = {}
		consDict = {}
		for keywords in sentimetDict:
			prosDict = {}
			consDict = {}
			csvRow = []
			totalPos = 0
			totalNeg = 0
			totalNeu = 0
			attrDict = sentimetDict[keywords]
			try:
				actualKey = self.keyWordActualDict[keywords]
			except:
				actualKey = None
			for attr in attrDict:
				totalNeg = 0
				totalPos = 0
				csvRow = []
				cons = ""
				pros = ""
				prosDict = {}
				consDict = {}
				consDictVal = 0
				prosDictVal = 0
				if attr != "":
					values = attrDict[attr]
					pos = values[0]
					neg = values[1]
					totalNeg = totalNeg + neg
					totalNeu = 0
					totalPos = totalPos + pos
					if actualKey:
						keywordsProsConsDictValue = {}
						try:
							keywordsProsConsDictValue = keywordsProsConsDict[actualKey]
							prosDict = keywordsProsConsDictValue["pros"]
							consDict = keywordsProsConsDictValue["cons"]
							try:
								prosDictVal = prosDict[self.attributeProsCons[keywords][attr][0]]
								prosDictVal = prosDictVal + totalPos
								prosDict[self.attributeProsCons[keywords][attr][0]] = prosDictVal
							except:
								prosDictVal = totalPos
								if prosDictVal > 0:
									prosDict[self.attributeProsCons[keywords][attr][0]] = prosDictVal
							try:
								consDictVal = consDict[self.attributeProsCons[keywords][attr][1]]
								consDictVal = consDictVal + totalNeg
								consDict[self.attributeProsCons[keywords][attr][1]] = consDictVal
							except:
								consDictVal = totalNeg
								if consDictVal > 0:
									consDict[self.attributeProsCons[keywords][attr][1]] = consDictVal
						except:
							prosDictVal = totalPos
							try:
								if prosDictVal> 0 :
									prosDict[self.attributeProsCons[keywords][attr][0]] = prosDictVal
									keywordsProsConsDictValue["pros"] = prosDict
							except:
								pass
							consDictVal = totalNeg
							try:
								if consDictVal > 0: 
									consDict[self.attributeProsCons[keywords][attr][1]] = consDictVal
									keywordsProsConsDictValue["cons"] = consDict
							except:
								pass
							keywordsProsConsDict[actualKey]  = keywordsProsConsDictValue
		for keywords in keywordsProsConsDict:
			try:
				prosDict = keywordsProsConsDict[keywords]["pros"]
				
				for pros in prosDict:
					csvRow = []
					if prosDict[pros] != 0 and pros.strip() != "":
						proStatement = pros + " (" + str(prosDict[pros]) + ")"
						csvRow.append(brand)
						csvRow.append(file)
						csvRow.append(keywords)
						csvRow.append(proStatement)
						csvRow.append("")
						self.writeToFile(csvRow,filePath)
			except:
				pass
			try:
				consDict = keywordsProsConsDict[keywords]["cons"]
				for cons in consDict:
					csvRow = []
					if consDict[cons] != 0 and cons.strip() != "":
						consStatement = cons + " (" + str(consDict[cons]) + ")"
						csvRow.append(brand)
						csvRow.append(file)
						csvRow.append(keywords)
						csvRow.append("")
						csvRow.append(consStatement)
						self.writeToFile(csvRow,filePath)
			except:
				pass
		# pprint.pprint(keywordsProsConsDict)
						
	def getBestFitTone(self,keyword,subtring,part):
		keywordPartDict = {}
		attributeCommentDict = {}
		if part == "Suffix":
			keywordPartDict = self.keyWordSuffixDict
		else:
			keywordPartDict = self.keyWordPrefixDict
		try:
			attributeCommentDict =  keywordPartDict[keyword]
		except:
			pass
		maxTone = 0
		sentimentIndex = 0
		maxAttribute = ""
		for attr in attributeCommentDict:
			if (attr.lower() in subtring.lower()) and (attr != ""):
				tone = self.similar(attributeCommentDict[attr][0].lower(), subtring.lower())
				if maxTone < tone:
					maxTone = tone
					maxAttribute = attr
					sentimentIndex = attributeCommentDict[attr][1]
				break;
			elif attr == "":
				tone = self.similar(attributeCommentDict[attr][0].lower(), subtring.lower())
				if maxTone < tone:
					maxTone = tone
					maxAttribute = attr
					sentimentIndex = attributeCommentDict[attr][1]
		return maxTone, maxAttribute, sentimentIndex

	def similar(self,a, b):
		return SequenceMatcher(None, a, b).ratio()

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
				reviewSring =  allReview[4]
			except:
				pass
			for puntuation in self.puntuationList:
				
				try:
					reviewSring = "".join(reviewSring)
				except:
					pass
				reviewSring = reviewSring.replace( puntuation, "#")
			reviewSring = reviewSring.split("#")
			allReviewStringForFile.extend(reviewSring)
		allReviewStringForFile = list(set(allReviewStringForFile))
		return allReviewStringForFile

	def writeToFile(self,row,filename):
		if not os.path.exists(os.path.dirname(filename)):
			os.makedirs(os.path.dirname(filename))

		with open(filename, 'a') as outcsv:
			writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
			writer.writerow(row)
	def getListFromCSV(self, filename):
		profileLinks = []
		with open(filename, 'r') as f:
			readColumns = (csv.reader(f, delimiter=','))
			for row in readColumns:
				try:
					profileLinks.append(row)
				except:
					pass
			return profileLinks





