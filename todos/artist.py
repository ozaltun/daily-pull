""" Given an artist that exists in the artistID and artistList files, this
class and functions pull data from APIs. At the moment it is limited to Spotify's
API, but can be expandedself.

We set the environment variables in aws ssm using the terminal command:
aws ssm put-parameter --name supermanToken --type String --value mySupermanToken
"""

import requests
import re
import json
import os
import datetime
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

SPOTIFY_CLIENT_ID= os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET= os.getenv('SPOTIFY_CLIENT_SECRET')

class spotifyArtist:
    def __init__(self, id, token):
        self.id = id
        self.token = token
        self.dict = dict()
        self.header = {'Authorization': '{} {}'.format(
                token['token_type'], token['access_token'])}

    def getArtistGeneral(self):
        url= 'https://api.spotify.com/v1/artists/{id}'.format(id= self.id)
        requestResponse= requests.get(url, headers=self.header)
        if (requestResponse.status_code== 200):
            self.dict['artistGeneral']= requestResponse.json()
        else:
            print(requestResponse.status_code)

    def getArtistAlbums(self, param= None):
        # The parameters for this GET request are optional. Find documentation on:
        # https://developer.spotify.com/documentation/web-api/reference/artists/get-artists-albums/

        url = 'https://api.spotify.com/v1/artists/{id}/albums'.format(id= self.id)
        if param == None:
            requestResponse= requests.get(url, headers=self.header)
            if (requestResponse.status_code== 200):
                self.dict['artistAlbums']= requestResponse.json()
            else:
                print(requestResponse.status_code)
        else:
            requestResponse= requests.get(url, params=param, headers=self.header)
            if (requestResponse.status_code== 200):
                self.dict['artistAlbums']= requestResponse.json()
            else:
                print(requestResponse.status_code)

    def getArtistTopTracks(self, countryISO):
        url= 'https://api.spotify.com/v1/artists/{id}/top-tracks'.format(id= self.id)
        country= {'country': countryISO}
        requestResponse= requests.get(url, params=country, headers=self.header)
        if (requestResponse.status_code== 200):
            self.dict['artistTopTracks']= requestResponse.json()
        else:
            print('Yikes, this isn\'t working:')
            print(url)
            print(country)
            print(self.header)
            print(requestResponse.status_code)

    def getArtistRelatedArtists(self):
        url = 'https://api.spotify.com/v1/artists/{id}/related-artists'.format(id= self.id)
        requestResponse= requests.get(url, headers=self.header)
        if (requestResponse.status_code== 200):
            self.dict['artistRelatedArtist']= requestResponse.json()
        else:
            print(requestResponse.status_code)


def getSpotifyIDToken(artistName):
    with open('data/artistList.json','r') as fp:
        artistList = json.load(fp)
    with open('data/artistID.json','r') as fp:
        artistID = json.load(fp)

    artistIDs = artistList[artistID[artistName]]
    artistSpotifyID = artistIDs['spotify'][0]

    client = BackendApplicationClient(client_id=SPOTIFY_CLIENT_ID)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url='https://accounts.spotify.com/api/token',
    client_id=SPOTIFY_CLIENT_ID,client_secret=SPOTIFY_CLIENT_SECRET)

    return artistSpotifyID, token



def getDailyData(artistList):
    # Lets now assume that artistList contains a list of artist names!
    finalList = []
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M")
    for artistName in artistList:
        artistSpotifyID, token = getSpotifyIDToken(artistName)
        artistObject = spotifyArtist(artistSpotifyID, token)
        artistObject.getArtistGeneral()
        popularity = artistObject.dict['artistGeneral']['popularity']
        followers = artistObject.dict['artistGeneral']['followers']['total']
        finalList.append({'Date':now, 'Artist': artistName, 'Spotify Popularity': popularity, 'Spotify Followers': followers})

    return finalList
