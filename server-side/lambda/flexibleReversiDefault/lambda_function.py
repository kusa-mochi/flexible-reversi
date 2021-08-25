import json

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 404,
        'body': json.dumps('forbidden')
    }
