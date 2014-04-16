package br.com.intelie.google_search_util.impl;

import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;
import java.util.List;

import javax.json.Json;
import javax.json.JsonArray;
import javax.json.JsonObject;
import javax.json.JsonReader;

import br.com.intelie.google_search_util.interfaces.GoogleSearchTitleExtractor;

public class GoogleAjaxServiceAPI implements GoogleSearchTitleExtractor {

	public List<String> extractListTitles(String term) {
		List<String> titulos = new ArrayList<String>();
		
		try {
			
			for (int i = 0;; i+=4) {
				URL url = new URL(
						"http://ajax.googleapis.com/ajax/services/search/web?v=1.0&cr=countryBR&jl=pt-BR&q="
								+ term + "&start="+i);
				
				URLConnection connection = url.openConnection();
				connection.addRequestProperty("Referer", "www.google.com.br");
				JsonReader jsonReader = Json.createReader(connection.getInputStream());
				JsonObject jsonObject = jsonReader.readObject();
				
				if(!jsonObject.isNull("responseData")){
					
					JsonObject responseData = jsonObject.getJsonObject("responseData");
					JsonArray results = responseData.getJsonArray("results");
					for (JsonObject result : results.getValuesAs(JsonObject.class)) {
						titulos.add((result.getString("titleNoFormatting")));
					}
				}
				else{
					return titulos;
				}
			}
			
		} catch (Exception e) {
			throw new IllegalStateException("Houve um erro ao consultar a web search api do google: " + e.getMessage(), e);
		}
	}
}
