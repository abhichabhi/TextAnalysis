import itertools, getpass
import csv
import logging
import datetime

class PrefixSuffixDictGenerator():
	def __init__(self,category):
		self.prefixFile = "/home/" + getpass.getuser() + "/ScrapperInput/TextAnalysis/" + category + "/prefix.csv"
		self.suffixFile = "/home/" + getpass.getuser() + "/ScrapperInput/TextAnalysis/" + category + "/suffix.csv"
		self.keywordsToActual = "/home/" + getpass.getuser() + "/ScrapperInput/TextAnalysis/" + category + "/Keywords.csv"
		self.attributeMatching = "/home/" + getpass.getuser() + "/ScrapperInput/TextAnalysis/" + category + "/AttributeMatching.csv"
	
	def getPrefixDict(self):
		allRows = self.getListFromCSV(self.prefixFile)
		allKeywords = [row[0] for row in allRows]
		allKeywords = list(set(allKeywords))
		keyWordAttributeDict = {}
		keyWordAttributeCommentDict = {}
		for row in allRows:
			try:
				attributeCommentDict = keyWordAttributeCommentDict[row[0]]
				try:
					commentListForAttribute = attributeCommentDict[row[3]]
					commentListForAttribute.append([row[1],row[2]])
					attributeCommentDict[row[3]] = commentListForAttribute
				except:
					commentListForAttribute = {}
					attributeCommentDict[row[3]] = [row[1],row[2]]
				
			except:
				attributeCommentDict = {}
				attributeCommentDict[row[3]] = [row[1],row[2]]
				keyWordAttributeCommentDict[row[0]] = attributeCommentDict
		return keyWordAttributeCommentDict

	def getSuffixDict(self):
			allRows = self.getListFromCSV(self.suffixFile)
			allRows = allRows + self.getListFromCSV(self.prefixFile)
			allKeywords = [row[0] for row in allRows]
			allKeywords = list(set(allKeywords))
			keyWordAttributeDict = {}
			keyWordAttributeCommentDict = {}
			for row in allRows:
				try:
					attributeCommentDict = keyWordAttributeCommentDict[row[0]]
					try:
						commentListForAttribute = attributeCommentDict[row[3]]
						commentListForAttribute.append([row[1],row[2]])
						attributeCommentDict[row[3]] = commentListForAttribute
					except:
						commentListForAttribute = {}
						attributeCommentDict[row[3]] = [row[1],row[2]]
					
				except:
					attributeCommentDict = {}
					attributeCommentDict[row[3]] = [row[1],row[2]]
					keyWordAttributeCommentDict[row[0]] = attributeCommentDict


			return keyWordAttributeCommentDict

	def getAllKeywordsAndAttributes(self):
		allRows = self.getListFromCSV(self.prefixFile)
		allKeywords = [row[0] for row in allRows]
		allKeywords = list(set(allKeywords))
		keyWordAttributeDict = {}
		keyWordAttributeCommentDict = {}
		for row in allRows:
			try:
				attributeListForKeyword = keyWordAttributeDict[row[0]]
				attributeListForKeyword.append(row[3])
				attributeListForKeyword = list(set(attributeListForKeyword))
				keyWordAttributeDict[row[0]] = attributeListForKeyword
			except:
				keyWordAttributeDict[row[0]] = [row[3]]

		return allKeywords, keyWordAttributeDict

	def getkeywodToActual(self):
		allRows = self.getListFromCSV(self.keywordsToActual)
		allKeywords = [row[0] for row in allRows]
		allKeywords = list(set(allKeywords))
		keyWordActualDict = {}
		for row in allRows:
			try:
				attributeListForKeyword = keyWordActualDict[row[0]]
				attributeListForKeyword = row[1]
				attributeListForKeyword = list(set(attributeListForKeyword))
				keyWordActualDict[row[0]] = attributeListForKeyword
			except:
				keyWordActualDict[row[0]] = row[1]
		return keyWordActualDict

	def getAttributeProsCons(self):
		allRows = self.getListFromCSV(self.attributeMatching)
		allKeywords = [row[0] for row in allRows]
		allKeywords = list(set(allKeywords))
		keyWordAttributeCommentDict = {}
		keyWordAttributeCommentDict = {}
		for row in allRows:
			try:
				attributeCommentDict = keyWordAttributeCommentDict[row[0]]
				try:
					commentListForAttribute = attributeCommentDict[row[1]]
					# commentListForAttribute.append([row[3],row[4]])
					# attributeCommentDict[row[1]] = commentListForAttribute
				except:
					commentListForAttribute = {}
					attributeCommentDict[row[1]] = [row[3],row[4]]
				
			except:
				attributeCommentDict = {}
				attributeCommentDict[row[1]] = [row[3],row[4]]
				keyWordAttributeCommentDict[row[0]] = attributeCommentDict
		return keyWordAttributeCommentDict

	def getListFromCSV(self, filename):
		profileLinks = []
		with open(filename, 'r') as f:
			readColumns = (csv.reader(f, delimiter=','))
			iter = 0
			for row in readColumns:
				profileLinks.append(row)
			return profileLinks
