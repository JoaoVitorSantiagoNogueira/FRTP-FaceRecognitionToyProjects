import boto3
from PIL import Image, ImageDraw
import io
import matplotlib.pyplot as plt
import numpy as np



"""from boto3.session import Session

s = Session()
dynamodb_regions = s.get_available_regions('rekognition')
"""

local='testimg.jpg'
local2 = 'testimg2.jpg'

client = boto3.client('rekognition', region_name='us-east-1')
image = Image.open(local)
image2 = Image.open(local2)

stream = io.BytesIO()
stream2 = io.BytesIO()

image.save(stream,format="JPEG")
image2.save(stream2,format="JPEG")

src_image_binary  = stream.getvalue()
trgt_image_binary = stream2.getvalue()


response = response = client.compare_faces(
    SimilarityThreshold=90,
    SourceImage={'Bytes':src_image_binary},
    TargetImage={'Bytes':trgt_image_binary}
    )

"""for faceMatch in response['FaceMatches']:
        position = faceMatch['Face']['BoundingBox']
        similarity = str(faceMatch['Similarity'])
        print('The face at ' +
              str(position['Left']) + ' ' +
              str(position['Top']) +
              ' matches with ' + similarity + '% confidence')"""


# create bounding boxes orignal image

top    = response['SourceImageFace']['BoundingBox']['Top'] * image.height
left   = response['SourceImageFace']['BoundingBox']['Left'] * image.width
width  = response['SourceImageFace']['BoundingBox']['Width'] * image.width
height = response['SourceImageFace']['BoundingBox']['Height'] * image.height

shape = [(left, top), (left + width, top + height)]

imgSquare = ImageDraw.Draw(image)
imgSquare.rectangle(shape, fill ="#ffff3300", outline ="red")

# create bounding boxes target image

top2    = response['FaceMatches'][0]['Face']['BoundingBox']['Top'] * image2.height
left2   = response['FaceMatches'][0]['Face']['BoundingBox']['Left'] * image2.width
width2  = response['FaceMatches'][0]['Face']['BoundingBox']['Width'] * image2.width
height2 = response['FaceMatches'][0]['Face']['BoundingBox']['Height'] * image2.height

shape2 = [(left2, top2), (left2 + width2, top2 + height2)]

img2Square = ImageDraw.Draw(image2)
img2Square.rectangle(shape2, fill ="#ffff3300", outline ="red")


fig = plt.figure(figsize=(10, 7))
print(response)
#image.show()
fig.add_subplot(2, 1, 1)
plt.axis('off')
plt.imshow(np.asarray(image))


fig.add_subplot(2, 1, 2)
plt.axis('off')
plt.imshow(np.asarray(image2))
plt.show()