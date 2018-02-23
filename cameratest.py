import boto3
import picamera
import time

BUCKET = "pythonrekognition"
KEY_SOURCE = "image.jpg"
KEY_TARGET = "sundarimage.jpg"

def UploadToS3():
    KEY = "image.jpg"	
    s3client = boto3.resource('s3')
    data = open('image.jpg', 'rb')
    s3client.Bucket(BUCKET).put_object(Key='image.jpg', Body=data)
    print('upload succcessful')

def TakePicture():
    camera = picamera.PiCamera()
    camera.start_preview()
    time.sleep(6)
    camera.capture('image.jpg')
    camera.stop_preview()
    print('picture taken')

def compare_faces(bucket, key, bucket_target, key_target, threshold=80, region="us-east-1"):    
	rekognition = boto3.client("rekognition", region)
	response = rekognition.compare_faces(
	    SourceImage={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},

		TargetImage={
			"S3Object": {
				"Bucket": bucket_target,
				"Name": key_target,
			}

		},

	    SimilarityThreshold=threshold,

	)

	return response['SourceImageFace'], response['FaceMatches']



if __name__ == '__main__':
    print('trying')
    TakePicture()
    UploadToS3()
    compare_faces(BUCKET, KEY_SOURCE, BUCKET, KEY_TARGET)
    source_face, matches = compare_faces(BUCKET, KEY_SOURCE, BUCKET, KEY_TARGET)
    print("Source Face ({Confidence}%)".format(**source_face))
    for match in matches:
        print ("Target Face ({Confidence}%)".format(**match['Face']))
        print ("  Similarity : {}%".format(match['Similarity']))

  