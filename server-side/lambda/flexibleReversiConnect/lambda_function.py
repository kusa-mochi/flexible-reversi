import boto3
import json

dynamodb = boto3.resource('dynamodb')
connections = dynamodb.Table('flexible-reversi-connections')

def lambda_handler(event, context):
    connection_id = event.get('requestContext', {}).get('connectionId')
    domainName = event.get('requestContext',{}).get('domainName')
    stage       = event.get('requestContext',{}).get('stage')
    
    endpointUrl = F"https://{domainName}/{stage}"
    result = connections.put_item(Item={'id': connection_id, 'endpointUrl': endpointUrl})
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
