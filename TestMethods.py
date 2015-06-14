import pprint
import logging
import json
from dictGenerator.PrefixSuffixDictGenerator import PrefixSuffixDictGenerator
from RougeNation import RougeNation
LOG = "/home/stratdecider/ScrapperLogging/TextAnalysis.log"                                                     
logging.basicConfig(filename=LOG, filemode="w", level=logging.DEBUG)  

# console handler  
console = logging.StreamHandler()  
console.setLevel(logging.ERROR)  
logging.getLogger("").addHandler(console)
def testPreficDictGenerator():
	prefixSuffixDictGenerator = PrefixSuffixDictGenerator()
	# keyWordAttributeCommentDict = prefixSuffixDictGenerator.getPrefixDict()
	# print keyWordAttributeCommentDict
	# allKeywords, keyWordAttributeDict = prefixSuffixDictGenerator.getAllKeywordsAndAttributes()
	# keyWordActualDict = prefixSuffixDictGenerator.getkeywodToActual()
	# print keyWordActualDict
	# pprint.pprint(keyWordActualDict)
	rougeNation = RougeNation()
	rougeNation.primeAllFileTextAnalyzer() 

testPreficDictGenerator()