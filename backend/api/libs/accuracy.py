from sklearn.model_selection import train_test_split
from django.db import transaction
import os
import zipfile
import csv
from django.db.models import Count

from api.models import (
    Classifier, 
    Project, 
    Seed, 
    Label, 
    Accuracy, 
    SampleFrequency)
import api.libs.vro as vro
import api.libs.nlco as nlco
import api.libs.classifier as classifier

from main.celery import async_init_accuracy, async_update_accuracy

WA_TYPE = 'wa'
MODULE_DIR = os.path.dirname(__file__)
NEGATIVE_SEED = os.path.join(MODULE_DIR, '../temp_data/negative.zip')
SEED_DIR = os.path.join(MODULE_DIR, '../temp_data/')

TRIED_STARTED_CLF = -1
RESTARTED_CLF_IF_READY = -2
INVALID_PROJECT_TYPE = -3
ALREADY_UPDATING_CLF = -4

def has_accuracy_clf(project_id):
    return Classifier.objects.filter(project__id=project_id,
                                     is_accuracy=True).exists()


def has_accuracy_data(project_id):
    return Seed.objects.filter(data__project__id=project_id,
                               is_train=None).exists()


def is_ready(project_id):
    ''' check if the project's accuracy clf is done training '''
    project_type = Project.objects.get(id=project_id).data_type.type_name
    clf = Classifier.objects.get(project__id=project_id, is_accuracy=True)
    if project_type == classifier.TEXT_TYPE:
        is_training = True
        try:
            is_training = nlco.is_training(clf.ibm_classifier_id,
                             project_id)
        except Exception as e:
            is_training = True 

        return not is_training
    elif project_type == classifier.IMAGE_TYPE:
        is_training = True
        try:
            is_training = vro.is_training(clf.ibm_classifier_id,
                               project_id)
        except Exception as e:
            is_training = True
        return not is_training
    elif project_type == WA_TYPE:
        return True  # TODO:
    else:
        raise ValueError(
            'Unaccepted data type {} for opperation'.format(project_type))


def create_csv_file(seed, filename, fieldnames):
    """ Creates csv file from dB to train classifier """
    file_path = os.path.join(SEED_DIR, filename)
    with open(file_path, "w") as outfile:
        wr = csv.DictWriter(outfile, fieldnames)
        for i in seed:
            wr.writerow(i)
    return file_path


def seed_is_good(project_id, min_seed=6):
    """
    Checks if seed content is within minimum required for classifier creation
    """
    project = Project.objects.get(id=project_id)
    label_count = Seed.objects.filter(label__project__id=project_id,
                                      is_train=True) \
                              .order_by() \
                              .values('label') \
                              .distinct() \
                              .count()

    if project.data_type.type_name == classifier.TEXT_TYPE:
        label_db_count = Label.objects.filter(project__id=project_id).count()
        seed_count = Seed.objects.filter(label__project__id=project_id,
                                         is_train=True).count()
        return label_count == label_db_count and seed_count >= min_seed

    elif project.data_type.type_name == classifier.IMAGE_TYPE:
        min_seed = min_seed if min_seed > 10 else 10
        labels = Label.objects.filter(project__id=project_id)
        has_enough = all(Seed.objects.filter(label=label, is_train=True)
                     .count() >= min_seed for label in labels)
        return (label_count == Label.objects.filter(project__id=project_id)
                .count()) and has_enough


def split_seed(project_id, last_updated=None):
    ''' split seed into train and test datasets '''
    if last_updated is None:
        seed = list(Seed.objects.filter(data__project__id=project_id))
    else:
        seed = list(Seed.objects.filter(data__project__id=project_id,
                                        date__gte=last_updated))
    return train_test_split(seed)


def save_train_test_split(train, test):
    with transaction.atomic():
        for tr in train:
            tr.is_train = True
            tr.save()
        for te in test:
            te.is_train = False
            te.save()


def format_seed(project_id):
    seed = Seed.objects.filter(
               data__project__id=project_id,
               is_train=True)

    return [{'content': s.data.content,
             'label': s.label} for s in seed]


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
            contents = Seed.objects.filter(
                label=label, data__project__id=project_id,
                is_train=True)
        else:
            contents = Seed.objects.filter(
                label=label, data__project__id=project_id,
                date__gte=last_updated, is_train=True)

        zipname = classifier.VR_SEED_DIR + 'seed_' + str(pool_zip_num) + '.zip'
        with zipfile.ZipFile(zipname, 'w') as seedfile:
            for content in contents:
                # first arg is the path for the file, 2nd one is the
                # name it'll be called internally
                seedfile.write(str(classifier.BUCKET_DIR +
                                   content.data.content),
                               content.data.content)
        # {'cat': seed_<pool_zip_num>.zip, 'dog': ...}
        seed[label.label] = zipname
        pool_zip_num += 1
    return seed


