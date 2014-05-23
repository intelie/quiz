
package desafiointelie.website;

import desafiointelie.json.JSONException;
import desafiointelie.json.JSONObject;


/**
 *
 * @author Gabriel Salvatti
 */
public class WebSite {
    
    public WebSite(){
        
    }
    
    public WebSite(JSONObject jsonObject) throws JSONException{
        this.title = jsonObject.get("title").toString();
        this.url = jsonObject.get("link").toString();
        
    }
    
    private String url;
    private String title;


    public String getTitle() {
        return title;
    }

    public String getUrl() {
        return url;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    @Override
    public String toString() {
        StringBuilder builder = new StringBuilder();
        builder.append(this.title);
        builder.append("\n");
        builder.append(this.url);
        return builder.toString();
    }
    
    
    
}
