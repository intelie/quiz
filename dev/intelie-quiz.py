#!/usr/bin/env python
# encoding: utf-8

"""
author: Danillo Souza <danillo012@gmail.com>
date: 2012-11-13

Saber quantas vezes o termo buscado é contido nos títulos das páginas retornadas como resultado. 
O termo pode aparecer mais de uma vez em um mesmo título.
Considerar também termos que tenham sido digitados erradamente, com distância de Levenshtein de no máximo 2.


Uso: $ python intelie-quiz.py <termo da busca>

"""

import re
import sys
import urllib
import urllib2
import simplejson

def get_google_headers(term):
	"""
	Retorna uma lista com os Headers dos resultados.
	"""
	
	titles = []
	url = ('https://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + urllib.urlencode({'q': term}))
	
	request = urllib2.Request(url, None, {})
	response = urllib2.urlopen(request)
	
	results = simplejson.load(response)
	
	for result in results['responseData']['results']:
		titles.append( re.sub('<[^<]+?>', '', result['title']) ) # remove tags html e adiciona à lista de retorno
	
	return titles



def lev_distance(a, b):
	"""
	Calcula a Distância de Livenshtein entre duas strings.
	
	Baseado em: http://en.wikipedia.org/wiki/Levenshtein_distance#Computing_lev_distance_distance
	"""
	
	if len(a) < len(b): return lev_distance(b, a)
	if not len(b): return len(a)

	previous_row = xrange(len(b) + 1)

	for x, c1 in enumerate(a):
		current_row = [x + 1]

		for y, c2 in enumerate(b):
			current_row.append(min(previous_row[y + 1] + 1, current_row[y] + 1, previous_row[y] + (c1 != c2)))

		previous_row = current_row

	return previous_row[-1]



def classify(term, titles):
	"""
	Classifica em quais titulos o termo aparece (ou similar com distância de Levenshtein de no máximo 2).
	Retorna um dicionário contendo o número de ocorrências e os títulos com essas ocorrências.
	"""

	counter = 0
	old_counter = counter
	titles_containing = []
	
	for title in titles:
		words = re.split('[\s,\.!\?~\[\]]', title)
		
		for word in words:
			if lev_distance(term, word) <= 2:
				counter += 1
			
		if counter > old_counter:
			titles_containing.append(title)
			old_counter = counter
	
	return {"counter": counter, "titles": titles_containing}



if __name__ == '__main__':

	try:
		term = sys.argv[1]
	except:
		print "Uso: $ python %s <termo da busca> \n" % sys.argv[0]
		sys.exit(1)
	
	titles = get_google_headers(term)
	founds = classify(term, titles)
	
	print "Encotrados %d título(s) contento %d ocorrência(s) de %s no total (ou muito similar)\n" % (len(founds['titles']), founds['counter'], term)
	
	for title in founds['titles']:
		print "\t- %s" % title
	
	print
