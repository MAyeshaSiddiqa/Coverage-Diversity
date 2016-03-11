import urllib2
import urllib
import nltk
from bs4 import BeautifulSoup
import re
from nltk.tokenize import RegexpTokenizer
from urllib import urlopen
from nltk.corpus import stopwords

##------------------- remove multiple occurences of the same term ---------------##

def uniquify(string):
    output = []
    seen = set()
    for word in string.split():
        if word not in seen:
            output.append(word)
            seen.add(word)
    return ' '.join(output)

##----------------------------- Get search results -----------------------------##

def getSearchResultDDG(query):
	q =t= re.sub(' ', '_', query)
  	wikiurl_q = 'https://en.wikipedia.org/wiki/'+q
  	query = urllib2.quote(query.encode('utf8'))
  	uri ='http://duckduckgo.com/html/?q='+query
  	data = urllib2.urlopen (uri).read()
  	parsed = BeautifulSoup(data)
  	topics = parsed.findAll('a')
  	results =[link['href'] for link in topics if link.has_attr('href')] 

  	if results != []:
    		results.pop(0)

        if wikiurl_q in results:
		try:
			results.remove(wikiurl_q)
		except:
			pass
      
	return results

##----------------------- Represent text in ESA concept vector -------------------##

def cvs(new2):
 #print len(new2)
	encoded = urllib2.quote(new2.encode('utf8'))
        response2 = urllib2.urlopen('http://vmdeb20.deri.ie:8890/esaservice?task=vector&source='+encoded+'&limit=10')
	#response2 = urllib2.urlopen('http://10.6.30.43:8800/esaservice?task=vector&source='+encoded+'&limit=10')
	concepts = response2.read()
	cv = re.findall('"([^"]*)"',concepts)
	#print len(cv)
	cvs = []
	#cvs.append([])
	for i in range(0,len(cv)):
     		cvs.append( cv[i].split(',') )
        # best practice to close the file
	response2.close()
	return cvs

##--------------------------------- ESA limitations in representation ----------------##

def getConceptVectors(result_uri):
    #print result_uri
    conceptvectors = []
    try:
    	#print 'entered get concept vectors'
    	response1 = urllib2.urlopen(result_uri)
    	html = response1.read()
    	soup = BeautifulSoup(html,'html.parser')
	#raw = nltk.clean_html(h)
    	#print(raw)
        raw = soup.get_text()
    	tokenizer = RegexpTokenizer(r'\w+')
    	tokenized_data = tokenizer.tokenize(raw)
    	data = ' '.join(tokenized_data)
    	#print len(data)
        #------ Remove stop words----------------#
        stop = stopwords.words('english')
        non_stop = [i for i in data.split() if i not in stop]
        data = ' '.join(non_stop)

    	unique_words = uniquify(data)
	print '-----------------------------------------------------------------\n',unique_words
    	print len(unique_words)
    	
        '''d = len(unique_words)/5000
    	r = len(unique_words) % 5000
    	s = int(0)
    	l = int(5000)
    	if (d != 0):
     		for i in range(0,d):
         		unique_words2 = unique_words[s:l]
            		cv = cvs(unique_words2)
            		#print cv
            		#for i in range(0,len(cv)):
                		#conceptvectors.append(cv)
            		s = l
            		l = l+5000
        if(r == 0):
        	pass
        else:
         #print r
        	unique_words2 = unique_words[s:l]
		#print unique_words2
        	cv = cvs(unique_words2)
		#print cv'''
    except urllib2.URLError, e:
    	print '---code---',e	
    #return conceptvectors

##------------------------ Not covered concepts in Stub ------------------------##
def NotOverlappingConcepts(articleConcepts,wikiConcepts):
	notcoveredinwiki = []
	ac = set(articleConcepts)
	wc = set(wikiConcepts)
	cc = ac.intersection(wc)
    	# set intersection
    	#print 'concepts common in between article and wikiarticle'
    	#print len(cc)
    	#  set difference between other article and non wiki article
    	ncw1 = ac.difference(wc)
    	#print 'covered in article but not in wiki'
    	#print len(ncw1)
	ncw2 =  wc.difference(ac)
    	#print 'covered in wiki but not in article'
    	#print len(ncw2)
    	notcoveredinwiki = list(ncw1)
   	return notcoveredinwiki


##-------------------------- main program -------------------------------------------##

def main():

	inp = open('queries.txt').readlines()
        # fetch results from search engine 
	results = []
	for art_title in inp:
  		query = art_title.strip()
  		results = getSearchResultDDG(query)

        AllConceptvectors = []
    	for i in range(0,len(results)):
        	uri = results[i]
        	temp = getConceptVectors(uri)
        	'''if(temp != []):
        		AllConceptvectors.append(temp)

        tot = len(AllConceptvectors)
        
        WikiConceptvector = []
        wiki_uri = 'https://en.wikipedia.org/w/index.php?title=Deep_learning&diff=440438638&oldid=440437784'
        WikiConceptvector = getConceptVectors(uri)

    	notcoveredconcepts  = []
    	for i in range(0,tot-1):
        	temp = NotOverlappingConcepts(AllConceptvectors[i],WikiConceptvector)
        	newtemp = ','.join(temp)
		notcoveredconcepts.append(temp)

	print '----notcoveredconcepts----\n', notcoveredconcepts'''
        '''for i in range(0,len(inp)):
	    results.append( inp[i].rstrip())'''

if __name__=="__main__":
	main()

