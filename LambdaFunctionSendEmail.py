import os
import json
import boto3


SUCCESS = 200
SERVER_ERROR = 500


def lambda_handler(event, context):
    # send our event data to CloudWatch Logs for debugging
    # do not forget give permission for Lambda to write logs to CloudWatch
    print(event)

    # decode the JSON we received in the body of the request
    body = json.loads(event['body'])

    # extract name, email, desc
    data = {
        'name': body.get('name'),
        'email': body.get('email'),
        'desc': body.get('desc'),
    }

    try:
        client = boto3.client('ses')
        client.send_email(
            Source= os.environ.get('EMAIL_SOURCE'),
            Destination={
                'ToAddresses': [os.environ.get('EMAIL_RECIPIENT')]
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': 'Name: ' + data['name'] + '\nE-mail: ' + data['email'] + '\nDescription: ' + data['desc'],
                    },
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': 'Contact Form CloudMaCloud.ru: ' + data['name'],
                },
            },
        )

    except (ClientError, ParamValidationError) as e:
        print('SES Error', e)
        return response(SERVER_ERROR, e)

    return response(SUCCESS)


def response(statusCode, errors=None):
    body = {
        'Success': True if statusCode == SUCCESS else False,
    }
    if errors is not None:
        body['errors'] = errors
    return {
        'statusCode': statusCode,
        'body': json.dumps(body),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
        "isBase64Encoded": 'false',
    }