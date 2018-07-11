"""

MANY WAYS THAT THIS SHOULD BE IMPROVED:
- TRY TO TURN IT INTO A PACKAGE OF SORTS
    - WHERE ADDING MORE SERVICES SHOULD BE EASY TO HANDLE (BY JUST ADDING A NEW FUNCTION/CLASS)
- TAKE OUT CREDENTIALS FROM THE SYSTEM, TOO MANY APP CREDENTIALS ARE USED
- FIND BETTER WAY TO STORE ARTIST ID AND SOCIAL MEDIA ID'S.
    - MAYBE ANOTHER BUCKET OR DYNAMODB TABLE

"""

import json
import logging
import boto3
from artist import *
from search import *
dynamodb = boto3.resource('dynamodb')

def daily(event, context):
    data = getDailyData('Major Lazer')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    item = data

    table.put_item(Item=item)

    response = {
            "statusCode": 200,
            "body": json.dumps(item)
    }
    return response


def addArtist(artistName,id=None):
    addArtist2JSON(artistName)


def removeArtist(artistName, id=None):
    removeArtistFromJSON(artistName)

# if __name__ == '__main__':
#     print(addArtist(artistName='Maroon 5'))
# def create(event, context):
#     data = getDailyData('Major Lazer')
#     print(getDailyData('Major Lazer'))
#
# if __name__ == '__main__':
#     print(create('',''))
