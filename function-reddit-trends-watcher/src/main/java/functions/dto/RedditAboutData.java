package functions.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonIgnoreProperties( ignoreUnknown = true )
public class RedditAboutData {

    @JsonProperty( "data" )
    private AboutDataBean data;

    // Getters and setters
    public AboutDataBean getData() {
        return data;
    }

    public void setData( AboutDataBean data ) {
        this.data = data;
    }


}

