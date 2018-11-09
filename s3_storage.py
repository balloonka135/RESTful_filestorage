import boto3
import botocore
import config

# initialize session with AWS S3 service
session = boto3.Session(
    aws_access_key_id=config.AWS_SERVER_PUBLIC_KEY,
    aws_secret_access_key=config.AWS_SERVER_SECRET_KEY
)

s3 = session.resource('s3')


# initialize client to upload/download files
client_s3 = boto3.client(
   "s3",
   aws_access_key_id=config.AWS_SERVER_PUBLIC_KEY,
   aws_secret_access_key=config.AWS_SERVER_SECRET_KEY
)


def upload_file(file, bucket_name, acl="public-read"):
    '''
    Upload binary file to S3 bucket.
    '''
    try:
        client_s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        print("Error occured: ", e)
        return e

    return "{}{}".format(config.S3_LOCATION, file.filename)


def check_file(file, bucket_name):
    '''
    Checking file availability in S3 bucket by key.
    '''
    objects = bucket_content(bucket_name)

    # check if bucket and file exist
    if objects[0]:
        if str(file) in objects[1]:
            return True
    return False


def bucket_content(bucket_name):
    '''
    Iterate over objects in S3 bucket.
    '''

    bucket = s3.Bucket(bucket_name)

    # validate if bucket exists
    exists = True
    try:
        s3.meta.client.head_bucket(Bucket=bucket_name)
    except botocore.exceptions.ClientError as e:
        # if 404 error, then the bucket does not exist
        error_code = e.response['Error']['Code']
        if error_code == '404':
            exists = False
            return exists, e
    if exists:
        obj_list = []
        for key in bucket.objects.all():
            obj_list.append(key.key)
        return exists, obj_list


def download_file(file, bucket_name):
    '''
    Download file from S3 bucket by key.
    '''
    file_output = open('file_output.bin', 'wb')  # file to download data to
    try:
        client_s3.download_fileobj(bucket_name, file, file_output)
        file_output.close()
        return True
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
            return False
