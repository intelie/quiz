import java.io.IOException;
import java.io.UnsupportedEncodingException;

public class Teste {

	public static void main(String[] args) {
		try {
			if (args.length>0)
				PesquisaGoogle.pesquisaTermo(args[0]);
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

}
