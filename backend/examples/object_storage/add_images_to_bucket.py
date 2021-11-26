import ibm_boto3
from ibm_botocore.client import Config
import os

api_key = 'z11of1txyZX_nse_tjRahHwb6eOAtUTkxadWeQL_hMx9'
service_instance_id = 'crn:v1:bluemix:public:cloud-object-storage:global:a/742\
                       ad5ad55ed3bdd3afb038213b69b8a:b8532a93-2e59-40a6-b5b7-f\
                       60aa0067b6b::'
auth_endpoint = 'https://iam.bluemix.net/oidc/token'
service_endpoint = 'https://s3-api.us-geo.objectstorage.softlayer.net'

bucket_name = 'bucketinsper'

cos = ibm_boto3.resource('s3',
                      ibm_api_key_id=api_key,
                      ibm_service_instance_id=service_instance_id,
                      ibm_auth_endpoint=auth_endpoint,
                      config=Config(signature_version='oauth'),
                      endpoint_url=service_endpoint)


script_dir = os.path.dirname(__file__)
rel_path = "../dataset/images"
abs_file_path = os.path.join(script_dir, rel_path)
for filename in os.listdir(abs_file_path):
    with open(os.path.join(abs_file_path, filename), 'rb') as myfile:
        data = myfile.read()
        cos.Object(bucket_name, filename).put(
            Body=data,
            ACL='public-read'
        )