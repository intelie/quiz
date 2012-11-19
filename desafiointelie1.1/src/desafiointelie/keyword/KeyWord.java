
package desafiointelie.keyword;

/**
 *
 * @author Gabriel Salvatti
 */
public class KeyWord {
    
    public KeyWord(String text){
        this.text = text;
    }
    
    private String text;

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }
    
    //Changes some special characters into the Google Search's patterns
    public String toHHTP(){
        String hTTPText = this.text;
        hTTPText = hTTPText.replaceAll(" ", "+");
        hTTPText = hTTPText.replaceAll("%", "%25");
        hTTPText = hTTPText.replaceAll("@", "%40");
        hTTPText = hTTPText.replaceAll("#", "%23");
        hTTPText = hTTPText.replaceAll("&", "%26");
        hTTPText = hTTPText.replaceAll("/", "%2F");
        hTTPText = hTTPText.replaceAll("}", "%7D");
        hTTPText = hTTPText.replaceAll("]", "%5D");
        hTTPText = hTTPText.replaceAll(";", "%3B");
        hTTPText = hTTPText.replaceAll("ª", "%AA");
        hTTPText = hTTPText.replaceAll("º", "%BA");
        hTTPText = hTTPText.replaceAll("\\$", "%24");
        hTTPText = hTTPText.replaceAll("\\[", "%5B");
        hTTPText = hTTPText.replaceAll("\\{", "%7B");
        hTTPText = hTTPText.replaceAll("\\?", "%3F");
        
        return hTTPText;
    }
    
}
