package desafiointelie;

import desafiointelie.json.JSONArray;
import desafiointelie.json.JSONException;
import desafiointelie.keyword.KeyWord;
import desafiointelie.resources.LevenshteinDistance;
import desafiointelie.resources.SearchEngine;
import desafiointelie.website.WebSite;
import java.io.*;
import java.util.ArrayList;
import java.util.InputMismatchException;
import java.util.Scanner;

/**
 * 
 * @author Gabriel Salvatti Main Class
 */
public class Search {

	private static int answer = 0;
	private static int countTermAppeared = 0;
	private static int answerComparator = 0;
	private static ArrayList<WebSite> webSites;
	private static SearchEngine searchEngine;

	public static void main(String[] args) throws IOException, JSONException {

		webSites = new ArrayList<WebSite>();

		searchEngine = new SearchEngine();

		boolean choiceToEnd = false;
		do {
			// menu
			System.out.println("\n\n");
			System.out.println("THE INTELIE CHALLENGE - DEVELOPMENT");
			System.out.println("\n\n");
			System.out.println("1-New Search\t 2-End");
			System.out.println("\n");
			System.out.println("Inform your choice and press 'Enter': ");

			Scanner inPutMainMenu = new Scanner(System.in);
			int mainMenuOption = 0;
			try {
				mainMenuOption = inPutMainMenu.nextInt();
			} catch (InputMismatchException e) {
			}

			switch (mainMenuOption) {
			case 1:
				System.out.print("Type the term to be search: ");
				Scanner inPutTerm = new Scanner(System.in);
				String typedText = inPutTerm.nextLine();

				// tests whether the typed term is blank
				if (typedText.trim().length() > 0) {
					System.out.println("\n\nSearching...\n\n");

					KeyWord keyWord = new KeyWord(typedText);
					
					// calls the search and creates the WebSites' Array.
					JSONArray jSONArray = searchEngine
							.jsonArrayResponse(keyWord.toHHTP());
					for (int i = 0; i < jSONArray.length(); i++) {
						for (int j = 0; j < jSONArray.getJSONArray(i).length(); j++) {
							WebSite webSite = new WebSite(jSONArray
									.getJSONArray(j).getJSONObject(i));
							webSites.add(webSite);
						}
					}

					/*
					 * calls the method which counts how many times a term
					 * appears in the results.
					 */
					answer = getAnswer(typedText, webSites);

					// prints the results on the screen
					for (int i = 0; i < webSites.size(); i++) {
						System.out.println(webSites.get(i).toString());
						System.out
								.println("-------------------------------------");

					}
					
					//Report's Title
					System.out.println("\nREPORT:");
					
					// How many times does the term appear in the results?
					System.out.println("\nThe term '" + typedText
							+ "' appears " + answer
							+ " times in the found results.");
					// how many percent of results it appears?
					double percOccurrence = ((double) countTermAppeared / (double) webSites
							.size()) * 100;
					System.out.print("\nThe term '" + typedText
							+ "' appears in ");
					System.out.printf("%.2f", percOccurrence);
					System.out.print("% of the found results.");
					/*
					 * Prints the total of results and the number of titles
					 * which the term appears
					 */
					System.out.println("\n\nThe Total of Results: "
							+ webSites.size()
							+ "\tThe Titles which the term appears: "
							+ countTermAppeared);
				} else {
					System.out.println("THE TYPED TERM IS NOT VALID!");
				}

				answer = 0;
				answerComparator = 0;
				countTermAppeared = 0;
				webSites.clear();
				break;
			case 2:
				// Menu option to close the application
				choiceToEnd = true;
				break;
			// validation of the menu option
			default:
				System.out.println("\nYOU MUST CHOOSE A VALID OPTION.");
			}
			System.out.println("\n----------------------------------");
		} while (!choiceToEnd);

	}

	// counts how many times a term appears in the results.
	private static int getAnswer(String keyWord, ArrayList<WebSite> webSites) {
		keyWord = prepareString(keyWord);
		// Levenshtein Distance = 0 to terms less than or equal to 2 characters
		// long
		if (keyWord.length() <= 2) {
			for (int i = 0; i < webSites.size(); i++) {
				String webTitle = prepareString(webSites.get(i).getTitle());
				for (int j = 0; j < webTitle.length(); j++) {
					if ((j + keyWord.length()) <= webTitle.length()) {
						String webTitlePart = webTitle.substring(j,
								j + keyWord.length());
						if (keyWord.equals(webTitlePart)) {
							answer++;
						}
					}
				}
				if (answer > answerComparator) {
					countTermAppeared++;
					answerComparator = answer;
				}
			}
		}

		// Levenshtein Distance = 1 to terms from 3 to 4 characters long
		if ((keyWord.length() == 3) || (keyWord.length() == 4)) {
			for (int i = 0; i < webSites.size(); i++) {
				String webTitle = prepareString(webSites.get(i).getTitle());
				for (int j = 0; j < webTitle.length(); j++) {
					if ((j + keyWord.length()) <= webTitle.length()) {
						String webTitlePart = webTitle.substring(j,
								j + keyWord.length());
						if (LevenshteinDistance.compute(keyWord, webTitlePart) <= 1) {
							answer++;
							j += 2;
						}
					}
				}
				if (answer > answerComparator) {
					countTermAppeared++;
					answerComparator = answer;
				}
			}
		}

		// Levenshtein Distance = 2 to terms more than or equal to 5 characters
		// long
		if (keyWord.length() >= 5) {
			for (int i = 0; i < webSites.size(); i++) {
				String webTitle = prepareString(webSites.get(i).getTitle());
				for (int j = 0; j < webTitle.length(); j++) {
					if ((j + keyWord.length()) <= webTitle.length()) {
						String webTitlePart = webTitle.substring(j,
								j + keyWord.length());
						if (LevenshteinDistance.compute(keyWord, webTitlePart) <= 2) {
							answer++;
							j += 3;
						}
					}
				}
				if (answer > answerComparator) {
					countTermAppeared++;
					answerComparator = answer;
				}
			}
		}

		return answer;
	}

	// changes some special characters
	private static String prepareString(String string) {
		string = string.toLowerCase();
		string = string.replaceAll("á", "a");
		string = string.replaceAll("â", "a");
		string = string.replaceAll("ã", "a");
		string = string.replaceAll("ä", "a");
		string = string.replaceAll("é", "e");
		string = string.replaceAll("ê", "e");
		string = string.replaceAll("ë", "e");
		string = string.replaceAll("ï", "i");
		string = string.replaceAll("í", "i");
		string = string.replaceAll("ó", "o");
		string = string.replaceAll("õ", "o");
		string = string.replaceAll("ö", "o");
		string = string.replaceAll("ú", "u");
		string = string.replaceAll("ũ", "u");
		string = string.replaceAll("ü", "u");

		return string;
	}

}
