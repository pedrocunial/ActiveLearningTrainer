from examples.populate_utils import get_data
from api.models import Data, Label, Pool, PredictProba, Seed


data = get_data()
texts = data.keys()
labels = ['temperature', 'contitions']

datas = [Data(content=text) for text in texts]
for d in datas:
    try:
        d.save()
    except Exception as e:
        print(f'could not save {d}')

labels = [Label(label=label) for label in labels]
for d in labels:
    try:
        d.save()
    except Exception as e:
        print(f'could not save {d}')

for text in texts:
    data_obj = Data.objects.get(content=text)
    pool = Pool(data=data_obj)
    pool.save()
    std_proba = 1 / len(labels)
    lps = [PredictProba(pool=pool, label=Label.objects.get(label=label),
                        proba=std_proba) for label in labels]
    for d in lps:
        try:
            d.save()
        except Exception as e:
            print(f'could not save {d}')

for p in Pool.objects.all():
    try:
        Seed.objects.get(data=p.data).delete()
    except Exception as e:
        print(f'{p} wasnt in seed')
