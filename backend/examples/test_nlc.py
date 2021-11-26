from nlco import NLCO
import os
import time
import atexit

MODULE_DIR = os.path.dirname(__file__)
cred = os.path.join(MODULE_DIR, '../credentials_marcelo.txt')
pool = os.path.join(MODULE_DIR, '../pool.csv')
seed = os.path.join(MODULE_DIR, '../seed.csv')

nlc = NLCO(cred)
nlc.create_and_fit(seed)

while True:
    is_training = nlc.is_training()
    if not is_training:
        break
    time.sleep(20)

classes = nlc.classify(pool)
print(classes)

def delete():
    print("delete")
    nlc.delete_classifier()

atexit.register(delete)