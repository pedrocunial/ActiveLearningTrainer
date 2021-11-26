import os
import ibm_boto3
import ibm_botocore
import api.libs.wao as wao

from ibm_botocore.client import Config
from api.models import (Pool, Data, Label, PredictProba, Project, User,
                        DataType, CredentialVR, CredentialNLC,
                        CredentialWA, Classifier, CredentialObjectStorage,
                        ProjectHasUser)
from api.libs.accuracy import WA_TYPE
from api.libs.classifier import TEXT_TYPE, IMAGE_TYPE
from main.celery import async_populate_db

from django.db import transaction

MODULE_DIR = os.path.dirname(__file__)
BUCKET_DIR = os.path.join(MODULE_DIR, "../../bucket/")
ALLOWED_DATA_TYPES = (WA_TYPE, TEXT_TYPE, IMAGE_TYPE)


def populate_db(project_name, data_type, labels, uid, workspace_id,
                api_key, url, api_key_storage, instance_id, bucket_name,
                url_endpoint):
    ''' wrapper for making this function call "mockable" '''
    async_populate_db.delay(project_name, data_type, labels, uid, workspace_id,
                            api_key, url, api_key_storage, instance_id,
                            bucket_name, url_endpoint)


def sync_populate_db(project_name, data_type, labels, uid, workspace_id,
                     api_key, url, api_key_storage, instance_id, bucket_name,
                     url_endpoint):
    """
    Populates DB upon creation of new project
    according to its parameters.
    """
    with transaction.atomic():
        try:
            user = User.objects.get(id=uid)
        except User.DoesNotExist:
            raise ValueError("Incorrect user ID")

        if not DataType.objects.filter(type_name=data_type).exists():
            if data_type in ALLOWED_DATA_TYPES:
                DataType.objects.create(type_name=data_type)
            else:
                raise ValueError('Invalid data type')

        dtype = DataType.objects.get(type_name=data_type)

        if not Project.objects.filter(name=project_name).exists():
            project = Project.objects.create(
                name=project_name,
                data_type=dtype,
            )
        else:
            raise ValueError("A project with this name already exists")

        # Create relationship between project and user
        ProjectHasUser.objects.create(
            user=user,
            project=project,
            permission=2  # dono
        )

        if data_type != "wa":
            credentials = CredentialObjectStorage(project=project,
                                                  api_key=api_key_storage,
                                                  instance_id=instance_id,
                                                  bucket_name=bucket_name,
                                                  url=url_endpoint)
            credentials.save()

        if data_type == "text":
            credentials = CredentialNLC(api_key=api_key,
                                        project=project,
                                        url=url)
            credentials.save()
        elif data_type == "image":
            credentials = CredentialVR(api_key=api_key, project=project)
            credentials.save()
        elif data_type == "wa":
            credentials = CredentialWA(api_key=api_key,
                                       project=project,
                                       url=url)
            credentials.save()
            clf = Classifier(ibm_classifier_id=workspace_id,
                             project=project,
                             is_accuracy=False)
            clf.save()

        read_pool = []
        if data_type == "text":
            read_pool = _get_text_content_from_bucket(api_key_storage,
                                                      instance_id,
                                                      bucket_name,
                                                      url_endpoint)

        elif data_type == "image":
            read_pool = _list_files_from_bucket(api_key_storage,
                                                instance_id,
                                                bucket_name,
                                                url_endpoint)

        elif data_type == "wa":
            wao.get_intents(project.id)
            wao.get_logs(project.id, is_first=True)
            return project.id

        datas = []
        for data in read_pool:
            new_data = Data(content=data, project=project)
            if data_type == "image":
                new_data.url = _get_url_item(api_key_storage,
                                             instance_id,
                                             bucket_name,
                                             data,
                                             url_endpoint)
            new_data.save()
            datas.append(new_data)

        pools = []
        for data in datas:
            new_pool = Pool(data=data)
            new_pool.save()
            pools.append(new_pool)

        label_objs = []
        for label in labels:
            new_label = Label(label=label, project=project)
            new_label.save()
            label_objs.append(new_label)

        len_labels = len(labels)

        for pool in pools:
            for label in label_objs:
                new_pp = PredictProba(proba=1/len_labels,
                                      label=label,
                                      pool=pool)
                new_pp.save()

    return project.id


def _list_files_from_bucket(api_key, instance_id, bucket_name, url_endpoint):
    result = []
    auth_endpoint = 'https://iam.bluemix.net/oidc/token'

    cos = ibm_boto3.resource('s3',
                             ibm_api_key_id=api_key,
                             ibm_service_instance_id=instance_id,
                             ibm_auth_endpoint=auth_endpoint,
                             config=Config(signature_version='oauth'),
                             endpoint_url=url_endpoint)

    files = cos.Bucket(bucket_name).objects.all()
    for f in files:
        result.append(f.key)
    return result


def _get_text_content_from_bucket(api_key, instance_id, bucket_name, url_endpoint):
    """
    Gets CSV text from bucket on Object Storage and
    parses it, spliting on \n.
    """
    auth_endpoint = 'https://iam.bluemix.net/oidc/token'

    cos = ibm_boto3.resource('s3',
                             ibm_api_key_id=api_key,
                             ibm_service_instance_id=instance_id,
                             ibm_auth_endpoint=auth_endpoint,
                             config=Config(signature_version='oauth'),
                             endpoint_url=url_endpoint)

    files = cos.Bucket(bucket_name).objects.all()
    for f in files:
        item_name = f.key
    _file = cos.Object(bucket_name, item_name).get()
    file_content = _file["Body"].read()
    return file_content.splitlines()


def _get_url_item(api_key, instance_id, bucket_name, item_name, url_endpoint):
    """
    Generates a public url to an item on a Object Storage bucket.
    """
    auth_endpoint = 'https://iam.bluemix.net/oidc/token'

    cos_cli = ibm_boto3.client('s3',
                               ibm_api_key_id=api_key,
                               ibm_service_instance_id=instance_id,
                               ibm_auth_endpoint=auth_endpoint,
                               config=Config(
                               signature_version=ibm_botocore.UNSIGNED),
                               endpoint_url=url_endpoint)

    url = cos_cli.generate_presigned_url('get_object',
                                         ExpiresIn=0,
                                         Params={'Bucket': bucket_name,
                                                 'Key': item_name})
    return url