package desafiointelie.resources;

import org.apache.http.HttpResponse;
import java.io.IOException;
import java.net.URLEncoder;
import java.net.UnknownHostException;

import org.apache.http.HttpEntity;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;

import desafiointelie.json.JSONArray;
import desafiointelie.json.JSONException;
import desafiointelie.json.JSONObject;


/**
 * 
 * @author Gabriel Salvatti
 */
public class SearchEngine {

	JSONArray responseArray;
	int requestResponse;
	int startIndex;
	HttpClient httpclient = null;
	HttpGet httpget = null;

	public JSONArray jsonArrayResponse(String keyWords) throws IOException,
			JSONException {

		responseArray = new JSONArray();
		requestResponse = 0;
		startIndex = 1;
		
		keyWords = URLEncoder.encode(keyWords, "UTF-8");

		/*
		 * the loop runs until there isn't a next page. the custom search google
		 * api returns only the first 100 results and in pages of 10 results
		 * each. Then each search may need up to 10 requests (with 10 results
		 * each).
		 */
		boolean thereIsNextPage = true;
		while (thereIsNextPage) {
			httpclient = new DefaultHttpClient();

			// The search URL
			httpget = new HttpGet(""
					// API URL
					+ "https://www.googleapis.com/customsearch/v1?"
					// Google Developer's Key
					+ "key=AIzaSyBBqxJUehaqjKy7ne0cE3boENz2jRPczgY"
					// The code of the custom search engine
					+ "&cx=008610849337058204001:56qavpjavhe"
					// index Controller
					+ "&start=" + startIndex
					// fields to be returned (query parameters)
					+ "&fields=queries(nextPage/startIndex),items(title,link)"
					// term to be search
					+ "&q=" + keyWords
					// type of response = JSON String
					+ "&alt=json");

			try {
				HttpResponse response = httpclient.execute(httpget);
				HttpEntity entity = response.getEntity();
				String responseString = EntityUtils.toString(entity);
				
				//defines whether the request was successful
				requestResponse = response.getStatusLine().getStatusCode();
				switch (requestResponse) {
				case 200:
					//if it was successful...
					JSONObject jSONObject = new JSONObject(
							responseString.trim());
					responseArray.put(jSONObject.getJSONArray("items"));
					//gets the starting index of the next page of the results
					startIndex = jSONObject.getJSONObject("queries")
							.getJSONArray("nextPage").getJSONObject(0)
							.getInt("startIndex");
					break;

				case 500:
					//if the Custom Search server is down...
					System.out
							.println("It has not been possible to connect to the webserver. The Custom Search server is down.");
					thereIsNextPage = false;
					break;

				case 400:
					//if there is term spelling problem (extra special characters)...
					System.out.println("The search term has not been found.");
					thereIsNextPage = false;
					break;
				case 403:
					//if the resquests daily limit has been reached...
					System.out.println("I am Sorry! You have reached the daily limit for searches.");
					System.out.println("Please, try again tomorrow for more results.");
					thereIsNextPage = false;
					break;
				}

			} catch (JSONException e) {
				//when all the results has been found...
				thereIsNextPage = false;
			} catch (UnknownHostException e) {
				//if there is an Internet connection problem...
				System.out
						.println("It has not been possible to connect to the webserver.");
				thereIsNextPage = false;
			}
		}

		return responseArray;

	}

}
