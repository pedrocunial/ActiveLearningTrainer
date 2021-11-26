import api.libs.nlco as nlco
import api.libs.vro as vro
from api.models import (Pool, Data, Label, Seed,
                        PredictProba, Classifier, Project
                        )
from django.db import transaction
from main.celery import async_update_seed

import os
import csv
import datetime
import zipfile

IMAGE_TYPE = 'image'
TEXT_TYPE = 'text'
MODULE_DIR = os.path.dirname(__file__)
VR_SEED_DIR = os.path.join(MODULE_DIR, '../temp_data/seed_files/')
SEED_DIR = os.path.join(MODULE_DIR, '../temp_data/seed.csv')
NEGATIVE_SEED = os.path.join(MODULE_DIR, '../temp_data/negative.zip')
BUCKET_DIR = os.path.join(MODULE_DIR, "../../bucket/")


def seed_is_good(project_id, min_seed=6):
    """
    Checks if seed content is within minimum required for classifier creation
    """
    min_seed = min_seed if min_seed > 10 else 10

    project = Project.objects.get(id=project_id)
    label_count = Seed.objects.filter(label__project__id=project_id) \
                              .order_by() \
                              .values('label') \
                              .distinct() \
                              .count()

    if project.data_type.type_name == TEXT_TYPE:
        label_db_count = Label.objects.filter(project__id=project_id).count()
        seed_count = Seed.objects.filter(label__project__id=project_id).count()
        return label_count == label_db_count and seed_count >= min_seed

    elif project.data_type.type_name == IMAGE_TYPE:
        min_seed = min_seed if min_seed > 10 else 10
        labels = Label.objects.filter(project__id=project_id)
        has_enough = all(Seed.objects
                         .filter(label=label).count() >= min_seed
                         for label in labels)
        return label_count == Label.objects.filter(project__id=project_id) \
                                           .count() and has_enough


def has_classifier(project_id):
    return Classifier.objects.filter(project__id=project_id,
                                     is_accuracy=False).count() > 0


def get_seed_data(project_id):
    project_seeds = Seed.objects.filter(data__project__id=project_id)
    seed = [
        {
            "content": s.data.content,
            "label": s.label
        }
        for s in project_seeds
    ]
    return seed


def create_csv_file(seed, fieldnames):
    """ Creates csv file from dB to train classifier """
    file_path = SEED_DIR
    with open(file_path, "w") as outfile:
        wr = csv.DictWriter(outfile, fieldnames)
        for i in seed:
            wr.writerow(i)
    return file_path


def get_vr_seed_data(project_id, last_updated=None):
    label_ids = []
    if last_updated is None:
        label_ids = Seed.objects.filter(data__project__id=project_id) \
                                .values('label') \
                                .distinct()
    else:
        label_ids = Seed.objects.filter(date__gte=last_updated) \
                                .filter(data__project__id=project_id) \
                                .values('label') \
                                .distinct()
    labels = [Label.objects.get(id=label['label']) for label in label_ids]

    seed = {}
    pool_zip_num = 0
    for label in labels:
        if last_updated is None:
            contents = Seed.objects.filter(label=label,
                                           data__project__id=project_id)
        else:
            contents = Seed.objects.filter(label=label,
                                           data__project__id=project_id,
                                           date__gte=last_updated)

        zipname = VR_SEED_DIR + 'seed_' + str(pool_zip_num) + '.zip'
        with zipfile.ZipFile(zipname, 'w') as seedfile:
            for content in contents:
                # first arg is the path for the file, 2nd one is the
                # name it'll be called internally
                seedfile.write(str(BUCKET_DIR + content.data.content),
                               content.data.content)
        seed[label.label] = zipname  # {'cat': seed_<date>.zip, 'dog': ...}
        pool_zip_num += 1
    return seed


