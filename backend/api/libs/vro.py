from concurrent.futures import ThreadPoolExecutor, as_completed
from watson_developer_cloud import VisualRecognitionV3
import os
import zipfile
import datetime
import ibm_boto3
from ibm_botocore.client import Config

from api.models import (Classifier, Project, Data, CredentialVR,
                        CredentialObjectStorage)

MODULE_DIR = os.path.dirname(__file__)
POOL_DIR = os.path.join(MODULE_DIR, '../temp_data/pool_files/')
BUCKET_DIR = os.path.join(MODULE_DIR, "../../bucket/")


def create_and_fit(project_id,
                   positive_data,
                   negative_data=None,
                   is_accuracy=False,
                   classifier_name="default"):
    file_obj = {}

    for zipped in positive_data:
        file_obj[zipped + "_positive_examples"] = open(positive_data[zipped],
                                                       'rb')

    if negative_data:
        file_obj["negative_examples"] = open(negative_data, 'rb')

    classifier = get_vr(project_id).create_classifier(classifier_name,
                                                      **file_obj).get_result()

    date = datetime.datetime.now()
    classifier_id = classifier['classifier_id']

    # Close files
    for zipped in positive_data:
        file_obj[zipped + "_positive_examples"].close()

    if negative_data:
        file_obj["negative_examples"].close()

    create_training_classifier(classifier_id, project_id, date, is_accuracy)

    return classifier


def get_credentials(project_id):
    api_key = CredentialVR.objects.get(project__id=project_id).api_key
    return api_key


def get_vr(project_id, version='2018-03-19'):
    vr = VisualRecognitionV3(
        version,
        iam_apikey=get_credentials(project_id)
    )

    return vr


def create_training_classifier(classifier_id, project_id, date, is_accuracy=False):
    project = Project.objects.get(id=project_id)
    classifier = Classifier(ibm_classifier_id=classifier_id,
                            project=project,
                            date=date,
                            is_accuracy=is_accuracy)
    classifier.save()


def is_training(classifier_id, project_id):
    info = get_vr(project_id).get_classifier(classifier_id).get_result()
    status = info['status']
    return status in ("training", "retraining")


def classify(classifier_id,
             pool, project_id,
             threshold='0.0',
             max_workers=4,
             batch_size=20):

    urls = [i.data.url for i in pool]
    result = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(get_vr(project_id).classify,
                            url=url,
                            threshold=threshold,
                            classifier_ids=classifier_id
                            ) for url in urls
        }
        results = []
        for future in as_completed(futures):
            results.append(future.result())

        collection = []

        for res in results:
            collection_info = res.result
            collection += collection_info['images']

        data = {str(obj.data.url): obj.data.id for obj in pool}
        result = {
            data[str(value['source_url'])]: {
                item['class']: item['score']
                for item in value['classifiers'][0]['classes']
            }
            for value in collection
        }
    return result


def update_classifier(classifier_id, project_id, positive_data=None,
                      negative_data=None, is_accuracy=False):
    file_obj = {}

    if positive_data:
        for zipped in positive_data:
            file_obj[zipped + "_positive_examples"] = open(
                positive_data[zipped], 'rb')
    if negative_data:
        file_obj["negative_examples"] = open(negative_data, 'rb')

    get_vr(project_id).update_classifier(classifier_id,
                                         **file_obj)

    # Close Files
    for zipped in positive_data:
        file_obj[zipped + "_positive_examples"].close()

    if negative_data:
        file_obj["negative_examples"].close()

    last_updated = datetime.datetime.now()
    clf = Classifier.objects.get(
        project__id=project_id, is_accuracy=is_accuracy)
    clf.date = last_updated
    clf.save()


def download_data(project_id, data_id):
    credentials = CredentialObjectStorage.objects.get(project__id=project_id)
    data = Data.objects.get(id=data_id)
    auth_endpoint = 'https://iam.bluemix.net/oidc/token'
    cos = ibm_boto3.resource('s3',
                             ibm_api_key_id=credentials.api_key,
                             ibm_service_instance_id=credentials.instance_id,
                             ibm_auth_endpoint=auth_endpoint,
                             config=Config(signature_version='oauth'),
                             endpoint_url=credentials.url)

    cos.Object(credentials.bucket_name, data.content)\
       .download_file(BUCKET_DIR + data.content)
