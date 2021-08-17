import boto3
import json

dynamodb = boto3.resource('dynamodb')
appData = dynamodb.Table('flexible-reversi')

def lambda_handler(event, context):
    print(event['data'])
    
    # get room id
    roomId = event['data']['id']
    
    # check room state
    rooms = appData.scan().get('Items')
    targetRoom = list(filter(lambda room: room['id'] == roomId, rooms))[0]
    roomStateFrom = targetRoom['roomState']
    roomStateTo = event['data']['roomState']
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
    
    # update room properties
    exp = 'set '
    exp += 'boardLogs=:boardLogs,'
    exp += 'canView=:canView,'
    exp += 'currentBoard=:currentBoard,'
    exp += 'currentPlayer=:currentPlayer,'
    exp += 'entryPassword=:entryPassword,'
    exp += 'firstPlayerId=:firstPlayerId,'
    exp += 'opponentId=:opponentId,'
    exp += 'opponentName=:opponentName,'
    exp += 'requireEntryPassword=:requireEntryPassword,'
    exp += 'requireViewPassword=:requireViewPassword,'
    exp += 'roomAuthor=:roomAuthor,'
    exp += 'roomName=:roomName,'
    exp += 'roomState=:roomState,'
    exp += 'thinkingCounter=:thinkingCounter,'
    exp += 'viewPassword=:viewPassword'
    result = appData.update_item(
        Key={
            'id': roomId
        },
        UpdateExpression=exp,
        ExpressionAttributeValues={
            ':boardLogs': event['data']['boardLogs'],
            ':canView': event['data']['canView'],
            ':currentBoard': event['data']['currentBoard'],
            ':currentPlayer': event['data']['currentPlayer'],
            ':entryPassword': event['data']['entryPassword'],
            ':firstPlayerId': event['data']['firstPlayerId'],
            ':opponentId': event['data']['opponentId'],
            ':opponentName': event['data']['opponentName'],
            ':requireEntryPassword': event['data']['requireEntryPassword'],
            ':requireViewPassword': event['data']['requireViewPassword'],
            ':roomAuthor': event['data']['roomAuthor'],
            ':roomName': event['data']['roomName'],
            ':roomState': roomStateTo,
            ':thinkingCounter': event['data']['thinkingCounter'],
            ':viewPassword': event['data']['viewPassword']
        },
        ReturnValues='UPDATED_NEW'
        )
    
    return {
        'statusCode': 200,
        'body': json.dumps('update room fin.')
    }
