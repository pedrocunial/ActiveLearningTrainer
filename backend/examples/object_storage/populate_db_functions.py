import ibm_boto3
from ibm_botocore.client import Config

api_key = 'z11of1txyZX_nse_tjRahHwb6eOAtUTkxadWeQL_hMx9'
service_instance_id = 'crn:v1:bluemix:public:cloud-object-storage:global:a/742\
                       ad5ad55ed3bdd3afb038213b69b8a:b8532a93-2e59-40a6-b5b7-f\
                       60aa0067b6b::'
bucket_name = 'bucketinsper'

def _list_files_from_bucket(api_key, instance_id, bucket_name):
    result = []
    auth_endpoint = 'https://iam.bluemix.net/oidc/token'
    service_endpoint = 'https://s3-api.us-geo.objectstorage.softlayer.net'

    cos = ibm_boto3.resource('s3',
                      ibm_api_key_id=api_key,
                      ibm_service_instance_id=instance_id,
                      ibm_auth_endpoint=auth_endpoint,
                      config=Config(signature_version='oauth'),
                      endpoint_url=service_endpoint)

    files = cos.Bucket(bucket_name).objects.all()
    for f in files:
        result.append(f.key)
    return result

def _get_text_content_from_bucket(api_key, instance_id, bucket_name):
    auth_endpoint = 'https://iam.bluemix.net/oidc/token'
    service_endpoint = 'https://s3-api.us-geo.objectstorage.softlayer.net'

    cos = ibm_boto3.resource('s3',
                      ibm_api_key_id=api_key,
                      ibm_service_instance_id=instance_id,
                      ibm_auth_endpoint=auth_endpoint,
                      config=Config(signature_version='oauth'),
                      endpoint_url=service_endpoint)

    files = cos.Bucket(bucket_name).objects.all()
    for f in files:
        item_name = f.key
    _file = cos.Object(bucket_name, item_name).get()
    file_content = _file["Body"].read()
    return file_content.splitlines()

print(_get_text_content_from_bucket(api_key, service_instance_id, bucket_name))