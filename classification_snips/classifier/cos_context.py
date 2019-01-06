import ibm_boto3
import credentials_cos
from ibm_botocore.client import Config
from ibm_botocore.client import ClientError

class CosContext:
    """Setup to IBM Cloud Object Storage"""

    api_key = credentials_cos.API_KEY
    service_instance_id = credentials_cos.SERVICE_INSTANCE_ID
    auth_endpoint = 'https://iam.bluemix.net/oidc/token'
    service_endpoint = 'https://s3-api.us-geo.objectstorage.softlayer.net'
    cos_res = ""
    cos_client = ""
    bucket_name = ""

    def __init__(self):
        # high-level API
        cos_res = ibm_boto3.resource('s3',
                                     ibm_api_key_id=self.api_key,
                                     ibm_service_instance_id=self.service_instance_id,
                                     ibm_auth_endpoint=self.auth_endpoint,
                                     config=Config(signature_version='oauth'),
                                     endpoint_url=self.service_endpoint)
        # low-level API from cos resorce
        cos_client = cos_res.meta.client

    def create_bucket(self, bucket_name = 'engine'):
        self.bucket_name = bucket_name
        self.cos_res.create_bucket(Bucket= self.bucket_name)

    def upload_file(self, file_name):
        try:
             self.cos_client.upload_file(file_name,self.bucket_name,file_name)
        except Exception as e:
            print(Exception, e)
        else:
            print("File: {0} uploaded..".format(file_name))

    def download_file(self, file_name):
        try:
            self.cos_client.download_file(Bucket=self.bucket_name, Key=file_name,
                                       Filename='/path/'+file_name)
        except Exception as e:
            print(Exception, e)
        else:
            print("File: {0} downloaded..".format(file_name))

    def remove_file(self, file_name):
        print("Deleting item: {0}".format(file_name))
        try:
            self.cos_res.Object(self.bucket_name, file_name).delete()
            print("Item: {0} deleted!".format(file_name))
        except ClientError as be:
            print("CLIENT ERROR: {0}\n".format(be))
        except Exception as e:
            print("Unable to delete item: {0}".format(e))

    def _get_buckets(self):
        for bucket in self.cos_res.buckets.all():
            print(bucket.name)








