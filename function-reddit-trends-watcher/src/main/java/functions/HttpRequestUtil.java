package functions;

import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.Map;

public final class HttpRequestUtil {
    private HttpRequestUtil() {
    }

    public static <T> T sendHttpRequest( String urlString, Map<String, String> headers, Map<String, String> formData, Class<T> clazz, String requestMethod ) throws
                                                                                                                                                             IOException,
                                                                                                                                                             URISyntaxException {
        HttpURLConnection connection = createConnection( urlString, requestMethod, headers );
        if ( "POST".equals( requestMethod ) ) {
            sendFormData( connection, formData );
        }
        return getResponse( connection, clazz );
    }

    private static HttpURLConnection createConnection( String urlString, String requestMethod, Map<String, String> headers ) throws
                                                                                                                             IOException,
                                                                                                                             URISyntaxException {
        URI uri = new URI( urlString );
        URL url = uri.toURL();
        HttpURLConnection connection = ( HttpURLConnection ) url.openConnection();
        connection.setRequestMethod( requestMethod );
        setRequestHeaders( connection, headers );
        return connection;
    }

    private static void setRequestHeaders( HttpURLConnection connection, Map<String, String> headers ) {
        headers.forEach( connection::setRequestProperty );
    }

    private static void sendFormData( HttpURLConnection connection, Map<String, String> formData ) throws IOException {
        connection.setDoOutput( true );
        String encodedFormData = encodeFormData( formData );
        try ( DataOutputStream outputStream = new DataOutputStream( connection.getOutputStream() ) ) {
            outputStream.writeBytes( encodedFormData );
        }
    }

    private static String encodeFormData( Map<String, String> formData ) {
        StringBuilder encodedData = new StringBuilder();
        for ( Map.Entry<String, String> entry : formData.entrySet() ) {
            if ( !encodedData.isEmpty() ) {
                encodedData.append( '&' );
            }
            encodedData.append( URLEncoder.encode( entry.getKey(), StandardCharsets.UTF_8 ) );
            encodedData.append( '=' );
            encodedData.append( URLEncoder.encode( entry.getValue(), StandardCharsets.UTF_8 ) );
        }
        return encodedData.toString();
    }

    private static <T> T getResponse( HttpURLConnection connection, Class<T> clazz ) throws IOException {
        StringBuilder responseBuilder = new StringBuilder();
        try ( BufferedReader reader = new BufferedReader( new InputStreamReader( connection.getInputStream() ) ) ) {
            reader.lines()
                  .forEach( responseBuilder::append );
        }
        return deserializeJson( responseBuilder.toString(), clazz );
    }

    private static <T> T deserializeJson( String json, Class<T> clazz ) throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        return mapper.readValue( json, clazz );
    }
}
