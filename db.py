import boto3
from config import *


dynamodb = boto3.resource('dynamodb', aws_access_key_id=AWS_ID, aws_secret_access_key=AWS_SECRET_KEY, region_name=AWS_REGION)

def create_table(tbname):
    table = dynamodb.create_table(
        TableName=tbname,
        KeySchema=[
            {
                'AttributeName': '_id',
                'KeyType': 'HASH',
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': '_id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    table.wait_until_exists()

def add_item(tbname, item):
    table = dynamodb.Table(tbname)
    table.put_item(
        Item=item
    )

def add_batch_items(tbname, items):
    table = dynamodb.Table(tbname)
    with table.batch_writer() as batch:
        for item in items:
            try:
                batch.put_item(
                    Item=item
                )
            except Exception as e:
                print(item)
                print(e)
                break

def query_items(type):
    table = dynamodb.Table(TB_DATA)
    response = table.query(
        IndexName='createdBy-type-index',
        KeyConditionExpression='#createdBy = :createdBy AND #typeVar = :typeVal',
        ExpressionAttributeNames={
            '#createdBy': 'createdBy',
            '#typeVar': 'type'  # Use a placeholder for the reserved keyword 'type'
        },
        ExpressionAttributeValues={
            ':createdBy': 'admin',
            ':typeVal': type  # Use the parameter value here
        }
    )
    items = response['Items']
    return items