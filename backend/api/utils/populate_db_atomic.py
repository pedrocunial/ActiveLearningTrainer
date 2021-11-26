import os
from api.models import Pool, Data, Label, PredictProba, Project, User, DataType
from django.db import transaction

MODULE_DIR = os.path.dirname(__file__)


def populate_db(name, data_type, user, labels, force_recreate=False):
    """
    uses pool.csv in order to populate all tables from the
    initial database (except seed, which will be empty at
    the start of the project)
    """
    with transaction.atomic():
        user = User.objects.get(username=user) if user \
                                          else User.objects.get(id=0)
        # TODO: check if type is image or text
        try:
            dtype = DataType.objects.get(type_name=data_type)
        except DataType.DoesNotExist:
            dtype = DataType(type_name=data_type)
            dtype.save()

        if force_recreate:
            try:
                Project.objects.get(name=name).delete()
            except Project.DoesNotExist:
                pass
        project = Project(name=name, data_type=dtype, user=user)
        project.save()

    read_pool = []
    with open(os.path.join(MODULE_DIR, './raw_pool.csv')) as f:
        read_pool = [line.strip().split(',')[0] for line in f.readlines()]

    with transaction.atomic():
        datas = []
        for data in read_pool:
            new_data = Data(content=data, project=project)
            new_data.save()
            datas.append(new_data)

    with transaction.atomic():
        pools = []
        for data in datas:
            new_pool = Pool(data=data)
            new_pool.save()
            pools.append(new_pool)

    with transaction.atomic():
        label_objs = []
        for label in labels:
            new_label = Label(label=label, project=project)
            new_label.save()
            label_objs.append(new_label)

    len_labels = len(labels)

    with transaction.atomic():
        for pool in pools:
            for label in label_objs:
                new_pp = PredictProba(proba=1/len_labels,
                                      label=label,
                                      pool=pool)
                new_pp.save()

    return project.id
