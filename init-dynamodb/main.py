import boto3

dynamodb = boto3.resource('dynamodb')


# env = os.getenv('env', 'local')
# if env == 'local':
#     dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000",
#                               region_name='us-west-2',
#                               aws_access_key_id='ACCESS_ID',
#                               aws_secret_access_key='ACCESS_KEY')


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
        BillingMode='PAY_PER_REQUEST'
    )

    print('Table status:', table.table_status)


def init_table():
    table_name = 'spotify_followed_artist_latest_album'
    create_spotify_followed_artist_latest_album(table_name)


if __name__ == '__main__':
    init_table()
