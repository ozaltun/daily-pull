""" This document serves as a location for helper functions in pursuit of trying
to pull data from different APIs.

"""
import musicbrainzngs as musicB
from bs4 import BeautifulSoup as bs
import requests
import re
import json
import os
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

def get_MusicBrainzDirty(id= None, ArtistName= None):
    """ This is code to get social media websites from Music Brainz.
    I had to brute force myself to getting it. If you have a better method
    (especially skipping the substring search), please implement. I didn't
    want to spend a lot of time on figuring out BeautifulSoup.


    """

    if (id== None and ArtistName == None):
        return 'You need to either provide an id number or ArtistName'
    elif (id== None):
        #Pull data from MusicBrainz API
        musicB.set_useragent("mySocialMediaPageExtractor", "Version 1",
                                "ozaltun@mit.edu")
        searchResults= musicB.search_artists(artist=ArtistName)
        artistProfile= searchResults['artist-list'][0]
        score= artistProfile['ext:score']
        if int(score)<100:
            print('This is not an exact string match')
            print('You searched: ',ArtistName,', but the search found',
                    artistProfile['name'])
        artistID= artistProfile['id']
    else:
        artistID= id

    url= 'https://musicbrainz.org/artist/'+artistID
    r= requests.get(url)
    data= requests.text
    soup= bs(data)
    linkList = list([str(link.get('href')) for link in soup.find_all('a')])
    subStringList = ['facebook', 'youtube', 'twitter', 'instagram', 'wikipedia',
    'spotify', 'itunes']
    results = dict()
    for sub in subStringList:
        results[sub]=[]
    for s in linkList:
        [results.update({sub: results[sub]+[s]}) for sub in subStringList if sub in s]
    return ArtistName, artistID, results

def get_MusicBrainz(id= None, ArtistName= None):
    ArtistName, artistID, artistLinks = get_MusicBrainzDirty(id, ArtistName)
    artistKeys = dict()
    for key, value in artistLinks.items():
        for i in range(len(value)):
            subString = re.findall('[^/]*$', value[i])[0]
            value[i] = subString
        artistKeys.update({key: value})
    return ArtistName, artistID, artistKeys


def addArtist2JSON(id, ArtistName):
    ArtistName, artistID, artistKeys= get_MusicBrainz(id, ArtistName)
    artistList = {artistID: artistKeys}
    artist2ID = {ArtistName: artistID}

    try:
        with open('todos/artistID.json', mode='r') as feedsjson:
            feeds = json.load(feedsjson)

    except ValueError:
        with open('todos/artistID.json', mode='w') as feedsjson:
            json.dump(dict(), feedsjson)
        with open('todos/artistID.json', mode='r') as feedsjson:
            feeds = json.load(feedsjson)
    with open('todos/artistID.json', mode='w') as feedsjson:
        feeds.update(artist2ID)
        json.dump(feeds, feedsjson)

    try:
        with open('todos/artistList.json', mode='r') as feedsjson:
            feeds = json.load(feedsjson)
    except ValueError:
        with open('todos/artistList.json', mode='w') as feedsjson:
            json.dump(dict(), feedsjson)
        with open('todos/artistList.json', mode='r') as feedsjson:
            feeds = json.load(feedsjson)
    with open('todos/artistList.json', mode='w') as feedsjson:
        feeds.update(artistList)
        json.dump(feeds, feedsjson)


def removeArtistFromJSON(id, ArtistName):
    try:
        with open('todos/artistID.json', mode='r') as feedsjson:
            feeds = json.load(feedsjson)
    except ValueError:
        with open('todos/artistID.json', mode='w') as feedsjson:
            json.dump(dict(), feedsjson)
        with open('todos/artistID.json', mode='r') as feedsjson:
            feeds = json.load(feedsjson)
    with open('todos/artistID.json', mode='w') as feedsjson:
        if ArtistName in feeds:
            artistID = feeds[ArtistName]
        else:
            return
        del feeds[ArtistName]
        json.dump(feeds, feedsjson)

    try:
        with open('todos/artistList.json', mode='r') as feedsjson:
            feeds = json.load(feedsjson)
    except ValueError:
        with open('todos/artistList.json', mode='w') as feedsjson:
            json.dump(dict(), feedsjson)
        with open('todos/artistList.json', mode='r') as feedsjson:
            feeds = json.load(feedsjson)
    with open('todos/artistList.json', mode='w') as feedsjson:
        del feeds[artistID]
        json.dump(feeds, feedsjson)
