# daily-pull

This repository can be summed up to having two functions:
1. Static functions that given an Artist Name searches and scrapes MusicBrainz for social media links.
2. A dynamic AWS function that connects to Spotify everyday and pulls data. It saves that data to a DynamoDB table.

Credentials needs to be put in place by the user. I used a ".env" file to initialize credentials as environment variables.
