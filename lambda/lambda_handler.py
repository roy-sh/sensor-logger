import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SensorDataTable')

def main(event, context):
    data = json.loads(event['body'])
    # Process the data as needed
    response = table.put_item(Item=data)
    return {
        'statusCode': 200,
        'body': json.dumps('Data processed successfully!')
    }

