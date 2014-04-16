package br.com.intelie.google_search_util;
import java.util.List;

import br.com.intelie.google_search_util.impl.GoogleAjaxServiceAPI;
import br.com.intelie.google_search_util.impl.GoogleWebSearch;
import br.com.intelie.google_search_util.interfaces.GoogleSearchTitleExtractor;
import br.com.intelie.google_search_util.util.Util;


public class Main {

	public static void main(String[] args) {
		
		String term = "";
		GoogleSearchTitleExtractor googleSearch = null;
		
		if(args.length == 0){
			System.out.println("O termo de busca precisa ser informado");
			System.exit(1);
		}
		else{
			
			term = args[0];
			if(term.isEmpty()){
				System.out.println("O termo de busca não pode ser vazio");
				System.exit(1);
			}
			if(args.length > 1 && args[1].equalsIgnoreCase("webSearch")){
				googleSearch = new GoogleWebSearch();
			}
			else{
				googleSearch = new GoogleAjaxServiceAPI();
			}
		}
		

		List<String> titulos = googleSearch.extractListTitles(term);
		
		for (String titulo : titulos) {
			System.out.println(titulo);
		}
		
		Util util = new Util();
		System.out.println("\nNúmero de ocorrências: " + util.occurrencesCount(titulos, term));
	}

}
