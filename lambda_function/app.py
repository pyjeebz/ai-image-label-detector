import json
import boto3

def lambda_handler(event, context):
    # Initialize S3 and Rekognition clients
    s3 = boto3.client('s3')
    rekognition = boto3.client('rekognition')

    # Extract bucket name and image file key from the S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    image_key = event['Records'][0]['s3']['object']['key']

    print(f'Processing image: s3://{bucket}/{image_key}')

    # Call Rekognition to detect labels in the image
    response = rekognition.detect_labels(
        Image={'S3Object': {'Bucket': bucket, 'Name': image_key}},
        MaxLabels=10,
        MinConfidence=80
    )

    # Extract and format label names
    labels = [label['Name'] for label in response['Labels']]
    print(f"Detected labels for image {image_key}: {labels}")

    return {
        'statusCode': 200,
        'body': json.dumps({'labels': labels})
    }
