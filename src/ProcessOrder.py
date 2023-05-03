import json
import boto3

sqs = boto3.client('sqs')
sns = boto3.client('sns')
queue_url = 'https://sqs.ap-southeast-1.amazonaws.com/830103335377/OrderQueue'
topic_arn = 'arn:aws:sns:ap-southeast-1:830103335377:OrderTopic'



def lambda_handler(event, context):
    for record in event['Records']:
        message = json.loads(record['body'])
        order_id = message['order_id']
        customer_name = message['customer_name']
        order_total = message['order_total']

        subject = f'New Order {order_id}'
        message = f'Customer Name: {customer_name}\nOrder Total: {order_total}'

        response = sns.publish(
            TopicArn=topic_arn,
            Subject=subject,
            Message=message
        )

        print(response)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Orders processed'
        })
    }
