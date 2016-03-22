import urllib2
import urllib
import nltk
from bs4 import BeautifulSoup
import re
import requests
import justext
import unicodedata
from nltk.tokenize import RegexpTokenizer
from urllib import urlopen
from nltk.corpus import stopwords


def getWikilinks(query):
        
        results = []
	q =t= re.sub(' ', '_', query)
  	#wikiurl_q = 'https://en.wikipedia.org/wiki/'+q
  	wikiurl_q ='https://en.wikipedia.org/w/index.php?title='+q+'&action=edit'
  	data = urllib2.urlopen (wikiurl_q).read()
  	
  	
  	#parsed = BeautifulSoup(data)
  	#topics = parsed.findAll('a')
  	#results =[link['href'] for link in topics if link.has_attr('href')]
  	
  	soup = BeautifulSoup(data, 'html.parser')
  	text = soup.get_text()
  	
  	'''for link in soup.find_all('a'):
        	print(link.get('href'))'''
  	res =  re.findall('\[\[(?:[^\]|]*\|)?([^\]|]*)\]\]', text)
  	for i in res:
  		results.append(unicodedata.normalize('NFKD', i).encode('ascii','ignore'))
  		#results.append(i.decode('unicode_escape').encode('ascii','ignore'))
  	
        #print results
	return results


def main():
	inp = open('queries.txt').readlines()
	out = open('wiki_outlinks.txt','w')
	
	all_results = {}
	
	for art_title in inp:
  		query = art_title.strip()
  		results = getWikilinks(query)
  		results = ','.join(results)
	        all_results[query] = results
                
        for key,value in all_results.items():
        	out.write(key+':'+value+'\n')
        	
if __name__=="__main__":
	main()
