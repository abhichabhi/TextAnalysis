'''Runs the  RougeNation Class that performs the TextAnalysis of all the reviews
	Input: category: category of the product
	Output: /home/stratdecider/ScrapperOutput/TextAnalysis/category/Sentiment/Sentiment.csv
	and /home/stratdecider/ScrapperOutput/TextAnalysis/category/ProsCons/ProsCons.csv'''
import pprint
import logging
import json, sys
from RougeNation import RougeNation
if __name__ == "__main__":
	category = None
	try:
		category = sys.argv[1]
	except:
		print "Enter Category. Eg: mobile"
	if category:
		rougeNation = RougeNation(category)
		rougeNation.primeAllFileTextAnalyzer()
	
