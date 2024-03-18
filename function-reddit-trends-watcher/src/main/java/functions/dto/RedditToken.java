package functions.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonIgnoreProperties( ignoreUnknown = true )
public class RedditToken {

    @JsonProperty( "access_token" )
    private String token;

    // Getters and setters
    public String getToken() {
        return token;
    }

    public void setToken( final String token ) {
        this.token = token;
    }
}

