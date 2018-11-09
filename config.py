import os


REST_API = '/api/v1.0/'
FILES_LIST_GET = 'uploads'
FILE_CHECK_GET = 'uploads/<string:filename>'
FILE_POST = 'upload'
FILE_GET = 'downloads/<string:filename>'

S3_BUCKET = os.environ.get("S3_BUCKET_NAME")
AWS_SERVER_PUBLIC_KEY = os.environ.get("S3_PUBLIC_KEY")
AWS_SERVER_SECRET_KEY = os.environ.get("S3_SECRET_KEY")

S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
