import boto3
from botocore.exceptions import NoCredentialsError

def s3_connection():
    try:
        s3 = boto3.client(
            service_name="s3",
            region_name="ap-northeast-2",
            aws_access_key_id="{access key}",
            aws_secret_access_key="{secret key}",
        )
    except NoCredentialsError:
        print("No AWS credentials found.")
    except Exception as e:
        print(e)
    else:
        print("s3 bucket connected!") 
        return s3
        
s3 = s3_connection()

try:
    s3.upload_file("{file_name_to_upload_in_local}","{bucket_name}","{file_name_to_save_in_bucket}")
    print("s3 uploaded!")
except Exception as e:
    print(e)