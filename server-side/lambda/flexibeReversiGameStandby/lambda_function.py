import boto3
import json

dynamodb = boto3.resource('dynamodb')
connections = dynamodb.Table('flexible-reversi-tokens')
appData = dynamodb.Table('flexible-reversi')

def rooms_default_dumps(obj):
    if isinstance(obj, Decimal):
        return int(obj)
    raise TypeError

def lambda_handler(event, context):
    print("game start.")
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
    
    # room id
    roomId = postData['roomId']
    
    # room data
    roomData = appData.get_item(Key={'id': roomId})['Item']
    
    # room author's token
    authorToken = roomData['roomAuthorId']
    
    # opponent's token
    opponentToken = roomData['opponentId']
    
    # if two players are in a same room
    if authorToken != '' and opponentToken != '':
        # room author connection
        roomAuthorConnection = connections.get_item(Key={'token': authorToken})['Item']
        # room author url
        roomAuthorUrl = roomAuthorConnection['endpointUrl']
        # room author connection id
        roomAuthorConnectionId = roomAuthorConnection['connectionId']
        # room author nickname
        roomAuthorNickname = roomAuthorConnection['nickname']
        
        # opponent connection
        opponentConnection = connections.get_item(Key={'token': opponentToken})['Item']
        # opponent url
        opponentUrl = opponentConnection['endpointUrl']
        # opponent connection id
        opponentConnectionId = opponentConnection['connectionId']
        # room author nickname
        opponentNickname = opponentConnection['nickname']
        
        # return data to room author
        retToAuthor = json.dumps({'dataType':'gameStandby', 'data': {'opponentName': opponentNickname}}, default=rooms_default_dumps)
        # return data to opponent
        retToOpponent = json.dumps({'dataType':'gameStandby', 'data': {'opponentName': roomAuthorNickname}}, default=rooms_default_dumps)
        
        # "start game" signal to players.
        am = boto3.client('apigatewaymanagementapi', endpoint_url=roomAuthorUrl)
        _ = am.post_to_connection(ConnectionId=roomAuthorConnectionId, Data=retToAuthor)
        
        am = boto3.client('apigatewaymanagementapi', endpoint_url=opponentUrl)
        _ = am.post_to_connection(ConnectionId=opponentConnectionId, Data=retToOpponent)
    
    return {
        'statusCode': 200,
        'body': json.dumps('game standby.')
    }
