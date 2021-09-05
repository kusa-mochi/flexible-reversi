import boto3
import json

dynamodb = boto3.resource('dynamodb')
connections = dynamodb.Table('flexible-reversi-tokens')
appData = dynamodb.Table('flexible-reversi')

def lambda_handler(event, context):
    print("exitRoom start.")
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
            'body': json.dumps('the room is already reset.')
        }
    
    # room author connection
    roomAuthorConnection = connections.get_item(Key={'token': roomAuthorToken})
    
    # room author connection id
    roomAuthorConnectionId = roomAuthorConnection['Item']['connectionId']
    
    # reset the room
    sendData = "{\"data\":{\"token\":\"" + roomAuthorToken + "\","
    sendData += "\"id\":" + str(roomId) + ","
    sendData += "\"boardLogs\":[],"
    sendData += "\"canView\":false,"
    sendData += "\"currentBoard\":[],"
    sendData += "\"currentPlayer\":true,"
    sendData += "\"entryPassword\":\"\","
    sendData += "\"firstPlayer\":true,"
    sendData += "\"requireEntryPassword\":false,"
    sendData += "\"roomName\":\"\","
    sendData += "\"roomState\":\"vacancy\","
    sendData += "\"thinkingCounter\":0,"
    sendData += "\"opponentId\":\"4dc4a59af1a341ee468607550985aa4a23437d5061c365f341aad92b09176035\","
    sendData += "\"opponentName\":\"\","
    sendData += "\"roomAuthorId\":\"4dc4a59af1a341ee468607550985aa4a23437d5061c365f341aad92b09176035\","
    sendData += "\"roomAuthor\":\"\""
    sendData += "}}"
    response = boto3.client('lambda').invoke(
        FunctionName='arn:aws:lambda:ap-northeast-1:280196608156:function:flexibleReversiUpdateRoom',
        InvocationType='Event',
        Payload=json.dumps({'body':sendData, 'requestContext':{'connectionId':roomAuthorConnectionId}})
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('exitRoom fin.')
    }