def get_test_data(project_id):
    return Seed.objects.filter(data__project__id=project_id,
                               is_train=False)


def get_train_data(project_id):
    return Seed.objects.filter(data__project__id=project_id,
                               is_train=True)

def set_updating_acc_off(project_id):
    project = Project.objects.get(id=project_id)
    project.is_updating_acc = False
    project.save()

def update_accuracy(project_id):
    project = Project.objects.get(id=project_id)
    project_type = project.data_type.type_name

    clf = Classifier.objects.get(project__id=project_id, is_accuracy=True)
    train, test = split_seed(project_id, clf.date)
    save_train_test_split(train, test)
    
    if project_type == classifier.TEXT_TYPE:
        nlco.delete_classifier(clf.ibm_classifier_id,
                               project_id, is_accuracy=True)
        train = get_train_data(project_id)
        train = format_seed(train)
        train_csv = create_csv_file(train, 'train.csv', ['content', 'label'])
        nlco.create_and_fit(train_csv, project_id, is_accuracy=True)
    elif project_type == classifier.IMAGE_TYPE:
        train_formated = get_vr_seed_data(project_id, last_updated=clf.date)
        vro.update_classifier(clf.ibm_classifier_id, project_id,
                              train_formated, is_accuracy=True)

    project.is_updating_acc = False
    project.save()


def init_accuracy(project_id):
    project = Project.objects.get(id=project_id)
    project_type = project.data_type.type_name
    
    if project_type == classifier.TEXT_TYPE:
        train = format_seed(project_id)
        train_csv = create_csv_file(train, 'train.csv', ['content', 'label'])
        nlco.create_and_fit(train_csv, project_id, is_accuracy=True)
    elif project_type == classifier.IMAGE_TYPE:
        train_formated = get_vr_seed_data(project_id, last_updated=None)
        vro.create_and_fit(project_id, train_formated,
                           is_accuracy=True)
    
    project.is_updating_acc = False
    project.save()



def calculate_accuracy(project_id):
    project = Project.objects.get(id=project_id)
    project_type = project.data_type.type_name
    

    test = list(get_test_data(project_id))
    clf = Classifier.objects.get(project__id=project_id,
                                 is_accuracy=True)
    
    if project_type == classifier.TEXT_TYPE:
        predictions = nlco.classify(clf.ibm_classifier_id, test, project_id)
    elif project_type == classifier.IMAGE_TYPE:
        predictions = vro.classify(clf.ibm_classifier_id, test, project_id)

    rights = 0
    for key, value in predictions.items():
        expected = Seed.objects.get(data__id=key).label.label
        predicted = max(value, key=value.get)
        if predicted == expected:
            rights += 1

    project = Project.objects.get(id=project_id)
    accuracy = rights / len(predictions)
    new_accuracy = Accuracy.objects.create(
        project=project,
        accuracy=accuracy
    )
    new_accuracy.save()

    save_samples_frequencies(new_accuracy, project_id)

def save_samples_frequencies(accuracy, project_id):
    seed = Seed.objects.filter(data__project__id=project_id) \
                       .values("label") \
                       .annotate(freq=Count("label"))

    for elem in seed:
        label = Label.objects.get(id=elem["label"])
        new_sample_freq = SampleFrequency.objects.create(
            accuracy=accuracy,
            label=label,
            frequency=elem["freq"]
        )
        new_sample_freq.save() 


def get_accuracy_history(project_id):
    return Accuracy.objects.filter(project__id=project_id)


def get_samples_frequencies(accuracy_id):
    return SampleFrequency.objects.filter(accuracy__id=accuracy_id)


def check_update_accuracy_state(project_id):
    project = Project.objects.get(id=project_id)
    project_type = project.data_type.type_name
    
    if project_type == WA_TYPE:
        return INVALID_PROJECT_TYPE

    if project.is_updating_acc:
        return ALREADY_UPDATING_CLF

    project.is_updating_acc = True
    project.save()
    
    if not has_accuracy_clf(project_id):
        async_init_accuracy.delay(project_id) #after done, changes is_updating_acc to false
        return TRIED_STARTED_CLF

    if has_accuracy_data(project_id) or (not get_accuracy_history(project_id).exists()):
        async_update_accuracy.delay(project_id) #after done, changes is_updating_acc to false
        return RESTARTED_CLF_IF_READY

    project.is_updating_acc = False
    project.save()