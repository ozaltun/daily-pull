"""

MANY WAYS THAT THIS SHOULD BE IMPROVED:
- FIND BETTER WAY TO STORE ARTIST ID AND SOCIAL MEDIA ID'S.
    - MAYBE ANOTHER BUCKET OR DYNAMODB TABLE

"""

import json
import logging
import boto3
from todos.artist import *
from todos.search import * #Instead of importing, you should try to create an object that basically points to the helper file location
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

if __name__ == '__main__':
    print(addArtist(artistName='Maroon 5'))
def create(event, context):
    data = getDailyData('Major Lazer')
    print(getDailyData('Major Lazer'))

if __name__ == '__main__':
    print(create('',''))
