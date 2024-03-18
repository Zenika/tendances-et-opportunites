package functions.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneId;
import java.util.List;

@JsonIgnoreProperties( ignoreUnknown = true )
public class RedditMessagesData {

    @JsonProperty( "data" )
    private Data data;

    // Getters and setters
    public Data getData() {
        return data;
    }

    public void setData( Data data ) {
        this.data = data;
    }

    @JsonIgnoreProperties( ignoreUnknown = true )
    public static class Data {

        @JsonProperty( "children" )
        private List<Child> children;

        // Getters and setters
        public List<Child> getChildren() {
            return children;
        }

        public void setChildren( List<Child> children ) {
            this.children = children;
        }
    }

    @JsonIgnoreProperties( ignoreUnknown = true )
    public static class Child {

        @JsonProperty( "data" )
        private ChildData data;

        // Getters and setters
        public ChildData getData() {
            return data;
        }

        public void setData( ChildData data ) {
            this.data = data;
        }


    }

    @JsonIgnoreProperties( ignoreUnknown = true )
    public static class ChildData {

        @JsonProperty( "subreddit" )
        private String subreddit;

        @JsonProperty( "created" )
        private String created;

        // Getters and setters
        public String getSubreddit() {
            return subreddit;
        }

        public void setSubreddit( String subreddit ) {
            this.subreddit = subreddit;
        }

        public LocalDate getCreated() {
            return timestampToLocalDate( created );
        }

        public void setCreated( String created ) {
            this.created = created;
        }

        @Override
        public String toString() {
            return "ChildData{" +
                    "subreddit='" + subreddit + '\'' +
                    ", created=" + getCreated() +
                    '}';
        }
    }

    public static LocalDate timestampToLocalDate( String timestampString ) {
        // Convert the String timestamp to a double, then to milliseconds
        long milliseconds = ( long ) (Double.parseDouble( timestampString ) * 1000);

        // Create an Instant object from the timestamp
        Instant instant = Instant.ofEpochMilli( milliseconds );

        // Convert the Instant to LocalDate
        return  instant.atZone( ZoneId.systemDefault() )
                                .toLocalDate();

    }
}
