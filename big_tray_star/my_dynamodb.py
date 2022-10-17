import boto3

dynamodb = boto3.resource('dynamodb')


# env = os.getenv('env', 'local')
# if env == 'local':
#     dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000",
#                               region_name='us-west-2',
#                               aws_access_key_id='ACCESS_ID',
#                               aws_secret_access_key='ACCESS_KEY')


def put_item(table_name, item):
    table = dynamodb.Table(table_name)
    table.put_item(
        Item=item
    )


def get_item(table_name, artist):
    table = dynamodb.Table(table_name)
    response = table.get_item(Key=artist)
    return response
