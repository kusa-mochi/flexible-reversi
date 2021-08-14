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
    #print(json.dumps(rooms[0]['current_board'], default=decimal_default_proc))
    
    for room in rooms:
        ret += '{'
        
        # board logs ->
        ret += '"board_logs":['
        for board in room['board_logs']:
            ret += '['
            for row in board:
                ret += '['
                for val in row:
                    ret += str(val) + ','
                ret = ret[:-1] + '],'
            ret = ret[:-1] + '],'
        ret = ret[:-1] + '],'
        # <- board logs
        
        # can view ->
        ret += '"can_view":' + str(room['can_view']).lower() + ','
        # <- can view
        
        # current board ->
        ret += '"current_board":['
        for row in room['current_board']:
            ret += '['
            for val in row:
                ret += str(val) + ','
            ret = ret[:-1] + '],'
        ret = ret[:-1] + '],'
        # <- current board
        
        # current player ->
        ret += '"current_player":' + str(room['current_player']).lower() + ','
        # <- current player
        
        # entry password ->
        ret += '"entry_password":"' + room['entry_password'] + '",'
        # <- entry password
        
        # first player id ->
        ret += '"first_player_id":"' + room['first_player_id'] + '",'
        # <- first player id
        
        # id ->
        ret += '"id":' + str(room['id']) + ','
        # <- id
        
        # opponent id ->
        ret += '"opponent_id":"' + room['opponent_id'] + '",'
        # <- opponent id
        
        # opponent name ->
        ret += '"opponent_name":"' + room['opponent_name'] + '",'
        # <- opponent name
        
        # require entry password ->
        ret += '"require_entry_password":' + str(room['require_entry_password']).lower() + ','
        # <- require entry password
        
        # require view password ->
        ret += '"require_view_password":' + str(room['require_view_password']).lower() + ','
        # <- require view password
        
        # room author ->
        ret += '"room_author":"' + room['room_author'] + '",'
        # <- room author
        
        # room name ->
        ret += '"room_name":"' + room['room_name'] + '",'
        # <- room name
        
        # room state ->
        ret += '"room_state":"' + room['room_state'] + '",'
        # <- room state
        
        # thinking counter ->
        ret += '"thinking_counter":' + str(room['thinking_counter']) + ","
        # <- thinking counter
        
        # view password ->
        ret += '"view_password":"' + room['view_password'] + '",'
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
        'body': json.dumps('Hello from Lambda!')
    }
