import boto3
import json

dynamodb = boto3.resource('dynamodb')
connections = dynamodb.Table('flexible-reversi-tokens')
nicknames = dynamodb.Table('flexible-reversi-nicknames')
appData = dynamodb.Table('flexible-reversi')

def lambda_handler(event, context):
    # トークン情報をすべて削除する。
    connectionsScan = connections.scan()
    with connections.batch_writer() as batch:
        for each in connectionsScan['Items']:
            batch.delete_item(
                Key={
                    'token': each['token']
                }
            )
    
    # ニックネームをすべて削除する。
    nicknamesScan = nicknames.scan()
    with nicknames.batch_writer() as batch:
        for each in nicknamesScan['Items']:
            batch.delete_item(
                Key={
                    'nickname': each['nickname']
                }
            )
    
    # id 2以降の部屋情報を削除する。
    appDataScan = appData.scan()
    with appData.batch_writer() as batch:
        for each in appDataScan['Items']:
            if each['id'] >= 2:
                batch.delete_item(
                    Key={
                        'id': each['id']
                    }
                )
    
    # id 1の部屋情報をid 2~30にコピーする。
    vacancyRoomData = appData.get_item(Key={'id': 1})['Item']
    for roomId in range(2, 31):
        vacancyRoomData['id'] = roomId
        appData.put_item(Item=vacancyRoomData)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
