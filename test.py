import boto3
import pandas

# Creating the low level functional client
client = boto3.client(
    's3',
    aws_access_key_id = 'AKIA46SFIWN5AMWMDQVB',
    aws_secret_access_key = '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',
    region_name = 'ap-south-1'
)
    
# Creating the high level object oriented interface
resource = boto3.resource(
    's3',
    aws_access_key_id = 'AKIA46SFIWN5AMWMDQVB',
    aws_secret_access_key = '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',
    region_name = 'ap-south-1'
)