import boto3

def lambda_handler(event, context):
    source_bucket = 'lwsourcecopybucket'
    destination_bucket = 'jagguprojectwebsiteproject'
    s3_client = boto3.client('s3')

    # List objects in the source bucket
    response = s3_client.list_objects_v2(Bucket=source_bucket)
    
    # Transfer each object to the destination bucket
    for obj in response['Contents']:
        key = obj['Key']
        copy_source = {'Bucket': source_bucket, 'Key': key}
        s3_client.copy_object(CopySource=copy_source, Bucket=destination_bucket, Key=key)

    # Publish SNS notification after files are transferred
    sns_client = boto3.client('sns')
    sns_topic_arn = 'arn:aws:sns:us-east-1:380481785354:sendingmailontime'
    sns_client.publish(TopicArn=sns_topic_arn, Message='http://landingwebpagebucket.s3-website-us-east-1.amazonaws.com',Subject='Birthday Wishes')

    return {
        'statusCode': 200,
        'body': 'Files transferred successfully!'
    }