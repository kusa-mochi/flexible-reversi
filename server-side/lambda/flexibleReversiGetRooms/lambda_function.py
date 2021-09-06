# summary:
# 1. read reversi rooms data from dynamodb.
# 2. send data to all WebSocket clients.

import boto3
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
import json

dynamodb = boto3.resource('dynamodb')
connections = dynamodb.Table('flexible-reversi-tokens')
appData = dynamodb.Table('flexible-reversi')

def rooms_default_dumps(obj):
    if isinstance(obj, Decimal):
        return int(obj)
    raise TypeError

def send_data(sendProperties):
    try:
        print(sendProperties['data'])
        am = boto3.client('apigatewaymanagementapi', endpoint_url=sendProperties['url'])
        print('sending..')
        _ = am.post_to_connection(ConnectionId=sendProperties['connectionId'], Data=sendProperties['data'])
    except:
        pass

def lambda_handler(event, context):
    print("getRooms start.")
    print(event)
    
    # check a token from a client.
    postData = json.loads(event.get('body', '{}')).get('data')
    token = postData['token']
    print(postData)
    connection = connections.get_item(Key={'token': token})
    print(connection)
    # if a token is not exist on DB
    if token != connection['Item']['token']:
        return {
            'statusCode': 404,
            'body': json.dumps('access denied.')
        }
    
    # WebSocket ID
    connectionId = event.get('requestContext', {}).get('connectionId')
    print('websocket id:')
    print(connectionId)
    
    # update WebSocket ID on DB.
    exp = "set connectionId=:connectionId"
    result = connections.update_item(
        Key={'token': token},
        UpdateExpression=exp,
        ExpressionAttributeValues={
            ':connectionId': connectionId
        },
        ReturnValues='UPDATED_NEW'
    )

    # get rooms data from dynamodb
    rooms = appData.scan().get('Items')
    for room in rooms:
        del room['boardLogs']
        del room['currentBoard']
        del room['currentPlayer']
        del room['entryPassword']
        del room['opponentId']
        del room['roomAuthorId']
        del room['thinkingCounter']
    ret = json.dumps({"dataType":"getRooms", "data":{"rooms":rooms}}, default=rooms_default_dumps)
    
    print('transaction settings start.')
    connectionTable = connections.scan().get('Items')
    if connectionTable is None:
        return { 'statusCode': 500, 'body': 'something went wrong' }
    
    print("transactions start.")
    with ThreadPoolExecutor(max_workers=10, thread_name_prefix="thread") as executor:
        for item in connectionTable:
            executor.submit(
                send_data,
                {
                    'url': item['endpointUrl'],
                    'connectionId': item['connectionId'],
                    'data': ret
                }
            )
    
    return {
        'statusCode': 200,
        'body': json.dumps('getrooms fin.')
    }
