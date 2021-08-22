import boto3
import datetime
import json

dynamodb = boto3.resource('dynamodb')
connections = dynamodb.Table('flexible-reversi-connections')

def lambda_handler(event, context):
    connectionId = event.get('requestContext', {}).get('connectionId')
    domainName = event.get('requestContext',{}).get('domainName')
    stage       = event.get('requestContext',{}).get('stage')
    
    endpointUrl = F"https://{domainName}/{stage}"
    expirationDatetime = datetime.datetime.now() + datetime.timedelta(days=2)
    result = connections.put_item(
        Item={
            'id': connectionId,
            'endpointUrl': endpointUrl,
            'expirationDatetime': int(expirationDatetime.timestamp())
        }
    )
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
