import boto3
import decimal
import json

dynamodb = boto3.resource('dynamodb')
connections = dynamodb.Table('flexible-reversi-connections')
appData = dynamodb.Table('flexible-reversi')

#def decimal_default_proc(obj):
#    if isinstance(obj, Decimal):
#        return float(obj)
#    raise TypeError

def lambda_handler(event, context):
    # get rooms data from dynamodb
    rooms = appData.scan().get('Items')
    ret = '{"rooms":['
    #print(json.dumps(rooms[0]['currentBoard'], default=decimal_default_proc))
    
    for room in rooms:
        ret += '{'
        
        # board logs ->
        ret += '"boardLogs":['
        if len(room['boardLogs']) > 0:
            for board in room['boardLogs']:
                ret += '['
                for row in board:
                    ret += '['
                    for val in row:
                        ret += str(val) + ','
                    ret = ret[:-1] + '],'
                ret = ret[:-1] + '],'
            ret = ret[:-1] + '],'
        else:
            ret += '],'
        # <- board logs
        
        # can view ->
        ret += '"canView":' + str(room['canView']).lower() + ','
        # <- can view
        
        # current board ->
        ret += '"currentBoard":['
        if len(room['currentBoard']) > 0:
            for row in room['currentBoard']:
                ret += '['
                for val in row:
                    ret += str(val) + ','
                ret = ret[:-1] + '],'
            ret = ret[:-1] + '],'
        else:
            ret += '],'
        # <- current board
        
        # current player ->
        ret += '"currentPlayer":' + str(room['currentPlayer']).lower() + ','
        # <- current player
        
        # entry password ->
        ret += '"entryPassword":"' + room['entryPassword'] + '",'
        # <- entry password
        
        # first player id ->
        ret += '"firstPlayerId":' + str(room['firstPlayer']).lower() + ','
        # <- first player id
        
        # id ->
        ret += '"id":' + str(room['id']) + ','
        # <- id
        
        # opponent id ->
        ret += '"opponentId":"' + room['opponentId'] + '",'
        # <- opponent id
        
        # opponent name ->
        ret += '"opponentName":"' + room['opponentName'] + '",'
        # <- opponent name
        
        # require entry password ->
        ret += '"requireEntryPassword":' + str(room['requireEntryPassword']).lower() + ','
        # <- require entry password
        
        # require view password ->
        ret += '"requireViewPassword":' + str(room['requireViewPassword']).lower() + ','
        # <- require view password
        
        # room author ->
        ret += '"roomAuthor":"' + room['roomAuthor'] + '",'
        # <- room author
        
        # room author id ->
        ret += '"roomAuthorId":"' + room['roomAuthorId'] + '",'
        # <- room author id
        
        # room name ->
        ret += '"roomName":"' + room['roomName'] + '",'
        # <- room name
        
        # room state ->
        ret += '"roomState":"' + room['roomState'] + '",'
        # <- room state
        
        # thinking counter ->
        ret += '"thinkingCounter":' + str(room['thinkingCounter']) + ","
        # <- thinking counter
        
        # view password ->
        ret += '"viewPassword":"' + room['viewPassword'] + '",'
        # <- view password
        
        ret = ret[:-1] + '},'
    
    # remove trailing comma.
    ret = ret[:-1] + "]}"

    domain_name = event.get('requestContext',{}).get('domainName')
    stage       = event.get('requestContext',{}).get('stage')
    connection_ids = connections.scan(ProjectionExpression='id').get('Items')

    if connection_ids is None:
        return { 'statusCode': 500, 'body': 'something went wrong' }
    am = boto3.client('apigatewaymanagementapi', endpoint_url=F"https://{domain_name}/{stage}")
    for item in connection_ids:
        try:
            print(item)
            #_ = am.post_to_connection(ConnectionId=item['id'], Data=json.dumps({"rooms": 12345}))
            _ = am.post_to_connection(ConnectionId=item['id'], Data=ret)
        except:
            pass
    return {
        'statusCode': 200,
        'body': json.dumps('getrooms fin.')
    }
