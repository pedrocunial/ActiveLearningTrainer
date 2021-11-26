from watson_developer_cloud import NaturalLanguageClassifierV1
from concurrent.futures import ThreadPoolExecutor, as_completed

import json


BATCH_SIZE = 30


credentials = []

with open("../credentials/credentials.txt", "r") as cred:
    credentials = [i.strip() for i in cred.readlines()]

nlc = NaturalLanguageClassifierV1(
    username=credentials[0],
    password=credentials[1],
    url=credentials[2]
)

# # Need to create this file before running
texts = []
with open("./dataset/nlc.csv", 'rb') as seed:
    try:
        classifier = nlc.create_classifier(
            training_data=seed,
            metadata='{"name":"nlc0", "language": "en"}'
        )
    except Exception as e:
        print(e)
        exit(0)

with open('dataset/nlc.csv', 'r') as seed:
    texts = [line.strip().split(',')[0] for line in seed.readlines()]

# print(classifier)
classifier_id = 'f3342ax453-nlc-837'
status = nlc.get_classifier(classifier_id)
print(status)
print(json.dumps(status, indent=2))

with ThreadPoolExecutor(max_workers=4) as executor:
    batches = []
    for i in range(0, len(texts), BATCH_SIZE):
        batch = []
        for text in texts[i:i + BATCH_SIZE if i + BATCH_SIZE <= len(texts)
                          else len(texts)+1]:
            batch.append({'text': text})
        batches.append(batch)

    print(batches)
    future_to_url = {
        executor.submit(nlc.classify_collection, classifier_id, batch): batch
        for batch in batches
    }

    results = []
    for future in as_completed(future_to_url):
        try:
            print(future.result())
            results.append(future.result())
        except Exception as exc:
            print(exc)

    print('done!')
    print('results:', results)
