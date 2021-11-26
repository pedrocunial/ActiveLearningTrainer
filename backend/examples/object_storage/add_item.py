import ibm_boto3
from ibm_botocore.client import Config

api_key = 'z11of1txyZX_nse_tjRahHwb6eOAtUTkxadWeQL_hMx9'
service_instance_id = 'crn:v1:bluemix:public:cloud-object-storage:global:a/742\
                       ad5ad55ed3bdd3afb038213b69b8a:b8532a93-2e59-40a6-b5b7-f\
                       60aa0067b6b::'
auth_endpoint = 'https://iam.bluemix.net/oidc/token'
service_endpoint = 'https://s3-api.us-geo.objectstorage.softlayer.net'

bucket_name = 'bucketinsper'
item_name = 'file_teste.txt'

cos = ibm_boto3.resource('s3',
                      ibm_api_key_id=api_key,
                      ibm_service_instance_id=service_instance_id,
                      ibm_auth_endpoint=auth_endpoint,
                      config=Config(signature_version='oauth'),
                      endpoint_url=service_endpoint)

with open("text_example.csv") as f:
   data = f.read()
   cos.Object(bucket_name, item_name).put(
            Body=data,
            ACL='public-read'
        )