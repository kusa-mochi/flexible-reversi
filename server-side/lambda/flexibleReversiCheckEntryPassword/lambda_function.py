import boto3
from decimal import Decimal
import hashlib
import json

dynamodb = boto3.resource('dynamodb')
connections = dynamodb.Table('flexible-reversi-tokens')
appData = dynamodb.Table('flexible-reversi')

def rooms_default_dumps(obj):
    if isinstance(obj, Decimal):
        return int(obj)
    raise TypeError

def lambda_handler(event, context):
    
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
        
    # 返信先情報
    connectionId = event.get('requestContext', {}).get('connectionId')
    domainName = event.get('requestContext',{}).get('domainName')
    stage       = event.get('requestContext',{}).get('stage')
    endpointUrl = F"https://{domainName}/{stage}"
    
    # 部屋番号
    roomId = postData['id']
    print('room id : ' + str(roomId))
    
    # DynamoDBから、部屋番号に対応する情報を取得する。
    response = appData.get_item(Key={'id': roomId})

    # DynamoDBで持っているパスワードのハッシュ値の取得
    dbPasswordHash = response['Item']['entryPassword']
    print(dbPasswordHash)
    
    # 送られてきたパスワードのハッシュ値を計算する。
    postPasswordHash = hashlib.sha256(postData['password'].encode('utf-8')).hexdigest()
    print(postPasswordHash)
    
    # ハッシュ値同士を比較し、パスワードが正しいかチェックする。
    ret = ''
    if postPasswordHash == dbPasswordHash:
        # トークンを部屋情報に記載する。
        # この情報と照合することで、パスワードを入力したユーザは部屋への入室が可能となる
        exp = 'set '
        exp += 'opponentId=:opponentId'
        appData.update_item(
            Key={'id': roomId},
            UpdateExpression=exp,
            ExpressionAttributeValues={
                ':opponentId': token
            },
            ReturnValues='UPDATED_NEW'
            )
        response = appData.get_item(Key={'id': roomId})
        # クライアントに、パスワードが正しいことと、先攻後攻情報、盤面情報、部屋の開設者のニックネームを送る。
        ret = json.dumps({
            "dataType":"checkedEntryPassword",
            "data":{
                "currentBoard":response['Item']['currentBoard'],
                "firstPlayer":response['Item']['firstPlayer'],
                "result":"OK",
                "roomAuthor":response['Item']['roomAuthor']
            }
        }, default=rooms_default_dumps)
    else:
        ret = json.dumps({"dataType":"checkedEntryPassword", "data":{"result":"NG"}})
    
    # チェック結果を返信する。
    am = boto3.client('apigatewaymanagementapi', endpoint_url=endpointUrl)
    _ = am.post_to_connection(ConnectionId=connectionId, Data=ret)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
