import boto3

dynamodb = boto3.resource('dynamodb')


# env = os.getenv('env', 'local')
# if env == 'local':
#     dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000",
#                               region_name='us-west-2',
#                               aws_access_key_id='ACCESS_ID',
#                               aws_secret_access_key='ACCESS_KEY')


def delete_table(table_name):
    try:
        table = dynamodb.Table(table_name)
        table.delete()
    except dynamodb.meta.client.exceptions.ResourceNotFoundException as e:
        pass


def put_item(table_name, item):
    table = dynamodb.Table(table_name)
    table.put_item(
        Item=item
    )


def get_item(table_name, artist):
    table = dynamodb.Table(table_name)
    response = table.get_item(Key=artist)
    return response


def create_spotify_followed_artist_latest_album(table_name):
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'artist_id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'artist_id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    print('Table status:', table.table_status)


def init_table():
    table_name = 'spotify_followed_artist_latest_album'
    delete_table(table_name)
    create_spotify_followed_artist_latest_album('spotify_followed_artist_latest_album')


if __name__ == '__main__':
    init_table()
