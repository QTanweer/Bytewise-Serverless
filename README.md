# Bytewise-serverless-Task

Creating a simple Ordering service with AWS Serverless Architecture using AWS SAM as Infrastructure-as-Code (IaC).

This project was a part from the [ByteWise](https://www.bytewiseltd.com/) fellowship program.
The goal of this project is to get acquainted with AWS Serverless Architecture, its various services, AWS SAM as IaC and Github Actions for CI/CD pipelines.

## AWS Serverless Architecture

This project is a simple ordering service that allows users to order a product and get the order details. The service is built using `AWS Lambda`, `API Gateway`, `SQS`, and ``SNS`` as shown in figure below.

![AWS Serverless Architecture](/images/Task-Flow.jpg)

The Project flow is as follows:

1. The user sends a POST request to the API Gateway endpoint with the order details.
2. The API Gateway triggers the `CreateOrder` Lambda function.
3. The Lampbda function sends the information to a queue (SQS).
4. The SQS queue, in turn, triggers the next Lambda function (`ProcessOrder`).
5. This Lambda function publishes the order details to an SNS Topic.
6. This SNS Topic sends the order details to the user via email.

### Usage

+ The Order details of user is sent by POST request to the "InvokingAPI" endpoint in the following JSON format:

```bash
{
    "name": "John Doe",
    "email": "xyz@mailserice.com",
    "product": "Product Name",
    "quantity": 1
}

```

+ The user will receive an email with the order details.

## Infrastucture-as-Code (IaC) using AWS SAM

As this project is built using AWS SAM, we will be using a [template](/template.yaml) file to define the AWS resources used in this project.

The template file defines the following resources:

1. Two Lambda functions: `CreateOrder` and `ProcessOrder`.
2. An SQS queue: `OrderQueue`.
3. An SNS Topic: `OrderTopic`.
4. An SNS Topic Subscription: `OrderNotificationSubscription`.
5. An API Gateway endpoint:  `InvokingApi`.

The template file also defines the following environment variables:

1. The SQS queue URL: `ORDER_TOPIC_ARN`.
2. The SNS Topic ARN: `QUEUE_URL`.

The template file also defines the following outputs:

1. The API Gateway endpoint URL.
2. The SQS queue URL:  `OrderQueueUrl`.
3. The SNS Topic ARN:  `OrderTopicArn`.

The template file also defines the following policies:

1. A policy for the CreateOrder Lambda function to send messages to the SQS queue.
2. A policy for the ProcessOrder Lambda function to receive messages from the SQS queue and publish messages to the SNS Topic.
3. A policy for the SNS Topic to send emails to the user.

The template file also defines the following permissions:

1. A permission for the SQS queue to trigger the ProcessOrder Lambda function.
2. A permission for the API Gateway endpoint to trigger the CreateOrder Lambda function.

The template file can be found [here](/template.yaml) in the project repository.

## CI/CD Pipeline using Github Actions

This service is deployed using CI/CD pipelines of Github Actions. The CI/CD pipeline is defined in the [workflow](/.github/workflows/sam-pipeline.yml) file.

The `DeployProd` job is defined in this workflow, which is responsible for deploying the application to the production environment. The job runs on an Ubuntu latest virtual machine and has an environment named "production". The job is triggered when a push event occurs on the main branch of the repository.

 The workflow file defines the following main jobs:

1. Build: This job builds the project using the `sam build --use-container` command
2. Deploy: This job deploys the SAM application to the production environment using the `sam deploy` command. The `--no-confirm-changeset` flag is used to automatically confirm the changeset, `--no-fail-on-empty-changeset` flag is used to not fail if there are no changes to be deployed, `--stack-name` flag is used to specify the name of the CloudFormation stack, `--resolve-s3` flag is used to resolve S3 bucket names in the CloudFormation template, `--capabilities` flag is used to specify the IAM and auto-expand capabilities, and `--region` flag is used to specify the AWS region.

The workflow file also defines the following environment variables:

1. AWS_ACCESS_KEY_ID: The AWS access key ID.
2. AWS_SECRET_ACCESS_KEY: The AWS secret access key.
3. AWS_DEFAULT_REGION: The AWS region.

These environment variables are acquired from AWS Console, and defined as secrets in the repository settings.

## License

[MIT](https://choosealicense.com/licenses/mit/)
