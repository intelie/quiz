
public class Levenshtein {
	
	private static int minimo (int a, int b, int c) {
		return Math.min(Math.min(a, b), c);
	}
	
	public static int calculaDistancia (String termo, String palavra) {
		
		int matriz[][] = new int[termo.length()+1][palavra.length()+1];
		int custo;
		
		for (int i = 0; i<=termo.length(); i++) {
			matriz[i][0] = i;
		}
		
		for (int i = 0; i<=palavra.length(); i++) {
			matriz[0][i] = i;
		}
		
		for (int i = 1; i<=termo.length(); i++) {
			for (int j = 1; j<=palavra.length(); j++) {
				
				if (termo.charAt(i-1) == palavra.charAt(j-1)) custo = 0;
				else custo = 2;
				
				matriz[i][j] = minimo(matriz[i-1][j]+1, matriz[i][j-1]+1, matriz[i-1][j-1]+custo);
				
			}
		}
		
		
		return matriz[termo.length()][palavra.length()];
	}
}
