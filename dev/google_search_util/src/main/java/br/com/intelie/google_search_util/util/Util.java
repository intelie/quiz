package br.com.intelie.google_search_util.util;

import java.util.List;

public class Util {
	
	private final String SEPARADORES = "\\+|–|«|\t|\"|\'|»|\\||\\>|\\...|\\.|\\]|\\[|[0-9]|,|\\?|:|\\(|\\)|;|-|!";
	
	public Integer occurrencesCount(List<String> list, String term){
		
		Integer counter = 0;
		LevenshteinDistance levenshteinDistance = new LevenshteinDistance();
		
		for (String item : list) {
			
			item = item.replaceAll(SEPARADORES, "");
			String[] itens = item.split(" ");
			
			for (int i = 0; i < itens.length; i++) {
				if(levenshteinDistance.computeLevenshteinDistance(term, itens[i]) <=2){
					counter++;
				}
			}
		}
		return counter;
		
	}

}
