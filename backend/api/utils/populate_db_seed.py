import os
from api.models import Pool, Data, Label, PredictProba, Project, User, DataType, Seed
from django.db import transaction

MODULE_DIR = os.path.dirname(__file__)
BUCKET_DIR = os.path.join(MODULE_DIR, "../../bucket/")


def populate_db_seed(name, data_type, user, labels, force_recreate=False):
    """
    populates db upon creation of new project, with an initial
    seed that makes it easy to test the classifier module.
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


    if data_type == "text": 
        with open(os.path.join(MODULE_DIR, './raw_pool.csv')) as f:
            read_pool = [line.strip().split(',')[0] for line in f.readlines()]
    
    elif data_type == "image": 
        read_pool = [filename for filename in os.listdir(BUCKET_DIR)]


    

    with transaction.atomic():
        datas = []
        for data in read_pool:
            new_data = Data(content=data, project=project)
            new_data.save()
            datas.append(new_data)
    
    with transaction.atomic():
        label_objs = []
        for label in labels:
            new_label = Label(label=label, project=project)
            new_label.save()
            label_objs.append(new_label)
    

    label = [Label.objects.filter(project__id=project.id).get(label=label_value) for label_value in labels]
    label_idx = 0
    counter = 1
    with transaction.atomic():
        for data in Data.objects.all().filter(project__id=project.id)[0:30]:
            new_seed = Seed(data=data, label=label[label_idx])
            new_seed.save()
            if counter % 10 == 0:
                label_idx += 1
                counter = 1
            else:
                counter+=1

    with transaction.atomic():
        pools = []
        for data in Data.objects.filter(project__id=project.id).all()[30:]:
            new_pool = Pool(data=data)
            new_pool.save()
            pools.append(new_pool)

    len_labels = len(labels)

    with transaction.atomic():
        for pool in pools:
            for label in label_objs:
                new_pp = PredictProba(proba=1/len_labels,
                                      label=label,
                                      pool=pool)
                new_pp.save()

    return project.id

