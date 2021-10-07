import boto3

from apps import app
from moto import mock_dynamodb2

test_apigateway_event = {
    "short_id": "sf24bx2z",
    "httpMethod": "GET"}

test_apigateway_event_notexit_noid = {
    "short_id": "noexit",
    "httpMethod": "GET"}

table_name = 'minttable_test'
region_name = 'us-east-1'


def create_dyno_table(table_name, region_name):

    dynamodb = boto3.resource('dynamodb', region_name)

    # create a mock table
    table = dynamodb.create_table(TableName=table_name,
                                  KeySchema=[{'AttributeName': 'short_id',
                                              'KeyType': 'HASH'}],
                                  AttributeDefinitions=[{'AttributeName': 'short_id',
                                                         'AttributeType': 'S'},
                                                        {'AttributeName': 'long_url',
                                                         'AttributeType': 'S'}],
                                  ProvisionedThroughput={'ReadCapacityUnits': 5,
                                                         'WriteCapacityUnits': 5},
                                  GlobalSecondaryIndexes=[{"IndexName": "long_url-index",
                                                           "KeySchema": [{"AttributeName": "long_url",
                                                                          "KeyType": "HASH"}],
                                                           "Projection": {"ProjectionType": "ALL"},
                                                           "ProvisionedThroughput": {'ReadCapacityUnits': 5,
                                                                                     'WriteCapacityUnits': 5}}])


@mock_dynamodb2
def test_update_record():

    create_dyno_table(table_name, region_name)

    # Test: update an existing noid record
    ddb = boto3.resource('dynamodb', region_name=region_name).Table(table_name)

    record = {}
    record["short_id"] = 'sf24bx2z'
    record["long_url"] = 'http://www.test.vt.edu'
    record["hits"] = 0

    ddb.put_item(Item=record)

    response = app.lambda_handler(
        event=test_apigateway_event, context={}, ddb=ddb)

    assert response["statusCode"] == 301
    assert response["location"] == 'http://www.test.vt.edu'

    response = ddb.get_item(
        Key={'short_id': 'sf24bx2z'}
    )
    assert response['Item']['hits'] == 1

    # Test: update a not exist noid record
    response = app.lambda_handler(
        event=test_apigateway_event_notexit_noid, context={}, ddb=ddb)

    assert response["statusCode"] == 301
    assert response["location"] == 'https://vtdlp-dev-cf.s3.amazonaws.com/404.png'
