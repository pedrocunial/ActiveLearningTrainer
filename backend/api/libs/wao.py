from watson_developer_cloud import AssistantV1
import os

from django.db import transaction
from api.models import (Classifier, Project, CredentialWA,
                        Label, Data, Pool, PredictProba)
from main.celery import async_wao_update


def get_wa(project_id, version='2018-09-20'):
    """
    Gets WA object from IBM lib
    """
    url, api_key = get_credentials(project_id)

    wa = AssistantV1(
        version=version,
        iam_apikey=api_key,
        url=url
    )
    return wa


def get_credentials(project_id):
    credentials = CredentialWA.objects.get(project__id=project_id)
    url = credentials.url
    api_key = credentials.api_key
    return (url, api_key)


def update(body, project_id):
    ''' wrapper necessary for testing '''
    async_wao_update.delay(body, project_id)


def get_logs(project_id, is_first=False, is_accuracy=False):
    """update logs based on last log date"""
    clf = Classifier.objects.get(
        project__id=project_id, is_accuracy=is_accuracy)
    project = Project.objects.get(id=project_id)

    response = {}
    if is_first:
        response = get_wa(project_id).list_logs(
            workspace_id=clf.ibm_classifier_id,
            sort='request_timestamp',
        ).get_result()
    else:
        query_filter = "response_timestamp>" + clf.log_date
        response = get_wa(project_id).list_logs(
            workspace_id=clf.ibm_classifier_id,
            sort='request_timestamp',
            filter=query_filter
        ).get_result()

    with transaction.atomic():
        if response["logs"]:
            for log in response["logs"]:
                new_data = Data(
                    project=project,
                    content=log["request"]["input"]["text"]
                )
                new_data.save()

                new_pool = Pool(data=new_data)
                new_pool.save()

                label = Label.objects.get(
                    project__id=project_id,
                    label=log["response"]["intents"][0]["intent"]
                )

                new_proba = PredictProba(
                    label=label,
                    pool=new_pool,
                    proba=log["response"]["intents"][0]["confidence"]
                )
                new_proba.save()

            last_log_time = response["logs"][-1]["response_timestamp"]
            clf.log_date = last_log_time
            clf.save()


def get_intents(project_id, is_accuracy=False):
    """populate labels with assistant intents"""

    clf = Classifier.objects.get(
        project__id=project_id, is_accuracy=is_accuracy)
    project = Project.objects.get(id=project_id)
    response = get_wa(project_id).list_intents(
        workspace_id=clf.ibm_classifier_id
    ).get_result()

    with transaction.atomic():
        for intent in response["intents"]:
            new_label = Label(label=intent["intent"], project=project)
            new_label.save()


def update_intent(pool_id, label_id, project_id, label, is_accuracy=False):
    """creates an example on an intent based on the rotulated log"""
    clf = Classifier.objects.get(
        project__id=project_id, is_accuracy=is_accuracy)

    get_wa(project_id).create_intent(
        workspace_id=clf.ibm_classifier_id,
        intent=label,
        examples=[
            {'text': Data.objects.get(id=pool_id).content}
        ]
    )

    try:
        response = get_wa(project_id).create_example(
            workspace_id=clf.ibm_classifier_id,
            intent=Label.objects.get(id=label_id).label,
            text=Data.objects.get(id=pool_id).content
        )

    except Exception as e:
        """
        Tries to upload new example to intent, but it might exist already.
        """
        pass

    Pool.objects.get(data__id=pool_id).delete()
