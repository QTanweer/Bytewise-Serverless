import json

def lambda_handler(event, context):
    print("Processing order..")
    return {
        'statusCode': 200,
        'body': json.dumps('Order processed!')
    }