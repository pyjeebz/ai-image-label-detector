import json
import boto3

def lambda_handler (event, context):
    s3 = boto3.client('s3')
    rekognition = boto3.client ('rekognition')

    bucket = event['Records'][0]['s3']['bucket']['name']
    image_key = event['Records'][0]['s3']['object']['key']

    print (f'Processing image: s3://{bucket}/{image_key}')

    response = rekognition.detect_labels (
        Image = {'S3Object': {'Bucket': bucket, 'Name': image_key}},
        MaxLabels = 10,
        MinConfidence = 80
    )

    labels = [label['Name'] for label in response ['Labels']]

    print (f"Detected labels for image {image_key}: {labels}")

    return {
        'statusCode' : 200,
        'body' : json.dumps({'labels' : labels})
    }

