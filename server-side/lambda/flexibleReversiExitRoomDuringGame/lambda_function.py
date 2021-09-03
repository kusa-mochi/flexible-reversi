import boto3
import json

dynamodb = boto3.resource('dynamodb')
connections = dynamodb.Table('flexible-reversi-tokens')
appData = dynamodb.Table('flexible-reversi')

def lambda_handler(event, context):
    print("updateRoom start.")
    
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
    print('room id : ' + str(roomId))
    
    # room data
    roomData = appData.get_item(Key={'id': roomId})['Item']
    
    # room author's token
    authorToken = roomData['roomAuthorId']
    
    # room author connection
    roomAuthorConnection = connections.get_item(Key={'token': authorToken})['Item']
    
    # room author url
    roomAuthorUrl = roomAuthorConnection['endpointUrl']
    
    # room author connection id
    roomAuthorConnectionId = roomAuthorConnection['connectionId']
    
    # opponent's token
    opponentToken = roomData['opponentId']
    
    # opponent connection
    opponentConnection = connections.get_item(Key={'token': opponentToken})['Item']
    
    # opponent url
    opponentUrl = opponentConnection['endpointUrl']
    
    # opponent connection id
    opponentConnectionId = opponentConnection['connectionId']
    
    # which player is to exit. (True=room author, False=opponent)
    endpointUrl = ''
    connectionId = ''
    if token == authorToken:
        endpointUrl = opponentUrl
        connectionId = opponentConnectionId
    else:
        if token == opponentToken:
            endpointUrl = roomAuthorUrl
            connectionId = roomAuthorConnectionId
        else:
            # nothing to do
            return
    
    # game is set.
    
    # return raw values
    ret = {
        'dataType': 'exitRoomDuringGame',
        'data': {
            'message': 'the opponent player was exited.'
        }
    }
    
    am = boto3.client('apigatewaymanagementapi', endpoint_url=endpointUrl)
    _ = am.post_to_connection(ConnectionId=connectionId, Data=json.dumps(ret))

    return {
        'statusCode': 200,
        'body': json.dumps('flexibleReversiExitRoomDuringGame fin.')
    }
