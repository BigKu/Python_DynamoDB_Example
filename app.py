from __future__ import print_function
import boto3
import json
import os
import decimal
from boto3.dynamodb.conditions import Key, Attr
from flask import Flask, request, send_from_directory

'''
dynamodb = boto3.resource('dynamodb', ...)

memo_table = None
try:
    memo_table = dynamodb.create_table(TableName='Memos', ....)
except:
    memo_table = dynamodb.Table('Memos')




# memo_table.put_item(Item={...})

response = memo_table.get_item(key={'title': 'memo0', 'author': 'ksm'})

item =None
try:
    item = response['Item']
except:
    pass

'''


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

app = Flask(__name__, static_url_path='/static')

dynamodb = boto3.resource('dynamodb',
    endpoint_url='http://192.168.99.100:8000',
    region_name='west-east',
    aws_secret_access_key='dummy',
    aws_access_key_id='dummy',
    verify=False,
)

table = 'none'
try:
    table = dynamodb.create_table(
        TableName='Memos',
        KeySchema=[
            {
                'AttributeName': 'tag',
                'KeyType': "HASH",
            },
            {
                'AttributeName': 'memoId',
                'KeyType': "RANGE",
            },

        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'memoId',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'tag',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )
except:
    table = dynamodb.Table('Memos')


table.put_item(
    Item={
        'memoId': 'x',
        'message': 'This is an example message test sample',
        'tag': 'example-tag-one'
    },
)

table.put_item(
    Item={
        'memoId': 'z',
        'message': 'This is an example message test sample',
        'tag': 'three'
    },
)

table.put_item(
    Item={
        'memoId': 'y',
        'message': 'This is an example message test sample',
        'tag': 'example-tag-two'
    }
)

response = table.get_item(
    Key={
        'memoId': 'z',
        'tag': 'three'
    }
)
item = response['Item']
print(item)
print(table.item_count)

# @app.route('/memos')
# def memos():
#     response = table.scan()
#     return json.dumps(response['Items'], cls=DecimalEncoder)
@app.route('/memos')
def memos():
    query = request.args.get('tag')
    if query != None :
        response = table.query(
            KeyConditionExpression=Key('tag').eq(query)
        )
        return json.dumps(response['Items'], cls=DecimalEncoder)
    else:
        response = table.scan()
        return json.dumps(response['Items'], cls=DecimalEncoder)

@app.route('/')
def default_file():
    return app.send_static_file('index.html')

@app.route('/js/<path:path>')
def sendjs(path):
    if os.path.exists('static/js/%s' % path) :
        return send_from_directory('static/js', path)
    else :
         return ""
