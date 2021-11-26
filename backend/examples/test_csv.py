import os
MODULE_DIR = os.path.dirname(__file__)

test_obj = [
    {
        'content': 'Teste1',
        'label': 'Amigaol'
    },
    {
        'content': 'Teste2',
        'label': 'Amigao2'
    },
    {
        'content': 'Teste3',
        'label': 'Amigao3'
    }

]

def _create_csv_file(seed):
    """ Creates csv file from dB to train classifier"""
    import csv
    file_path = os.path.join(MODULE_DIR, './seed.csv')
    fieldnames = ['content', 'label']
    with open("seed.csv", "w") as outfile:
        wr = csv.DictWriter(outfile, fieldnames)
        for i in seed:
            wr.writerow(i)
    return file_path

path = _create_csv_file(test_obj)
print(path)