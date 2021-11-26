import ibm_boto3
import ibm_botocore
from ibm_botocore.client import Config

api_key = 'bkINGGmc7rR5sJY0SBSCmoQYhGmVXrw-Stl-BHlkUyxW'
service_instance_id = 'crn:v1:bluemix:public:cloud-object-storage:global:a/742\
                       ad5ad55ed3bdd3afb038213b69b8a:b8532a93-2e59-40a6-b5b7-f\
                       60aa0067b6b::'
auth_endpoint = 'https://iam.bluemix.net/oidc/token'
service_endpoint = 'https://s3-api.us-geo.objectstorage.softlayer.net'

bucket_name = 'bucketinsper'
item_name = 'file_teste.txt'

cos_cli = ibm_boto3.client('s3',
                      ibm_api_key_id=api_key,
                      ibm_service_instance_id=service_instance_id,
                      ibm_auth_endpoint=auth_endpoint,
                      config=Config(signature_version=ibm_botocore.UNSIGNED),
                      endpoint_url=service_endpoint)

url = cos_cli.generate_presigned_url('get_object', 
                                     ExpiresIn=0, 
                                     Params={'Bucket': bucket_name, 
                                             'Key': item_name})
print(url)