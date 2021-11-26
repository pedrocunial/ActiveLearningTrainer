from watson_developer_cloud import NaturalLanguageClassifierV1


credentials = []

with open("../credentials/credentials.txt", "r") as cred:
	credentials = [i for i in cred.readlines()]

nlc = NaturalLanguageClassifierV1(
	username=credentials[0],
	password=credentials[1],
	url=credentials[2]
)

# Need to create this file before running
with open("test_seed.csv") as seed:
	classifier = nlc.create_classifier(
		training_data=seed,
		metadata='{"language":"en"}'
	)

print(classifier) 

