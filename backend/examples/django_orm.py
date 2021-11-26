'''
usando:

python manage.py shell < ./exemples/django_orm.py


Comandos basicos do ORM ('super DAO' do django)

Vale lembrar que os imports são absolutos do projeto, portanto, deve-se
utilizar exatamente os mesmos do exemplo em qualquer arquivo do mesmo
(poupando o 'import *' quando nao necessario, claro)
'''

# todos os models devem estar disponives neste arquivo (seja diretamente ou
# por imports dentro do mesmo)
from api.models import PredictProba, Label, Data, Pool, Seed

# para limpar a DB por completo, defina a flag should_nuke como True
# nao faca isso mais pra frente, use apenas para testes
should_nuke = False
if should_nuke:
    PredictProba.objects.all().delete()
    Label.objects.all().delete()
    Data.objects.all().delete()
    Pool.objects.all().delete()
    Seed.objects.all().delete()


# aqui comeca o exemplo 'normal': criando dados novos na db
data = Data(content='ontem choveu a tarde inteira')
data2 = Data(content='ontem fez 42 graus!')

# dados ainda nao foram salvos na db
data.save()
print('data criado:', data)
data2.save()
print('data2 criado:', data2)

# select generico
datas = Data.objects.all()
# o atributo __str__ dos models foram sobrescritos para
# melhor representacao dos mesmos
print('datas (resultado da query .all()): ', datas)


labels = [
    Label(label='temperatura'),
    Label(label='condicao')
]
for label in labels:
    label.save()
    print('label criada:', label)


# tanto o seed quanto o pool possuem uma chave extrangeira, para isso
# deve-se utilizar objetos do proprio django para definir o valor da
# mesma (ao contrario do tradicional id)
data = Data.objects.get(content='ontem choveu a tarde inteira')

seed = Seed(data=data, label=labels[1])
seed.save()
print('seed criado:', seed)

pool = Pool(data=data2)
pool.save()
print('pool criado:', pool)


# o PredictProba eh mais chatinho: possui uma chave extrangeira de
# uma tabela criata unica e exclusivamente para garantir que o par
# label-pool sera unico dentro de um predicproba. alem disso, possui um campo
# decimal. existem motivos para utilizar tanto o campo decimal, quanto o
# float, acabei optando pelo decimal por parecer ser o prefirido da comunidade
# devido a maior precisao aritmetica (uma vez que guarda os valores como
# inteiros multiplicados por um numero e, na hora de sua representacao, os
# divide).

# criando o predictproba
probas = [
    PredictProba(proba=0.67, label=labels[0], pool=pool),
    PredictProba(proba=0.33, label=labels[1], pool=pool)
]
for proba in probas:
    proba.save()
    print('predictproba criado:', proba)


# o 'select' de uma coluna apenas pode ser feito com o metodo
# only('nome da coluna'); da mesma forma, o select de todas menos uma coluna
# pode ser feito com o defer('nome da coluna a ser ignorada'). tanto o only
# quanto o defer aceitam mais de um argumento (mais de uma coluna a ser
# selecionada, ou mais de uma a ser ignorada), assim:
somente_probas = PredictProba.objects.only('proba')
print('objetos com somente a coluna probas:', somente_probas)

# repare que ele criou um objeto por completo, no entanto, somente a coluna
# de probas foi selecionada na query, enquanto as outras so serao buscadas
# quando necessario (no caso, foi necessario buscar as outras colunas para
# criar o print do objeto, mas vamos fingir que nao)
soma_probas = sum([proba.proba for proba in somente_probas])
print('total das probas:', soma_probas)
