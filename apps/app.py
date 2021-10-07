import boto3
import os


region_name = os.getenv('Region')
table_name = os.getenv('TargetTable')
image_404 = os.getenv('Image404')

ddb = boto3.resource('dynamodb', region_name=region_name).Table(table_name)


def lambda_handler(event, context, ddb):

    short_id = event.get('short_id')

    try:
        item = ddb.get_item(Key={'short_id': short_id})

        if item.get('Item'):
            long_url = item.get('Item').get('long_url')

            # increase the hit number on the db entry of the url
            ddb.update_item(
                Key={'short_id': short_id},
                UpdateExpression='set hits = hits + :val',
                ExpressionAttributeValues={':val': 1}
            )
            return {
                "statusCode": 301,
                "location": long_url
            }
        else:
            raise Exception('No such Noid')

    except BaseException:
        return {
            'statusCode': 301,
            'location': image_404
        }
