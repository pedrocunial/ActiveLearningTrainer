import pandas as pd
from sklearn.model_selection import train_test_split
from watson_developer_cloud import NaturalLanguageClassifierV1
import time
from random import shuffle


def get_credentials():
    with open("credentials_nlc.txt") as f:
        credentials = f.readlines()
    api_key, url = [x.strip() for x in credentials]
    return (api_key, url)


def create_seed_file(seed, filename):
    seed.to_csv(filename, header=False, index=False)

def create_nlc(api_key, url):
    print(api_key, url)
    nlc = NaturalLanguageClassifierV1(
        iam_apikey=api_key,
        url=url
    )
    return nlc

def read_data():
    print("Lendo dados")
    data = pd.read_csv("porco.csv")
    data = data.replace("raça_ porco", "raça_porco")
    data["Example"] = data["Example"].str.lower()
    data = data.drop_duplicates(subset=["Example"])
    return data

def create_classifier(nlc, filename):
    print("Criando classificador")
    with open(filename, 'rb') as training_data:
        classifier = nlc.create_classifier(
            training_data=training_data,
            metadata='{"name": "My ClassifiClassificaer","language": "pt"}'
        ).get_result()
        return classifier['classifier_id']

def get_predictions(nlc, classifier_id, pool):
    print("Classificando amostras")
    pool_list = pool["Example"].tolist()
    examples = [{"text": x} for x in pool_list]
    small_examples = [examples[x:x+30] for x in range(0, len(examples), 30)]
    all_classes = []
    result = []
    for i in small_examples:
        classes = nlc.classify_collection(classifier_id, i).get_result()
        all_classes += [classes]
    for i in all_classes:
        for j in i['collection']:
            obj = {"text": j['text'], 
                    "confidence": j["classes"][0]["confidence"]}
            result.append(obj)
    return result
    
def calc_accuracy(nlc, classifier_id, test):
    test_list = test["Example"].tolist()
    examples = [{"text": x} for x in test_list]
    small_examples = [examples[x:x+30] for x in range(0, len(examples), 30)]
    all_classes = []
    right = 0
    for i in small_examples:
        classes = nlc.classify_collection(classifier_id, i).get_result()
        all_classes += [classes]
    for i in all_classes:
        for j in i['collection']: 
            predicted_label = j["classes"][0]["class_name"]
            real_label = test.loc[test['Example'] == j['text'], 'Class Name'].iloc[0]
            if predicted_label == real_label:
                right += 1
    accuracy = right / test.shape[0]
    return accuracy


def get_least_confident(batch_size, predictions):
    least_confident = sorted(predictions, 
       key=lambda k: k['confidence'])[0:batch_size]
    return least_confident


def get_random(batch_size, predictions):
    shuffle(predictions)
    least_confident = predictions[0:batch_size]
    return least_confident

def update_pool_and_seed(least_confident, pool, seed):
    samples = pd.DataFrame(columns=['Example', 'Class Name'])
    for i in least_confident:
        sample = pool.loc[pool['Example'] == i['text']]
        samples = samples.append(sample)
    for index, row in samples.iterrows():
        pool = pool.drop([index])
        seed = seed.append(row)
    return (pool, seed)


def check_nlc_training(nlc, classifier_id):
    print("NLC Treinando")
    status = nlc.get_classifier(classifier_id).get_result()
    return status['status'] == "Training"


def print_accuracy(accuracy, epoch, is_al):
    if is_al:
        with open("results_al.txt", "a") as f:
            f.write("Accuracy: {0:.2f}, Epoch: {1} \n".format(accuracy*100, epoch))
        print("AL: Acurácia na epoch {0}: {1:.2f}%".format(epoch, accuracy*100))
    else:
        with open("results_random.txt", "a") as f:
            f.write("Accuracy: {0:.2f}, Epoch: {1} \n".format(accuracy*100, epoch))
        print("Random: Acurácia na epoch {0}: {1:.2f}%".format(epoch, accuracy*100))


def delete_classifier(nlc, classifier_id):
    print("Deletando classificador")
    nlc.delete_classifier(classifier_id).get_result()

def main(nlc, train, test,  uses_al, initial_size=0.98, batch_size=100):
    if uses_al:
        filename = "seed_al.csv"
        with open("results_al.txt", "w") as f:
            f.write("Results Active Learning, Batch Size : {0}\n".format(batch_size)) 
    else:
        with open("results_random.txt", "w") as f:
            f.write("Results Random , Batch Size : {0}\n".format(batch_size)) 
        filename = "seed_random.csv"
    epoch = 0
    seed, pool = train_test_split(train, test_size=initial_size, random_state=42)
    create_seed_file(seed, filename)
    classifier_id = create_classifier(nlc, filename)
    while True:
        if not check_nlc_training(nlc, classifier_id):
            break
        time.sleep(30)
    predictions = get_predictions(nlc, classifier_id, pool)
    accuracy = calc_accuracy(nlc, classifier_id, test)
    print_accuracy(accuracy, epoch, uses_al)
    while pool.shape[0] > batch_size:
        if uses_al:
            least_confident = get_least_confident(batch_size, predictions)
        else:
            least_confident = get_random(batch_size, predictions)
        pool, seed = update_pool_and_seed(least_confident, pool, seed)
        create_seed_file(seed, filename)
        delete_classifier(nlc, classifier_id)
        classifier_id = create_classifier(nlc, filename)
        epoch += 1
        while True:
            if not check_nlc_training(nlc, classifier_id):
                break
            time.sleep(30)
        predictions = get_predictions(nlc, classifier_id, pool)
        accuracy = calc_accuracy(nlc, classifier_id, test)
        print_accuracy(accuracy, epoch, uses_al)
