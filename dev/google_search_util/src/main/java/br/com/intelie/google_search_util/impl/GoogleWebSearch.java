package br.com.intelie.google_search_util.impl;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import br.com.intelie.google_search_util.interfaces.GoogleSearchTitleExtractor;

/**
 * Hello world!
 *
 */
public class GoogleWebSearch implements GoogleSearchTitleExtractor
{
   
	private List<String> extraiTitulos(Document doc) {
		
		List<String> titulos = new ArrayList<String>();
		Elements resultLinks = doc.select("h3.r > a");
		for (Element element : resultLinks) {
			String t = element.text();
			titulos.add(t);
		}
		return titulos;
	}

	public List<String> extractListTitles(String term) {
		
		List<String> titulos = new ArrayList<String>();
    	
    	String url = "http://www.google.com.br/search";
    	
		try {
			Document doc = Jsoup.connect(url)
					.data("q", term)
					.userAgent("Mozilla/5.0").get();
			
			titulos.addAll(extraiTitulos(doc));
			
			Elements mais = doc.select("td.b > a");
			while(!mais.isEmpty()){
				String proxPagina = mais.attr("href");
				doc = Jsoup.connect("http://www.google.com.br"+proxPagina)
						.userAgent("Mozilla/5.0")
						.timeout(10000).get();
			
				titulos.addAll(extraiTitulos(doc));
			    
			    mais = doc.select("td.b>a:has(:contains(Mais))");
			}
		} catch (IOException e) {
			throw new IllegalStateException("Houve um erro ao consultar o web search do google: " + e.getMessage(), e);
		} 
        
        return titulos;
        
	}
}
