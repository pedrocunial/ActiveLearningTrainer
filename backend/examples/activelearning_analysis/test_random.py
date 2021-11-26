import utils as utils

api_key, url = utils.get_credentials()
nlc = utils.create_nlc(api_key, url)
data = utils.read_data()
train, test = utils.train_test_split(data, test_size=0.2, random_state=42)
utils.main(nlc, train, test, False)