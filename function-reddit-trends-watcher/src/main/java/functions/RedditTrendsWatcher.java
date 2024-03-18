package functions;

import com.google.cloud.functions.HttpFunction;
import com.google.cloud.functions.HttpRequest;
import com.google.cloud.functions.HttpResponse;
import functions.dto.RedditAboutData;
import functions.dto.RedditMessagesData;
import functions.dto.RedditToken;

import java.io.BufferedWriter;
import java.io.IOException;
import java.net.URISyntaxException;
import java.time.LocalDate;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static functions.HttpRequestUtil.sendHttpRequest;

public class RedditTrendsWatcher implements HttpFunction {

    private static final String       USER_AGENT = "ChangeMeClient/0.1 by YourUsername";
    private static final String       TOKEN_URL  = "https://www.reddit.com/api/v1/access_token";
    private static final String       AUTH_KEY   = "Basic X19kY0xESHZyM1Rkb2VxSkh6UWpuUTpTTVpZaTVSUHF4QWVlMDRKNEhKcGZyRGRfUUhxNEE=";
    private static final List<String> TOPICS     = List.of( "java", "javascript", "Python", "csharp" );

    @Override
    public void service( HttpRequest request, HttpResponse response ) {
        try {
            RedditToken redditToken = getRedditToken();
            String output = getTopicsInfo( redditToken );
            writeResponse( response, output );
        } catch ( Exception e ) {
            // Consider proper error handling here
            e.printStackTrace();
        }
    }

    private RedditToken getRedditToken() throws IOException, URISyntaxException {
        Map<String, String> tokenHeaders = new HashMap<>();
        tokenHeaders.put( "Content-Type", "application/x-www-form-urlencoded" );
        tokenHeaders.put( "Authorization", AUTH_KEY );

        Map<String, String> formData = new HashMap<>();
        formData.put( "grant_type", "password" );
        formData.put( "username", "Zreddit59" );
        formData.put( "password", "askVV" );

        return sendHttpRequest( TOKEN_URL, tokenHeaders, formData, RedditToken.class, "POST" );
    }

    private String getTopicsInfo( RedditToken redditToken ) throws IOException, URISyntaxException {
        StringBuilder output = new StringBuilder();
        for ( String topic : TOPICS ) {
            String messagesUrl = "https://oauth.reddit.com/r/" + topic + "/new?limit=100";
            String aboutUrl = "https://oauth.reddit.com/r/" + topic + "/about";
            Map<String, String> headers = Map.of( "User-Agent", USER_AGENT, "Authorization", "bearer " + redditToken.getToken() );

            RedditMessagesData messageResponse = sendHttpRequest( messagesUrl, headers, null, RedditMessagesData.class, "GET" );
            long messagesCount = messageResponse.getData()
                                                .getChildren()
                                                .stream()
                                                .map( RedditMessagesData.Child::getData )
                                                .filter( data -> data.getCreated()
                                                                     .isAfter( LocalDate.now()
                                                                                        .minusWeeks( 1 ) ) )
                                                .count();

            RedditAboutData aboutResponse = sendHttpRequest( aboutUrl, headers, null, RedditAboutData.class, "GET" );
            int subscribersCount = aboutResponse.getData()
                                                .getSubscribers();

            output.append( " | " )
                  .append( topic )
                  .append( " messages=[" )
                  .append( messagesCount )
                  .append( "] subscribers=[" )
                  .append( subscribersCount )
                  .append( "]\n" );
        }
        return output.toString();
    }

    private void writeResponse( HttpResponse response, String output ) throws IOException {
        BufferedWriter writer = response.getWriter();
        writer.write( output );
    }

}