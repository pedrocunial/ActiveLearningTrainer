import json
import random
import time

import numpy as np
from watson_developer_cloud import NaturalLanguageClassifierV1


from api.libs.nlco import NLCO

class ActiveLearningCycle:
    """Wrap active learning algorithm"""
    def __init__(self, pool_file, seed_file):
        self.pool_file = pool_file
        self.seed_file = seed_file

    def update_dataset(self, new_seed):
        """Update seed with newly labelled seed and remove from pool"""
        with open(self.seed_file, "a") as f:
            for line in new_seed:
                f.write(line)
                f.write("\n")

        with open(self.pool_file, "r+") as f:
            lines = f.readlines()
            f.seek(0)

            for line in lines:
                if line not in new_seed:
                    f.write(line)

            f.truncate()

    def random_pool(self, batch_size):
        """Select <batch_size> random instances"""
        with open(self.pool_file, 'r+') as f:
        
            instances = [i.strip("\n") for i in f.readlines()]

            if batch_size > len(instances):
                batch_size = len(instances)
            
            # Select random instances and respective index
            random_instances = random.sample(instances, batch_size)
            random_idxs = [instances.index(i) for i in random_instances]

            # Got to start of file
            f.seek(0)

            # Remove randomly selected instances from original file
            for instance in instances:
                if instance not in random_instances:
                    f.write(instance)
                    f.write("\n")

            # Remove everything after the last write
            f.truncate()

        return random_idxs, random_instances

    def probabilities(self, classification):
        """Get class probability for each instance"""
        collecting_labels = True
        labels = set()
        sample_text = []
        predict_probas = []

        for instance in classification['collection']:
            for class_ in instance["classes"]:
                labels.add(class_['class_name'])

            instance_probabilities = [0] * len(labels)
            
            for class_ in instance["classes"]:
                idx = list(labels).index(class_["class_name"])
                instance_probabilities[idx] = class_['confidence']

            sample_text.append(instance["text"])
            predict_probas.append(instance_probabilities)

        return labels, predict_probas, sample_text

    def get_least_confident_instances(self, classification, batch_size):
        """Get indexes of instances matching least confident criteria"""
        labels, probabilities, sample_text = self.probabilities(classification)
        
        instances = []

        # Get highest probability for each instance
        max_prop = np.amax(probabilities, axis=1)

        # Partial sorting (sort only <batch_size> elements)
        sorted_idx = np.argpartition(max_prop, batch_size)

        # Return only sorted instances
        min_idx = sorted_idx[:batch_size]

        with open(self.pool_file, "r") as pool_file:
            lines = [l.strip("\n") for l in pool_file.readlines()]

            for idx in min_idx:
                instances.append((idx, lines[idx]))
        
        return instances
