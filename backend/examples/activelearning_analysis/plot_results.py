import matplotlib.pyplot as plt
import numpy as np

with open("results_al.txt") as f:
    data = f.readlines()
    batch_size = data[0].split(",")[1].split(":")[1].strip()
    al_data = [float(x.split(",")[0].split(":")[1].strip()) for x in data[1:]]
    x_al = range(1, len(al_data) + 1)
    x_al = [int(x) * int(batch_size) for x in x_al]

with open("results_random.txt") as f:
    data = f.readlines()
    batch_size = data[0].split(",")[1].split(":")[1].strip()
    random_data = [float(x.split(",")[0].split(":")[1].strip()) for x in data[1:]]
    x_random = range(1, len(random_data) + 1)
    x_random = [int(x) * int(batch_size) for x in x_random]

plt.title("Comparação de acurácia entre Active Learning e treinamento tradicional com dados da Pinacoteca")
plt.xlabel("Número de amostras")
plt.ylabel("Acurácia(%)")
plt.axvline(x=1000, ymax=.77, color='b', linestyle='--')
plt.axvline(x=2500, ymax=.77, color='r', linestyle='--')
plt.plot(x_al, al_data, marker='o', color='b', label="Active Learning")
plt.plot(x_random, random_data, color='r', marker='o', label="Random")
plt.xticks(list(plt.xticks()[0]) + [1000, 2500])
plt.ylim(bottom=40, top=100)
plt.xlim(left=0, right=4000)
plt.legend(loc='upper left')
plt.show()

