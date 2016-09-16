import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.util.ArrayList;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class PesquisaGoogle {

	public static void pesquisaTermo(String termo) throws UnsupportedEncodingException, IOException {
		
		String google = "http://www.google.com/search?q="+termo+"&num=100";
		String userAgent = "Mozilla/5.0 (Windows; U; WindowsNT 5.1; en-US; rv1.8.1.6) Gecko/20070725 Firefox/2.0.0.6";
		int contador = 0;

		Elements links = Jsoup.connect(google).userAgent(userAgent).get().select(".g>.r>a");
		System.out.println("Titulos :\n");
		
		for (int i = 0; i<links.size(); i++) {
		    System.out.println((i+1)+") " + links.get(i).text());
		   	for (String s: links.get(i).text().split(" ")) {
		   		if (Levenshtein.calculaDistancia(termo, s)<=2) {
		   			contador++;
		   		}
		   	}
		}
		
		System.out.println("Numero de Titulos: "+ links.size());
		System.out.println("Numero em que o termo "+termo+" aparece respeitando a distancia de Levenshtein menor que 2: "+contador);
	}

}
