import json
import boto3
import os


sns = boto3.client('sns')
# queue_url = 'https://sqs.ap-southeast-1.amazonaws.com/830103335377/OrderQueue'
# topic_arn = 'arn:aws:sns:ap-southeast-1:830103335377:OrderTopic'
topic_arn = os.environ['ORDER_TOPIC_ARN'] # This is the environment variable we set in the Lambda function
queue_url = os.environ['ORDER_QUEUE_URL'] # This is the environment variable we set in the Lambda function
# queue = boto3.client('sqs').get_queue_url(QueueName=queue_url)['QueueUrl']
sqs = boto3.resource('sqs').Queue(queue_url)

def lambda_handler(event, context):
    for message in sqs.receive_messages():
        print(message.body)
        
        message_body = json.loads(message.body)
        subject = message_body['subject']
        message = message_body['message']


        response = sns.publish(
            TopicArn=topic_arn,
            Subject=subject,
            Message=message
        )

        message.delete()

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Orders processed'
        })
    }
