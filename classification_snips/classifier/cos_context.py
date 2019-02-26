import ibm_boto3
from ibm_botocore.client import Config
from ibm_botocore.client import ClientError

DEFAULT_BUCKET_NAME = "engine"

class CosContext:
    """Setup to IBM Cloud Object Storage"""
    bucket_name = ""
    cos_res = ""
    cos_client = ""

    #init cos client, create default bucket
    def __init__(self, api_key, service_instance_id, auth_endpoint, service_endpoint, bucket_name = DEFAULT_BUCKET_NAME):
        # high-level API
        self.cos_res = ibm_boto3.resource('s3',
                                          ibm_api_key_id=api_key,
                                          ibm_service_instance_id=service_instance_id,
                                          ibm_auth_endpoint=auth_endpoint,
                                          config=Config(signature_version='oauth'),
                                          endpoint_url=service_endpoint)

        # low-level API from cos resorce
        self.cos_client = self.cos_res.meta.client
        self.bucket_name = bucket_name
        if not self._bucket_exist(self.bucket_name):
            result = self.create_bucket()
            if(not result):
                raise Exception("It was not possible to create a bucket: {} ! Please check bucket naming convention..".format(self.bucket_name))

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
        print("Deleting item: '{0}' from bucket {1}...".format(file_name, self.bucket_name))
        try:
            self.cos_res.Object(self.bucket_name, file_name).delete()
            print("OK.Item: '{0}' deleted from bucket!".format(file_name))
        except ClientError as be:
            result = False
            print("CLIENT ERROR: {0}\n".format(be))
        except Exception as e:
            result = False
            print("Unable to delete item: {0}".format(e))
        return result

    def rename_file(self, file_name, new_name):
        result = True
        try:
            self.cos_res.Object(self.bucket_name, new_name).copy_from(CopySource=self.bucket_name+'/' +file_name)
            self.remove_file(file_name)
        except Exception as e:
            result = False
            print(e)
        else:
            print("Renamed file '{0}' to '{1}' ...".format(file_name, new_name))
        return result


    def get_buckets(self):
        for bucket in self.cos_res.buckets.all():
            print(bucket.name)

    def _bucket_exist(self, name ):
        print("Does Bucket ", name, "exist")
        all_buckets = self.cos_res.buckets.all()
        print(all_buckets)
        for bucket in all_buckets:
            if (bucket.name == name):
                return True
        return False

    def remove_bucket(self):
        result = True
        bucket = self.cos_res.Bucket(self.bucket_name)
        try:
            bucket.delete()
        except Exception as e:
            result = False
            print(e)
        else:
            print("Bucket '{0}' was deleted".format(self.bucket_name))
        return result

    def file_exist_in_bucket(self, file_name):
        result = True
        try:
            #do a HEAD request and look at the the result,
            self.cos_res.Object(self.bucket_name, file_name).load()
        except ClientError as e:
            if e.response['Error']['Code'] == "404":
                result = False
                print("The object '{0}' does not exist in bucket '{1}' !".format(file_name, self.bucket_name))
            else:
                result = False
                print(e)
        return result








