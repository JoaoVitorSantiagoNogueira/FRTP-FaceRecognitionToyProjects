import boto3

session = boto3.Session()
client = session.client('rekognition', region_name='us-east-1')

print(client.describe_collection(CollectionId="FaceTestID"))