import json
import boto3

sqs = boto3.client('sqs')
queue_url = 'https://sqs.ap-southeast-1.amazonaws.com/830103335377/OrderQueue'


def lambda_handler(event, context):
    order = json.loads(event['body'])
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(order)
    )
    print("Creating order..")
    print("sending in Queue..")

    return {
        'statusCode': 200,
        'body': json.dumps('Order created!')
    }

