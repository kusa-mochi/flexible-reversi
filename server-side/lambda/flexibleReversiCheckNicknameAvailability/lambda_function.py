import boto3
import json

dynamodb = boto3.resource('dynamodb')
connections = dynamodb.Table('flexible-reversi-tokens')
nicknames = dynamodb.Table('flexible-reversi-nicknames')

def lambda_handler(event, context):
    print("checkNicknameAvailability start.")
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
    
    nickname = postData['nickname']
    
    # TODO: check if a nickname is already registered to DB.
    response = nicknames.get_item(Key={'nickname': nickname})
    checkResult = ''
    if 'Item' in response:
        print('nickname is already in use.')
        checkResult = 'inUse'
    else:
        print('nickname is not yet in use.')
        checkResult = 'isAvailable'

    # ニックネームが使用可能な場合
    if checkResult == 'isAvailable':
        # トークンの有効期限をDBから取得する。
        expirationDatetime = connections.get_item(Key={'token': token})['Item']['expirationDatetime']
        # DBにニックネームを記録する。
        connections.update_item(
            Key={
                'token': token
            },
            UpdateExpression='set nickname=:nickname',
            ExpressionAttributeValues={
                ':nickname': nickname
            },
            ReturnValues="UPDATED_NEW"
        )
        nicknames.put_item(Item={
            'nickname': nickname,
            'expirationDatetime': expirationDatetime
        })
    
    # クライアントの宛先情報（WebSocketの接続ID）
    connectionId = event.get('requestContext', {}).get('connectionId')
    
    # クライアントの宛先情報（API GatewayのURL）
    domainName = event.get('requestContext',{}).get('domainName')
    stage       = event.get('requestContext',{}).get('stage')
    endpointUrl = F"https://{domainName}/{stage}"
    
    # クライアントにニックネームのチェック結果を送る。
    am = boto3.client('apigatewaymanagementapi', endpoint_url=endpointUrl)
    _ = am.post_to_connection(ConnectionId=connectionId, Data=json.dumps({"dataType":"checkNicknameAvailability", "data":{"nicknameAvailability": checkResult}}))
    
    return {
        'statusCode': 200,
        'body': json.dumps('checkNicknameAvailability fin.')
    }
