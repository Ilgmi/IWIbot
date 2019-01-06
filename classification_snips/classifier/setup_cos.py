import ibm_boto3
import credentials_cos
from ibm_botocore.client import Config

#Setup to IBM Cloud Object Storage
#Install per pip ibm-cos-sdk

api_key = credentials_cos.API_KEY
service_instance_id = credentials_cos.SERVICE_INSTANCE_ID
auth_endpoint = 'https://iam.bluemix.net/oidc/token'
service_endpoint = 'https://s3-api.us-geo.objectstorage.softlayer.net'


cos = ibm_boto3.resource('s3',
                      ibm_api_key_id=api_key,
                      ibm_service_instance_id=service_instance_id,
                      ibm_auth_endpoint=auth_endpoint,
                      config=Config(signature_version='oauth'),
                      endpoint_url=service_endpoint)


for bucket in cos.buckets.all():
        print(bucket.name)