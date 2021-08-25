import boto3
import datetime
import hashlib
import json

dynamodb = boto3.resource('dynamodb')
connections = dynamodb.Table('flexible-reversi-tokens')

def lambda_handler(event, context):
    # クライアントの宛先情報（WebSocketの接続ID）
    connectionId = event.get('requestContext', {}).get('connectionId')
    
    # クライアントの宛先情報（API GatewayのURL）
    domainName = event.get('requestContext',{}).get('domainName')
    stage       = event.get('requestContext',{}).get('stage')
    endpointUrl = F"https://{domainName}/{stage}"
    
    # 現在時刻
    now = datetime.datetime.now()
    nowString = str(int(now.timestamp()))
    print(nowString)
    
    # トークンの有効期限
    expirationDatetime = now + datetime.timedelta(days=1)
    
    # 現在時刻から新規にトークンを生成する。トークンは以後の通信でクライアントの識別に用いる。
    token = hashlib.sha256(nowString.encode('utf-8')).hexdigest()
    print(token)
    
    # トークン、API Gateway URL、トークン有効期限、WebSocket 接続ID、をDBに保存する。
    connections.put_item(Item={
        'token': token,
        'endpointUrl': endpointUrl,
        'expirationDatetime': int(expirationDatetime.timestamp()),
        'connectionId': connectionId,
    })
    
    # クライアントにトークンを送る。
    am = boto3.client('apigatewaymanagementapi', endpoint_url=endpointUrl)
    _ = am.post_to_connection(ConnectionId=connectionId, Data=json.dumps({"dataType":"newToken", "data":{"token": token}}))
    
    return {
        'statusCode': 200,
        'body': json.dumps('new token generated.')
    }
