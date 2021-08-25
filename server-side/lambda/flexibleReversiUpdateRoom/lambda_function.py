# summary:
# 1. get room data from the API Gateway (mostly from clients).
# 2. update room data at DynamoDB.
# 3. call the lambda "flexibleReversiGetRooms."

import boto3
import hashlib
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
    
    #print(event)
    #print(json.dumps(event))
    #print(json.loads(json.dumps(event)))
    #print(json.loads(json.dumps(event))['data']['id'])
    #postData = json.loads(json.dumps(event))['data']
    #postData = json.loads(event.get('body', '{}')).get('data')

    # get room id
    roomId = postData['id']
    print('room id : ' + str(roomId))
    
    # check room state
    print("checking room state...")
    rooms = appData.scan().get('Items')
    targetRoom = list(filter(lambda room: room['id'] == roomId, rooms))[0]
    roomStateFrom = targetRoom['roomState']
    print('from : ' + roomStateFrom)
    roomStateTo = postData['roomState']
    print('to : ' + roomStateTo)
    
    if roomStateFrom == "vacancy":
        print("vacancy")
        if roomStateTo != "inPreparation":
            raise ValueError("invalid room state by client")
    elif roomStateFrom == "inPreparation":
        print("inPreparation")
        if roomStateTo != "standby" and roomStateTo != "vacancy":
            raise ValueError("invalid room state by client")
    elif roomStateFrom == "standby":
        print("standby")
        if roomStateTo != "inGame" and roomStateTo != "vacancy":
            raise ValueError("invalid room state by client")
    elif roomStateFrom == "inGame":
        print("inGame")
        if roomStateTo != "vacancy":
            raise ValueError("invalid room state by client")
    else:
        raise ValueError("invlalid room state on DB")
    
    print("done.")
    
    print('calculating password hash...')
    entryPasswordHash = ''
    if len(postData['entryPassword']) != 0:
        entryPasswordHash = hashlib.sha256(postData['entryPassword'].encode('utf-8')).hexdigest()
    
    print('done.')
    
    # update room properties
    print('making dynamodb query...')
    exp = 'set '
    exp += 'boardLogs=:boardLogs,'
    exp += 'canView=:canView,'
    exp += 'currentBoard=:currentBoard,'
    exp += 'currentPlayer=:currentPlayer,'
    exp += 'entryPassword=:entryPassword,'
    exp += 'firstPlayer=:firstPlayer,'
    exp += 'opponentId=:opponentId,'
    exp += 'opponentName=:opponentName,'
    exp += 'requireEntryPassword=:requireEntryPassword,'
    exp += 'roomAuthor=:roomAuthor,'
    exp += 'roomName=:roomName,'
    exp += 'roomState=:roomState,'
    exp += 'thinkingCounter=:thinkingCounter'
    
    eav = {
        ':boardLogs': postData['boardLogs'],
        ':canView': postData['canView'],
        ':currentBoard': postData['currentBoard'],
        ':currentPlayer': postData['currentPlayer'],
        ':entryPassword': entryPasswordHash,
        ':firstPlayer': postData['firstPlayer'],
        ':opponentId': postData['opponentId'],
        ':opponentName': postData['opponentName'],
        ':requireEntryPassword': postData['requireEntryPassword'],
        ':roomAuthor': postData['roomAuthor'],
        ':roomName': postData['roomName'],
        ':roomState': roomStateTo,
        ':thinkingCounter': postData['thinkingCounter']
    }
    print('done.')
    
    print('updating room status...')
    result = appData.update_item(
        Key={'id': roomId},
        UpdateExpression=exp,
        ExpressionAttributeValues=eav,
        ReturnValues='UPDATED_NEW'
    )
    print('done.')
    print(postData['firstPlayer'])
    
    # 各クライアントに変更後の各部屋のを通知する。
    response = boto3.client('lambda').invoke(
        FunctionName='arn:aws:lambda:ap-northeast-1:280196608156:function:flexibleReversiGetRooms',
        InvocationType='Event',
        Payload=json.dumps({'body':"{\"data\":{\"token\":" + token + "}}"})
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('update room fin.')
    }
