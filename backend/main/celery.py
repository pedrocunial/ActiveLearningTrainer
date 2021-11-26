from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

app = Celery('main')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(settings, namespace='CELERY')
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task
def async_init_accuracy(project_id):
    from api.libs.accuracy import (init_accuracy, set_updating_acc_off, 
                                   seed_is_good, save_train_test_split,
                                   split_seed)
    try:
        train, test = split_seed(project_id)
        save_train_test_split(train, test) # TODO make it stratified
        print("hood")
        if seed_is_good(project_id):
            print("hood")
            return init_accuracy(project_id)
        else:
            set_updating_acc_off(project_id)
    except Exception as e:
        set_updating_acc_off(project_id)


@app.task
def async_update_accuracy(project_id):
    from api.libs.accuracy import (is_ready, has_accuracy_data,
                                   calculate_accuracy, update_accuracy, 
                                   set_updating_acc_off)

    try:
        if is_ready(project_id):
            calculate_accuracy(project_id)
            update_accuracy(project_id)
        else:
            set_updating_acc_off(project_id)
    except Exception as e:
        set_updating_acc_off(project_id)


@app.task
def async_populate_db(project_name, data_type, labels, uid, workspace_id,
                      api_key, url, api_key_storage, instance_id,
                      bucket_name, url_endpoint):
    from api.utils.populate_db import sync_populate_db

    sync_populate_db(project_name, data_type, labels, uid, workspace_id,
                     api_key, url, api_key_storage, instance_id,
                     bucket_name, url_endpoint)


@app.task
def async_update_seed(data_id, label_id, project_id, label):
    from api.libs.classifier import sync_update_seed

    sync_update_seed(data_id, label_id, project_id, label)





@app.task
def async_wao_update(body, project_id):
    from api.libs.wao import update_intent, get_logs

    update_intent(
        body['id'],
        body['label']['id'],
        project_id,
        body['label']['label']
    )
    get_logs(project_id)


@app.task(name='celery.ping')
def ping():
    ''' required for celery testing '''
    return 'pong'
