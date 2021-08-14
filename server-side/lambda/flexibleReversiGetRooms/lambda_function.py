import boto3
import json

dynamodb = boto3.resource('dynamodb')
connections = dynamodb.Table('flexible-reversi-connections')
appData = dynamodb.Table('flexible-reversi')

def lambda_handler(event, context):
    # get rooms data from dynamodb
    # rooms = appData.scan().get('Items')

    domain_name = event.get('requestContext',{}).get('domainName')
    stage       = event.get('requestContext',{}).get('stage')
    items = connections.scan(ProjectionExpression='id').get('Items')

    if items is None:
        return { 'statusCode': 500, 'body': 'something went wrong' }
    apigw_management = boto3.client('apigatewaymanagementapi', endpoint_url=F"https://{domain_name}/{stage}")
    for item in items:
        try:
            print(item)
            _ = apigw_management.post_to_connection(ConnectionId=item['id'], Data=json.dumps({"mochi":1234}))
        except:
            pass
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
