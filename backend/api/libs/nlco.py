from watson_developer_cloud import NaturalLanguageClassifierV1
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

from api.models import Classifier, Project, CredentialNLC


MODULE_DIR = os.path.dirname(__file__)
CRED = os.path.join(MODULE_DIR, '../../credentials/nlc_credentials.txt')


def get_nlc(project_id):
    """
    Gets NLC object from IBM lib
    """
    url, api_key = get_credentials(project_id)

    nlc = NaturalLanguageClassifierV1(
        iam_apikey=api_key,
        url=url
    )
    return nlc


def get_credentials(project_id):
    credentials = CredentialNLC.objects.get(project__id=project_id)
    url = credentials.url
    api_key = credentials.api_key
    return (url, api_key)


def create_and_fit(training_data, project_id, is_accuracy=False):
    """
    Creates a classifier on IBM and saves on dB as a training classifier
    """
    with open(training_data, 'rb') as td:
        classifier = get_nlc(project_id).create_classifier(
            training_data=td,
            metadata='{"name":"nlc0", "language": "en"}'
        )

    classifier_info = classifier.result
    classifier_id = classifier_info['classifier_id']
    create_training_classifier(classifier_id, project_id, is_accuracy)


def create_training_classifier(classifier_id, project_id, is_accuracy=False):
    """
    Creates classifier on dB as training
    """
    project = Project.objects.get(id=project_id)
    classifier = Classifier(ibm_classifier_id=classifier_id,
                            project=project, is_accuracy=is_accuracy)
    classifier.save()


def classify(classifier_id, pool, project_id, max_workers=4, batch_size=30):
    """
    Classifies a pool of data
    """
    result = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        batches = []
        for i in range(0, len(pool), batch_size):
            limit = ((i + batch_size)
                     if ((i + batch_size) <= len(pool))
                     else len(pool))
            batches.append(
                [{'text': obj.data.content} for obj in pool[i:limit]]
            )
        futures = {
            executor.submit(get_nlc(project_id).classify_collection,
                            classifier_id,
                            data) for data in batches
        }
        results = []
        for future in as_completed(futures):
            results.append(future.result())

        collection = []
        for res in results:
            collection_info = res.result
            collection += collection_info['collection']
        data = {obj.data.content: obj.data.id for obj in pool}
        result = {
            data[value['text']]: {
                item['class_name']: item['confidence']
                for item in value['classes']
            }
            for value in collection
        }
    return result


def delete_classifier(classifier_id, project_id, is_accuracy=False):
    """
    Deletes classifier on IBM Cloud and dB
    """
    get_nlc(project_id).delete_classifier(classifier_id)
    Classifier.objects.get(ibm_classifier_id=classifier_id,
                           is_accuracy=is_accuracy).delete()


def is_training(classifier_id, project_id):
    """
    Checks if classifier is training
    """
    info = get_nlc(project_id).get_classifier(classifier_id)
    status = info.result['status']
    return status == "Training"
