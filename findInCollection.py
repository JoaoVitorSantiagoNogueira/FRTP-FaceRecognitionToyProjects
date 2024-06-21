import boto3
import io
from PIL import Image

##pode ser com ID ou com uma foto

session = boto3.Session()
client = session.client('rekognition', region_name='us-east-1')

local = "testimg3.jpeg"
image = Image.open(local)
stream = io.BytesIO()
image.save(stream,format="JPEG")
bytes  = stream.getvalue() 

result = client.search_faces_by_image(CollectionId="FaceTestID",
                                   FaceMatchThreshold=90,
                                   Image = {"Bytes":bytes},
                                   )

print(result)
print(len(result["FaceMatches"]))