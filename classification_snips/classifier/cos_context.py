import ibm_boto3
import credentials_cos
from ibm_botocore.client import Config
from ibm_botocore.client import ClientError

DEFAULT_BUCKET_NAME = "engine"

class CosContext:
    """Setup to IBM Cloud Object Storage"""
    bucket_name = DEFAULT_BUCKET_NAME
    cos_res = ""
    cos_client = ""

    def __init__(self):
        # high-level API
        self.cos_res = ibm_boto3.resource('s3',
                                     ibm_api_key_id=credentials_cos.API_KEY,
                                     ibm_service_instance_id=credentials_cos.SERVICE_INSTANCE_ID,
                                     ibm_auth_endpoint=credentials_cos.AUTH_ENDPOINT,
                                     config=Config(signature_version='oauth'),
                                     endpoint_url= credentials_cos.SERVICE_ENDPOINT)

        # low-level API from cos resorce
        self.cos_client = self.cos_res.meta.client

    def create_bucket(self):
        result = True
        try:
            res = self.cos_res.create_bucket(Bucket=self.bucket_name)
        except Exception as e:
            result = False
            print(Exception, e)
        else:
            print("Bucket {0} was created as: {1} ".format(self.bucket_name, res))
        return result

    def upload_file(self, path_to_file, file_name):
        result = True
        try:
            self.cos_client.upload_file(path_to_file, self.bucket_name, file_name)
        except Exception as e:
            result = False
            print(Exception, e)
        else:
            print("File: {0} uploaded to bucket: {1}".format(file_name, self.bucket_name))
        return result

    def download_file(self, path_to_save, file_name):
        result = True
        try:
            self.cos_client.download_file(Bucket=self.bucket_name, Key=file_name,
                                       Filename=path_to_save+'/'+file_name)
        except Exception as e:
            result = False
            print(Exception, e)
        else:
            print("File: {0} downloaded..".format(file_name))
        return result

    def remove_file(self, file_name):
        result = True
        print("Deleting item: {0}".format(file_name))
        try:
            self.cos_res.Object(self.bucket_name, file_name).delete()
            print("Item: {0} deleted!".format(file_name))
        except ClientError as be:
            result = False
            print("CLIENT ERROR: {0}\n".format(be))
        except Exception as e:
            result = False
            print("Unable to delete item: {0}".format(e))
        return result

    def get_buckets(self):
        for bucket in self.cos_res.buckets.all():
            print(bucket.name)

    def remove_bucket(self):
        result = True
        bucket = self.cos_res.Bucket(self.bucket_name)
        try:
            bucket.delete()
        except Exception as e:
            result = False
            print(e)
        else:
            print("Bucket {0} was deleted".format(self.bucket_name))
        return result









