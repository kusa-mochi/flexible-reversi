import boto3
from decimal import Decimal
import json

dynamodb = boto3.resource('dynamodb')
connections = dynamodb.Table('flexible-reversi-connections')
appData = dynamodb.Table('flexible-reversi')

def rooms_default_dumps(obj):
    if isinstance(obj, Decimal):
        return int(obj)
    raise TypeError

def lambda_handler(event, context):
    print("handler start.")
    # get rooms data from dynamodb
    rooms = appData.scan().get('Items')
    ret = json.dumps({"dataType":"getRooms", "data":{"rooms":rooms}}, default=rooms_default_dumps)
    
    print('transaction settings start.')
    connectionTable = connections.scan().get('Items')
    if connectionTable is None:
        return { 'statusCode': 500, 'body': 'something went wrong' }
    
    print("transactions start.")
    for item in connectionTable:
        try:
            print(item)
            am = boto3.client('apigatewaymanagementapi', endpoint_url=item['endpointUrl'])
            _ = am.post_to_connection(ConnectionId=item['id'], Data=ret)
        except:
            pass
    return {
        'statusCode': 200,
        'body': json.dumps('getrooms fin.')
    }
