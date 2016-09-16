import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.net.URLEncoder;

//import javax.lang.model.element.Element;
//import javax.lang.model.util.Elements;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class Outra {
	public static void main(String[] args) throws UnsupportedEncodingException, IOException {
		String google = "http://www.google.com/search?q=";
		String search = "árvore";
		String charset = "UTF-8";
		String userAgent = "Mozilla/5.0 (Windows; U; WindowsNT 5.1; en-US; rv1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"; // Change this to your company's name and bot homepage!

		Elements aux = Jsoup.connect(google + URLEncoder.encode(search, charset)).userAgent(userAgent).get().select(".g>.r>a");
		Elements links = Jsoup.connect(google + URLEncoder.encode(search, charset)).userAgent(userAgent).get().select(".g>.r>a");

		for (Element link : aux) {
		    String title = link.text();
		    //String url = link.absUrl("href"); // Google returns URLs in format "http://www.google.com/url?q=<url>&sa=U&ei=<someKey>".
		    //url = URLDecoder.decode(url.substring(url.indexOf('=') + 1, url.indexOf('&')), "UTF-8");

		    //if (!url.startsWith("http")) {
		      //  continue; // Ads/news/etc.
		    //}

		    System.out.println("Title: " + title);
		    //System.out.println("URL: " + url);
		}
	}
}