def create_nlc_classifier(project_id):
    """
    creates a new nlco, gets data from db labelled as seed and begins
    training classifier
    """
    seed = get_seed_data(project_id)
    seed_csv = create_csv_file(seed, ['content', 'label'])
    nlco.create_and_fit(seed_csv, project_id)


def create_vr_classifier(project_id):
    """
    Creates a new classifier instance, gets data from dB labelled
    as seed and begins training classifier
    """

    seed = get_vr_seed_data(project_id)
    vro.create_and_fit(project_id, seed)


def create_training_classifier(project_id):
    project = Project.objects.get(id=project_id)
    if project.data_type.type_name == TEXT_TYPE:
        create_nlc_classifier(project_id)
    elif project.data_type.type_name == IMAGE_TYPE:
        create_vr_classifier(project_id)


def update_predict_proba(project_id, classifier_id):
    """ Updates predict proba values on dB """
    pool = Pool.objects.filter(data__project__id=project_id)
    project_type = Project.objects.get(id=project_id).data_type.type_name
    if project_type == TEXT_TYPE:
        predictions = nlco.classify(classifier_id, pool, project_id)
    elif project_type == IMAGE_TYPE:
        predictions = vro.classify(classifier_id, pool, project_id)
    else:
        raise ValueError('Unkown data type {}'.format(project_type))

    with transaction.atomic():
        PredictProba.objects.filter(label__project__id=project_id).delete()
        for data_id, value in predictions.items():
            pool = Pool.objects.get(data__id=data_id)
            for label, proba in value.items():
                label_obj = Label.objects.get(project__id=project_id,
                                              label=label)
                PredictProba(pool=pool, label=label_obj, proba=proba).save()


def text_swap_classifiers(project_id):
    clf = Classifier.objects.get(project__id=project_id, is_accuracy=False)
    update_predict_proba(project_id, clf.ibm_classifier_id)
    nlco.delete_classifier(clf.ibm_classifier_id, project_id)
    create_training_classifier(project_id)


def image_swap_classifiers(project_id):
    seed_files = os.listdir(VR_SEED_DIR)
    if seed_files:
        for seed_file in seed_files:
            os.remove(VR_SEED_DIR + seed_file)
    clf = Classifier.objects.get(project__id=project_id, is_accuracy=False)
    update_predict_proba(project_id, clf.ibm_classifier_id)
    seed = get_vr_seed_data(project_id, clf.date)
    vro.update_classifier(clf.ibm_classifier_id, project_id, seed)


def update_seed(data_id, label_id, project_id, label):
    ''' wrapper necessary for mocking in tests '''
    async_update_seed.delay(data_id, label_id, project_id, label)


def sync_update_seed(data_id, label_id, project_id, label):
    '''
    Moves Data from Pool to Seed, and checks for classifier
    status, maybe calling the swap_classifier or creating a new one
    '''
    with transaction.atomic():
        Pool.objects.get(data__id=data_id).delete()
        data = Data.objects.get(id=data_id)
        label = Label.objects.get(id=label_id)
        new_seed = Seed.objects.create(
            data=data,
            label=label
        )

    project_type = Project.objects.get(id=project_id).data_type.type_name

    if project_type == IMAGE_TYPE:
        vro.download_data(project_id, data_id)

    if not has_classifier(project_id):
        if seed_is_good(project_id):
            create_training_classifier(project_id)

    else:
        training_classifier = Classifier.objects.get(project__id=project_id,
                                                     is_accuracy=False)
        if project_type == TEXT_TYPE:
            is_training = True
            try:
                is_training = nlco.is_training(training_classifier.ibm_classifier_id,
                                 project_id)
            except Exception as e:
                is_training = True 

            if not is_training:
                text_swap_classifiers(project_id)

        elif project_type == IMAGE_TYPE:
            is_training = True
            try:
                is_training = vro.is_training(training_classifier.ibm_classifier_id,
                                   project_id)
            except Exception as e:
                is_training = True
                
            if not is_training:
                image_swap_classifiers(project_id)
