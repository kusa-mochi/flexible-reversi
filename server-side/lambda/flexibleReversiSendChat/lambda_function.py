import boto3
import datetime
import json

dynamodb = boto3.resource('dynamodb')
connections = dynamodb.Table('flexible-reversi-tokens')
appData = dynamodb.Table('flexible-reversi')
chatData = dynamodb.Table('flexible-reversi-chat-logs')

def lambda_handler(event, context):
    print("sendChat start.")
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
    
    # room id
    roomId = postData['roomId']
    
    # room data
    roomData = appData.get_item(Key={'id': roomId})['Item']
    
    # room author token
    roomAuthorToken = roomData['roomAuthorId']
    # opponent token
    opponentToken = roomData['opponentId']
    
    if roomAuthorToken == '':
        return {
            'statusCode': 200,
            'body': json.dumps('the room is already reset.')
        }
    
    if token != roomAuthorToken and token != opponentToken:
        return {
            'statusCode': 200,
            'body': json.dumps('the token is not registered to the room #' + roomId + '.')
        }
    
    # room author connection
    roomAuthorConnection = connections.get_item(Key={'token': roomAuthorToken})
    # opponent connection
    opponentConnection = connections.get_item(Key={'token': opponentToken})
    
    # room author endpoint url
    roomAuthorUrl = roomAuthorConnection['Item']['endpointUrl']
    # opponent endpoint url
    opponentUrl = opponentConnection['Item']['endpointUrl']
    
    # room author connection id
    roomAuthorConnectionId = roomAuthorConnection['Item']['connectionId']
    # opponent connection id
    opponentConnectionId = opponentConnection['Item']['connectionId']
    
    # sender's nickname
    senderNickname = connections.get_item(Key={'token': token})['Item']['nickname']
    
    # message to send
    messageToSend = postData['message']
    
    ret = json.dumps({
        'dataType': 'sendChat',
        'data': {
            'nickname': senderNickname,
            'message': messageToSend
        }
    })
    
    # send chat message to both of room users.
    am = boto3.client('apigatewaymanagementapi', endpoint_url=roomAuthorUrl)
    _ = am.post_to_connection(ConnectionId=roomAuthorConnectionId, Data=ret)
    am = boto3.client('apigatewaymanagementapi', endpoint_url=opponentUrl)
    _ = am.post_to_connection(ConnectionId=opponentConnectionId, Data=ret)
    
    # timestamp
    now = datetime.datetime.now()
    timestamp = str(int(now.timestamp()))
    print(timestamp)
    
    # save nickname and message to the DB.
    response = chatData.put_item(Item={
        'timestamp': timestamp,
        'roomId': roomId,
        'nickname': senderNickname,
        'message': messageToSend
    })
    print(response)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
