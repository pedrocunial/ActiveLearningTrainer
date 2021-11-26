import mock
import json
import random
from django.test import TestCase, Client
from django.db.models import Sum
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from api.libs.accuracy import (
    get_accuracy_history,
    get_samples_frequencies,
    check_update_accuracy_state,
    TRIED_STARTED_CLF,
    RESTARTED_CLF_IF_READY,
    INVALID_PROJECT_TYPE,
    ALREADY_UPDATING_CLF
)
from api.models import (
    Seed,
    Data,
    Label,
    DataType,
    Project,
    ProjectHasUser,
    User,
    Accuracy, 
    SampleFrequency, 
    ProjectHasUser)


API_BASE_PATH = "/api/v1"


class ProjectTestCase(TestCase):

    def setUp(self):
        dtype = DataType.objects.create(type_name='test')
        Project.objects.create(data_type=dtype, name='Test Project')

    def test_project_exists(self):
        self.assertTrue(Project.objects.filter(name='Test Project').exists())

    def test_project_type(self):
        project = Project.objects.get(name='Test Project')
        dtype = DataType.objects.get(type_name='test')
        self.assertEqual(project.data_type.type_name, dtype.type_name)


class LoginViewTest(TestCase):
    """
    Tests to check integrity of LoginView.

    Test List:
        - Login user
        - Login user with incorrect credentials
    """
    
    def setUp(self):
        self.TEST_CLASS_PATH = API_BASE_PATH + "/login"
        self.client = Client()

        self.user = User.objects.create(
            username='makelele.prime@ea.com',
            email='makelele.prime@ea.com',
            first_name='Makelele Prime',
            password=make_password('secreto.1234', hasher='pbkdf2_sha256')
        )

        self.token = Token.objects.get_or_create(user=self.user)[0].key

    def test_login_user(self):
        path = API_BASE_PATH + "/login"

        data = {
            'username': 'makelele.prime@ea.com',
            'password': 'secreto.1234'
        }

        resp = self.client.post(
            path,
            data,
            content_type='application/json'
        )

        resp_body = resp.json()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_body['uid'], self.user.id)
        self.assertEqual(resp_body['token'], self.token)

    def test_login_user_incorrect_credentials(self):
        path = API_BASE_PATH + "/login"
        
        data = {
            'username': 'makelele.prime@ea.com',
            'password': 'secreto'
        }

        resp = self.client.post(
            path,
            data,
            content_type='application/json'
        )

        resp_body = resp.json()

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp_body['message'], "Incorrect credentials.")


class UserViewTest(TestCase):
    """
    Tests to check integrity of UserView.

    Test List:
        - Create user
        - Create user duplicate
        - List users
    """

    def setUp(self):
        self.TEST_CLASS_PATH = API_BASE_PATH + "/users"
        self.client = Client()

        self.user = User.objects.create(
            username='makelele.prime@ea.com',
            email='makelele.prime@ea.com',
            first_name='Makelele Prime',
            password=make_password('secreto.1234', hasher='pbkdf2_sha256')
        )

        self.token = Token.objects.get_or_create(user=self.user)[0].key

    def test_create_user(self):
        path = self.TEST_CLASS_PATH

        data = {
            'username': 'fred.flintstones@cartoonnetwork.com',
            'password': 'secreto.1234',
            'name': 'Fred Flintstone'
        }

        resp = self.client.post(
            path,
            data,
            content_type="application/json"
        )

        self.assertEqual(resp.status_code, 201)

    def test_create_duplicated_user(self):
        path = self.TEST_CLASS_PATH

        data = {
            'username': 'makelele.prime@ea.com',
            'password': 'secreto.1234',
            'name': 'Makelele Prime'
        }

        resp = self.client.post(
            path,
            data,
            content_type="application/json"
        )

        self.assertEqual(resp.status_code, 409)

    def test_list_users(self):
        path = self.TEST_CLASS_PATH

        resp = self.client.get(
            path
        )

        resp_body = resp.json()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_body['message'], 'Users found')
        self.assertEqual(len([u for u in resp_body['content']
                              if u['id'] == self.user.id]), 1)


class UserDetailViewTest(TestCase):
    """
    Tests to check integrity of UserDetailView.

    Test List:
        - List, Update, Delete invalid user
        - List, Update, Delete valid user
        - Update valid user with bad formatted data
        - List, Update, Delete valid user not having permission
    """

    def setUp(self):
        self.TEST_CLASS_PATH = API_BASE_PATH + "/users"
        self.client = Client()
        
        self.user = User.objects.create(
            username='chocotone@limao.com.vc',
            email='chocotone@limao.com.vc',
            first_name='Chocotone De Limao',
            password=make_password('secreto.1234', hasher='pbkdf2_sha256')
        )
        
        self.token = Token.objects.get_or_create(user=self.user)[0].key

    def test_list_invalid_user(self):
        path = self.TEST_CLASS_PATH + "/999999999"
        
        response = self.client.get(
            path,
            HTTP_AUTHORIZATION=f"Token {self.token}"
        )
        
        self.assertEqual(response.status_code, 404)

    def test_update_invalid_user(self):
        path = self.TEST_CLASS_PATH + "/999999999"
        
        data = {
            "password": "12345678"
        }

        response = self.client.put(
            path,
            data,
            HTTP_AUTHORIZATION=f"Token {self.token}",
            content_type="application/json"
        )
        
        self.assertEqual(response.status_code, 404)

    def test_delete_invalid_user(self):
        path = self.TEST_CLASS_PATH + "/999999999"
        
        response = self.client.delete(
            path,
            HTTP_AUTHORIZATION=f"Token {self.token}"
        )
        
        self.assertEqual(response.status_code, 404)

    def test_list_valid_user(self):
        path = self.TEST_CLASS_PATH + f"/{self.user.id}"

        resp = self.client.get(
            path,
            HTTP_AUTHORIZATION=f"Token {self.token}"
        )

        resp_body = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_body['message'], 'User found')
        self.assertEqual(resp_body['content']['id'], self.user.id)
        self.assertEqual(resp_body['content']['email'], self.user.email)

    def test_update_valid_user(self):
        path = self.TEST_CLASS_PATH + f"/{self.user.id}"

        data = {
            "password": "12345678"
        }

        resp = self.client.put(
            path,
            data,
            HTTP_AUTHORIZATION=f"Token {self.token}",
            content_type="application/json"
        )

        self.assertEqual(resp.status_code, 204)

    def test_update_valid_user_bad_formatting(self):
        path = self.TEST_CLASS_PATH + f"/{self.user.id}"

        data = {
            "password": ""
        }

        resp = self.client.put(
            path,
            data,
            HTTP_AUTHORIZATION=f"Token {self.token}",
            content_type="application/json"
        )

        self.assertEqual(resp.status_code, 400)

    def test_delete_valid_user(self):
        path = self.TEST_CLASS_PATH + f"/{self.user.id}"

        resp = self.client.delete(
            path,
            HTTP_AUTHORIZATION=f"Token {self.token}",
            content_type="application/json"
        )

        self.assertEqual(resp.status_code, 204)

    def test_list_valid_user_without_permission(self):
        other_user = User.objects.create(
            username='takarada.rikka@gridman.ssss',
            email='takarada.rikka@gridman.ssss',
            password=make_password('secreto.1234', hasher='pbkdf2_sha256')
        )

        path = self.TEST_CLASS_PATH + f"/{other_user.id}"

        resp = self.client.get(
            path,
            HTTP_AUTHORIZATION=f"Token {self.token}"
        )

        self.assertEqual(resp.status_code, 403)

    def test_update_valid_user_without_permission(self):
        other_user = User.objects.create(
            username='takarada.rikka@gridman.ssss',
            email='takarada.rikka@gridman.ssss',
            password=make_password('secreto.1234', hasher='pbkdf2_sha256')
        )

        path = self.TEST_CLASS_PATH + f"/{other_user.id}"

        data = {
            "password": "12345678"
        }

        resp = self.client.put(
            path,
            data,
            HTTP_AUTHORIZATION=f"Token {self.token}",
            content_type="application/json"
        )

        self.assertEqual(resp.status_code, 403)

    def test_delete_valid_user_without_permission(self):
        other_user = User.objects.create(
            username='takarada.rikka@gridman.ssss',
            email='takarada.rikka@gridman.ssss',
            password=make_password('secreto.1234', hasher='pbkdf2_sha256')
        )

        path = self.TEST_CLASS_PATH + f"/{other_user.id}"

        resp = self.client.delete(
            path,
            HTTP_AUTHORIZATION=f"Token {self.token}",
            content_type="application/json"
        )

        self.assertEqual(resp.status_code, 403)


def populate_db_mock(project_name, data_type, labels, uid, workspace_id,
                     api_key, url, api_key_storage, instance_id, bucket_name,
                     url_endpoint):

    if data_type in ("image", "text", "wa") \
            and not Project.objects.filter(name=project_name).exists():
        return 1
    else:
        raise ValueError("Error message")


class ProjectViewTest(TestCase):
    """
    Tests to check integrity of ProjectView.

    Test List:
        - Create project
        - Create project duplicate
        - Create project with invalid parameters
    """
    
    def setUp(self):
        self.TEST_CLASS_PATH = API_BASE_PATH + "/projects"
        self.client = Client()

        self.owner = User.objects.create(
            username='babao@insper.edu.br',
            email='babao@insper.edu.br',
            first_name='Babao Rivers',
            password=make_password('bitekona', hasher='pbkdf2_sha256')
        )

        self.project = Project.objects.create(
            name="Neckless Corporation",
            data_type=DataType.objects.create(type_name="image")
        )

        self.token = Token.objects.get_or_create(user=self.owner)[0].key

    @mock.patch('api.views.populate_db', side_effect=populate_db_mock)
    def test_create_project(self, m):
        path = self.TEST_CLASS_PATH

        data = {
            "name": "Thomas the Little Train Project",
            "type": "text",
            "user_id": 1,
            "classifier_credentials": {
                "api_key": "abcd1234",
                "url": "http://example.com",
                "workspace_id": "1234abcd"
            },
            "storage_credentials": {
                "api_key_storage": "efgh5678",
                "instance_id": "76496543",
                "bucket_name": "testbucket"
            },
            "labels": []
        }

        resp = self.client.post(
            path,
            data,
            HTTP_AUTHORIZATION=f"Token {self.token}",
            content_type="application/json"
        )

        self.assertEqual(resp.status_code, 201)

    @mock.patch('api.views.populate_db', side_effect=populate_db_mock)
    def test_create_project_invalid_type(self, m):
        path = self.TEST_CLASS_PATH

        data = {
            "name": "Thomas the Little Train Project",
            "type": "asdfghjk",
            "user_id": 1,
            "classifier_credentials": {
                "api_key": "abcd1234",
                "url": "http://example.com",
                "workspace_id": "1234abcd"
            },
            "storage_credentials": {
                "api_key_storage": "efgh5678",
                "instance_id": "76496543",
                "bucket_name": "testbucket"
            },
            "labels": []
        }

        resp = self.client.post(
            path,
            data,
            HTTP_AUTHORIZATION=f"Token {self.token}",
            content_type="application/json"
        )

        self.assertEqual(resp.status_code, 400)

    @mock.patch('api.views.populate_db', side_effect=populate_db_mock)
    def test_create_duplicated_project(self, m):
        path = self.TEST_CLASS_PATH

        data = {
            "name": "Neckless Corporation",
            "type": "image",
            "user_id": 1,
            "classifier_credentials": {
                "api_key": "abcd1234",
                "url": "http://example.com",
                "workspace_id": "1234abcd"
            },
            "storage_credentials": {
                "api_key_storage": "efgh5678",
                "instance_id": "76496543",
                "bucket_name": "testbucket"
            },
            "labels": []
        }

        resp = self.client.post(
            path,
            data,
            HTTP_AUTHORIZATION=f"Token {self.token}",
            content_type="application/json"
        )

        self.assertEqual(resp.status_code, 400)
 

class ProjectDetailViewTest(TestCase):
    """
    Tests to check integrity of ProjectDetailView.

    Test List:
        - List, Update, Delete invalid project
        - List, Update, Delete valid project
        - Update valid project with bad formatted data
        - List, Update, Delete valid project not having permission
    """

    def setUp(self):
        self.TEST_CLASS_PATH = API_BASE_PATH + "/projects"
        self.client = Client()

        self.user1 = User.objects.create(
            username="marcelove@email.com",
            email="marcelove@email.com",
            first_name="Marcelove Bombaldoni",
            password=make_password('animeacademia', hasher='pbkdf2_sha256')
        )

        self.user2 = User.objects.create(
            username="thanos@pelotas.com",
            email="thanos@pelotas.com",
            first_name="Thanos Pelotas",
            password=make_password('vingadores', hasher='pbkdf2_sha256')
        )

        self.project = Project.objects.create(
            name="Molcajete",
            data_type=DataType.objects.create(type_name="image")
        )

        ProjectHasUser.objects.create(
            user=self.user1,
            project=self.project,
            permission=2
        )

        ProjectHasUser.objects.create(
            user=self.user2,
            project=self.project,
            permission=0
        )

        self.user1_token = Token.objects.get_or_create(user=self.user1)[0].key
        self.user2_token = Token.objects.get_or_create(user=self.user2)[0].key

    def test_list_invalid_project(self):
        path = self.TEST_CLASS_PATH + "/999999"

        resp = self.client.get(
            path,
            HTTP_AUTHORIZATION=f"Token {self.user1_token}"
        )

        self.assertEqual(resp.status_code, 406)

    def test_update_invalid_project(self):
        path = self.TEST_CLASS_PATH + "/999999"

        data = {
            "name": "Casa de Papai"
        }

        resp = self.client.put(
            path,
            data,
            HTTP_AUTHORIZATION=f"Token {self.user1_token}",
            content_type="application/json"
        )

        self.assertEqual(resp.status_code, 406)

    def test_delete_invalid_project(self):
        path = self.TEST_CLASS_PATH + "/999999"

        resp = self.client.delete(
            path,
            HTTP_AUTHORIZATION=f"Token {self.user1_token}"
        )

        self.assertEqual(resp.status_code, 404)

    def test_list_valid_project(self):
        path = self.TEST_CLASS_PATH + f"/{self.project.id}"

        resp = self.client.get(
            path,
            HTTP_AUTHORIZATION=f"Token {self.user1_token}"
        )

        resp_body = resp.json()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_body["content"]["id"], self.project.id)
        self.assertEqual(resp_body["content"]["name"], self.project.name)

    def test_update_valid_project(self):
        path = self.TEST_CLASS_PATH + f"/{self.project.id}"

        data = {
            "name": "Casa de Papai"
        }

        resp = self.client.put(
            path,
            data,
            HTTP_AUTHORIZATION=f"Token {self.user1_token}",
            content_type="application/json"
        )

        self.assertEqual(resp.status_code, 204)

    def test_update_valid_project_bad_formatting(self):
        path = self.TEST_CLASS_PATH + f"/{self.project.id}"

        data = {
            "name": ""
        }

        resp = self.client.put(
            path,
            data,
            HTTP_AUTHORIZATION=f"Token {self.user1_token}",
            content_type="application/json"
        )

        self.assertEqual(resp.status_code, 400)

    def test_delete_valid_project(self):
        path = self.TEST_CLASS_PATH + f"/{self.project.id}"

        resp = self.client.delete(
            path,
            HTTP_AUTHORIZATION=f"Token {self.user1_token}"
        )

        self.assertEqual(resp.status_code, 204)

    def test_list_valid_project_without_permission(self):
        path = self.TEST_CLASS_PATH + f"/{self.project.id}"

        resp = self.client.get(
            path,
            HTTP_AUTHORIZATION=f"Token {self.user2_token}"
        )

        self.assertEqual(resp.status_code, 403)

    def test_update_valid_project_without_permission(self):
        path = self.TEST_CLASS_PATH + f"/{self.project.id}"

        data = {
            "name": "Casa de Papai"
        }

        resp = self.client.put(
            path,
            data,
            HTTP_AUTHORIZATION=f"Token {self.user2_token}",
            content_type="application/json"
        )

        self.assertEqual(resp.status_code, 403)

    def test_delete_valid_project_without_permission(self):
        path = self.TEST_CLASS_PATH + f"/{self.project.id}"

        resp = self.client.delete(
            path,
            HTTP_AUTHORIZATION=f"Token {self.user2_token}"
        )

        self.assertEqual(resp.status_code, 403)


class UsersParticipationViewTest(TestCase):
    
    def setUp(self):
        self.TEST_CLASS_PATH = API_BASE_PATH + "/users"
        self.client = Client()

        self.user1 = User.objects.create(
            username="emilio@discod.com",
            email="emilio@discod.com",
            first_name="Emilio DiscoD",
            password=make_password('irreal', hasher='pbkdf2_sha256')
        )

        self.user2 = User.objects.create(
            username="emilio@nails.com",
            email="emilio@nails.com",
            first_name="Emilio Nails",
            password=make_password('reinstalar', hasher='pbkdf2_sha256')
        )

        self.user3 = User.objects.create(
            username="cortella@isso.com",
            email="cortella@isso.com",
            first_name="Cortella Isso",
            password=make_password('iiiiisso', hasher='pbkdf2_sha256')
        )

        self.project = Project.objects.create(
            name="Little Orange",
            data_type=DataType.objects.create(type_name="image")
        )

        ProjectHasUser.objects.create(
            user=self.user1,
            project=self.project,
            permission=2
        )

        ProjectHasUser.objects.create(
            user=self.user2,
            project=self.project,
            permission=0
        )

        self.user1_token = Token.objects.get_or_create(user=self.user1)[0].key
        self.user2_token = Token.objects.get_or_create(user=self.user2)[0].key
        self.user3_token = Token.objects.get_or_create(user=self.user3)[0].key

    def test_list_non_existing_participations(self):
        path = self.TEST_CLASS_PATH + f"/{self.user3.id}/projects"

        resp = self.client.get(
            path,
            HTTP_AUTHORIZATION=f"Token {self.user3_token}"
        )

        resp_body = resp.json()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_body["message"], "No projects found for this user")

    def test_list_existing_participations(self):
        path = self.TEST_CLASS_PATH + f"/{self.user2.id}/projects"

        resp = self.client.get(
            path,
            HTTP_AUTHORIZATION=f"Token {self.user2_token}"
        )

        resp_body = resp.json()

        self.assertEqual(resp.status_code, 200)
        self.assertGreater(len(resp_body["content"]), 0)

    def test_list_existing_participations_without_permission(self):
        path = self.TEST_CLASS_PATH + f"/{self.user2.id}/projects"

        resp = self.client.get(
            path,
            HTTP_AUTHORIZATION=f"Token {self.user3_token}"
        )

        self.assertEqual(resp.status_code, 403)

    def test_create_participation_not_allowed(self):
        path = self.TEST_CLASS_PATH + f"/{self.user3.id}/projects"

        data = {
            "user": {
                "username": self.user3.username,
                "permission": 2
            }
        }

        resp = self.client.post(
            path,
            data,
            HTTP_AUTHORIZATION=f"Token {self.user3_token}",
            content_type="application/json"
        )

        self.assertEqual(resp.status_code, 405)

    def test_update_participation_not_allowed(self):
        path = self.TEST_CLASS_PATH + f"/{self.user2.id}/projects"

        data = {
            "user": {
                "username": self.user2.username,
                "permission": 1
            }
        }

        resp = self.client.put(
            path,
            data,
            HTTP_AUTHORIZATION=f"Token {self.user3_token}",
            content_type="application/json"
        )

        self.assertEqual(resp.status_code, 405)


class ProjectsParticipationViewTest(TestCase):
    
    def setUp(self):
        self.TEST_CLASS_PATH = API_BASE_PATH + "/projects"
        self.client = Client()

        self.user1 = User.objects.create(
            username="emilio@discod.com",
            email="emilio@discod.com",
            first_name="Emilio DiscoD",
            password=make_password('irreal', hasher='pbkdf2_sha256')
        )

        self.user2 = User.objects.create(
            username="emilio@nails.com",
            email="emilio@nails.com",
            first_name="Emilio Nails",
            password=make_password('reinstalar', hasher='pbkdf2_sha256')
        )

        self.user3 = User.objects.create(
            username="cortella@isso.com",
            email="cortella@isso.com",
            first_name="Cortella Isso",
            password=make_password('iiiiisso', hasher='pbkdf2_sha256')
        )

        self.project = Project.objects.create(
            name="Little Orange",
            data_type=DataType.objects.create(type_name="image")
        )

        ProjectHasUser.objects.create(
            user=self.user1,
            project=self.project,
            permission=2
        )

        ProjectHasUser.objects.create(
            user=self.user2,
            project=self.project,
            permission=0
        )

        self.user1_token = Token.objects.get_or_create(user=self.user1)[0].key
        self.user2_token = Token.objects.get_or_create(user=self.user2)[0].key
        self.user3_token = Token.objects.get_or_create(user=self.user3)[0].key

    def test_list_all_users_in_project(self):
        path = self.TEST_CLASS_PATH + f"/{self.project.id}/users"

        resp = self.client.get(
            path,
            HTTP_AUTHORIZATION=f"Token {self.user1_token}"
        )

        resp_body = resp.json()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_body["message"], "2 users found")

    def test_list_all_users_in_project_without_permission(self):
        path = self.TEST_CLASS_PATH + f"/{self.project.id}/users"

        resp = self.client.get(
            path,
            HTTP_AUTHORIZATION=f"Token {self.user2_token}"
        )

        resp_body = resp.json()

        self.assertEqual(resp.status_code, 403)

    def test_create_valid_participation_with_non_owner_user(self):
        path = self.TEST_CLASS_PATH + f"/{self.project.id}/users"

        data = {
            "user": {
                "username": self.user3.username,
                "permission": 2
            }
        }

        resp = self.client.post(
            path,
            data,
            HTTP_AUTHORIZATION=f"Token {self.user3_token}",
            content_type="application/json"
        )

        resp_body = resp.json()

        self.assertEqual(resp.status_code, 406)

    def test_create_valid_participation_with_owner_user(self):
        path = self.TEST_CLASS_PATH + f"/{self.project.id}/users"

        data = {
            "user": {
                "username": self.user3.username,
                "permission": 1
            }
        }

        resp = self.client.post(
            path,
            data,
            HTTP_AUTHORIZATION=f"Token {self.user1_token}",
            content_type="application/json"
        )

        resp_body = resp.json()

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp_body["message"], "Participation created")

    def test_create_invalid_participation(self):
        path = self.TEST_CLASS_PATH + f"/{self.project.id}/users"

        data = {
            "user": {
                "username": "fake@user",
                "permission": 1
            }
        }

        resp = self.client.post(
            path,
            data,
            HTTP_AUTHORIZATION=f"Token {self.user1_token}",
            content_type="application/json"
        )

        resp_body = resp.json()

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp_body["message"], "User not found")

    def test_create_duplicated_participation(self):
        path = self.TEST_CLASS_PATH + f"/{self.project.id}/users"

        data = {
            "user": {
                "username": self.user1.username,
                "permission": 1
            }
        }

        resp = self.client.post(
            path,
            data,
            HTTP_AUTHORIZATION=f"Token {self.user1_token}",
            content_type="application/json"
        )

        resp_body = resp.json()

        self.assertEqual(resp.status_code, 406)
        self.assertEqual(resp_body["message"], "User is already in project")

    def test_update_valid_participation_with_non_permitted_user(self):
        path = self.TEST_CLASS_PATH + f"/{self.project.id}/users"

        data = {
            "user": {
                "username": self.user1.username,
                "permission": 1
            }
        }

        resp = self.client.put(
            path,
            data,
            HTTP_AUTHORIZATION=f"Token {self.user2_token}",
            content_type="application/json"
        )

        resp_body = resp.json()

        self.assertEqual(resp.status_code, 403)

    def test_update_valid_participation_with_permitted_user(self):
        path = self.TEST_CLASS_PATH + f"/{self.project.id}/users"

        data = {
            "user": {
                "username": self.user2.username,
                "permission": 1
            }
        }

        resp = self.client.put(
            path,
            data,
            HTTP_AUTHORIZATION=f"Token {self.user1_token}",
            content_type="application/json"
        )

        resp_body = resp.json()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_body["message"], "Participation updated")

    def test_update_invalid_participation(self):
        path = self.TEST_CLASS_PATH + f"/{self.project.id}/users"

        data = {
            "user": {
                "username": "fake@user",
                "permission": 1
            }
        }

        resp = self.client.put(
            path,
            data,
            HTTP_AUTHORIZATION=f"Token {self.user1_token}",
            content_type="application/json"
        )

        resp_body = resp.json()

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp_body["message"], "User not found")


class ParticipationDetailViewTest(TestCase):
    
    def setUp(self):
        self.TEST_CLASS_PATH_USERS = API_BASE_PATH + "/users"
        self.TEST_CLASS_PATH_PROJECTS = API_BASE_PATH + "/projects"
        self.client = Client()

        self.user1 = User.objects.create(
            username="emilio@discod.com",
            email="emilio@discod.com",
            first_name="Emilio DiscoD",
            password=make_password('irreal', hasher='pbkdf2_sha256')
        )

        self.user2 = User.objects.create(
            username="emilio@nails.com",
            email="emilio@nails.com",
            first_name="Emilio Nails",
            password=make_password('reinstalar', hasher='pbkdf2_sha256')
        )

        self.user3 = User.objects.create(
            username="cortella@isso.com",
            email="cortella@isso.com",
            first_name="Cortella Isso",
            password=make_password('iiiiisso', hasher='pbkdf2_sha256')
        )

        self.project = Project.objects.create(
            name="Little Orange",
            data_type=DataType.objects.create(type_name="image")
        )

        ProjectHasUser.objects.create(
            user=self.user1,
            project=self.project,
            permission=2
        )

        ProjectHasUser.objects.create(
            user=self.user2,
            project=self.project,
            permission=0
        )

        self.user1_token = Token.objects.get_or_create(user=self.user1)[0].key
        self.user2_token = Token.objects.get_or_create(user=self.user2)[0].key
        self.user3_token = Token.objects.get_or_create(user=self.user3)[0].key

    def test_list_participation_with_non_permitted_user(self):
        # /users/uid/projects/pid
        path_user = self.TEST_CLASS_PATH_USERS + f"/{self.user2.id}" \
            + f"/projects/{self.project.id}"

        # /projects/pid/users/uid
        path_proj = self.TEST_CLASS_PATH_PROJECTS + f"/{self.project.id}" \
            + f"/users/{self.user2.id}"

        resp = self.client.get(
            path_user,
            HTTP_AUTHORIZATION=f"Token {self.user2_token}",
        )

        self.assertEqual(resp.status_code, 403)

        resp = self.client.get(
            path_proj,
            HTTP_AUTHORIZATION=f"Token {self.user2_token}",
        )

        self.assertEqual(resp.status_code, 403)

    def test_list_participation_with_permitted_user(self):
        # /users/uid/projects/pid
        path_user = self.TEST_CLASS_PATH_USERS + f"/{self.user2.id}" \
            + f"/projects/{self.project.id}"

        # /projects/pid/users/uid
        path_proj = self.TEST_CLASS_PATH_PROJECTS + f"/{self.project.id}" \
            + f"/users/{self.user2.id}"

        resp = self.client.get(
            path_user,
            HTTP_AUTHORIZATION=f"Token {self.user1_token}",
        )

        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(
            path_proj,
            HTTP_AUTHORIZATION=f"Token {self.user1_token}",
        )

        self.assertEqual(resp.status_code, 200)

    def test_list_invalid_participation(self):
        # /users/uid/projects/pid
        path_user = self.TEST_CLASS_PATH_USERS + f"/{self.user3.id}" \
            + f"/projects/{self.project.id}"

        # /projects/pid/users/uid
        path_proj = self.TEST_CLASS_PATH_PROJECTS + f"/{self.project.id}" \
            + f"/users/{self.user3.id}"

        resp = self.client.get(
            path_user,
            HTTP_AUTHORIZATION=f"Token {self.user1_token}",
        )

        self.assertEqual(resp.status_code, 404)

        resp = self.client.get(
            path_proj,
            HTTP_AUTHORIZATION=f"Token {self.user1_token}",
        )

        self.assertEqual(resp.status_code, 404)

    def test_delete_participation_with_non_permitted_user(self):
        # /users/uid/projects/pid
        path_user = self.TEST_CLASS_PATH_USERS + f"/{self.user1.id}" \
            + f"/projects/{self.project.id}"

        # /projects/pid/users/uid
        path_proj = self.TEST_CLASS_PATH_PROJECTS + f"/{self.project.id}" \
            + f"/users/{self.user1.id}"

        resp = self.client.get(
            path_user,
            HTTP_AUTHORIZATION=f"Token {self.user2_token}",
        )

        self.assertEqual(resp.status_code, 403)

        resp = self.client.delete(
            path_proj,
            HTTP_AUTHORIZATION=f"Token {self.user2_token}",
        )

        self.assertEqual(resp.status_code, 403)

    def test_delete_participation_with_permitted_user(self):
        # /users/uid/projects/pid
        path_user = self.TEST_CLASS_PATH_USERS + f"/{self.user2.id}" \
            + f"/projects/{self.project.id}"

        # /projects/pid/users/uid
        path_proj = self.TEST_CLASS_PATH_PROJECTS + f"/{self.project.id}" \
            + f"/users/{self.user2.id}"

        resp = self.client.delete(
            path_user,
            HTTP_AUTHORIZATION=f"Token {self.user1_token}",
        )

        self.assertEqual(resp.status_code, 204)

        # After deleting, participation should be deleted from both ends
        resp = self.client.delete(
            path_proj,
            HTTP_AUTHORIZATION=f"Token {self.user1_token}",
        )

        self.assertEqual(resp.status_code, 404)

    def test_delete_participation_of_owner(self):
        # /users/uid/projects/pid
        path_user = self.TEST_CLASS_PATH_USERS + f"/{self.user1.id}" \
            + f"/projects/{self.project.id}"

        # /projects/pid/users/uid
        path_proj = self.TEST_CLASS_PATH_PROJECTS + f"/{self.project.id}" \
            + f"/users/{self.user1.id}"

        resp = self.client.delete(
            path_user,
            HTTP_AUTHORIZATION=f"Token {self.user1_token}",
        )

        self.assertEqual(resp.status_code, 409)

        resp = self.client.delete(
            path_proj,
            HTTP_AUTHORIZATION=f"Token {self.user1_token}",
        )

        self.assertEqual(resp.status_code, 409)


def check_update_accuracy_state_mock(project_id):
    return None


class AccuracyViewTest(TestCase):

    def setUp(self):
        dtype = DataType.objects.create(type_name='test')
        self.project = Project.objects.create(data_type=dtype,
                                              name='AccuracyViewTest')
        self.labels = [Label.objects.create(project=self.project,
                                            label=str(i)) for i in range(3)]
        self.user = User.objects.create(
            username='chocotone@limao.com.vc',
            email='chocotone@limao.com.vc',
            first_name='Chocotone De Limao',
            password=make_password('secreto.1234', hasher='pbkdf2_sha256')
        )
        self.token = Token.objects.get_or_create(user=self.user)[0].key    
        ProjectHasUser.objects.create(
            user=self.user,
            project=self.project,
            permission=2
        )
        self.client = Client()

    @mock.patch('api.views.check_update_accuracy_state', 
                side_effect=check_update_accuracy_state_mock)
    def test_access_forbidden(self, m):
        new_user = User.objects.create(
            username='makelele.prime@ea.com',
            email='makelele.prime@ea.com',
            first_name='Makelele Prime',
            password=make_password('secreto.1234', hasher='pbkdf2_sha256')
        )
        new_token = Token.objects.get_or_create(user=new_user)[0].key
        ProjectHasUser.objects.create(
            user=new_user,
            project=self.project,
            permission=0
        )
        response = self.client.get('/api/v1/projects/{pid}/accuracy'
                                   .format(pid=self.project.id),
                                   HTTP_AUTHORIZATION='Token {}'
                                   .format(new_token))
        self.assertEqual(response.status_code, 403)

    @mock.patch('api.views.check_update_accuracy_state', 
                side_effect=check_update_accuracy_state_mock)
    def test_user_not_in_project(self, m):
        new_user = User.objects.create(
            username='nedved.prime@ea.com',
            email='nedved.prime@ea.com',
            first_name='Nedved Prime',
            password=make_password('secreto.1234', hasher='pbkdf2_sha256')
        )
        new_token = Token.objects.get_or_create(user=new_user)[0].key

        response = self.client.get('/api/v1/projects/{pid}/accuracy'
                                   .format(pid=self.project.id),
                                   HTTP_AUTHORIZATION='Token {}'
                                   .format(new_token))
        self.assertEqual(response.status_code, 404)

    @mock.patch('api.views.check_update_accuracy_state',
                side_effect=check_update_accuracy_state_mock)
    def test_no_acc_data(self, m):
        response = self.client.get('/api/v1/projects/{pid}/accuracy'
                                   .format(pid=self.project.id),
                                   HTTP_AUTHORIZATION='Token {}'
                                   .format(self.token))
        self.assertEqual(response.status_code, 204)

    @mock.patch('api.views.check_update_accuracy_state',
                side_effect=check_update_accuracy_state_mock)
    def test_with_acc_data(self, m):

        self.accs = [Accuracy.objects.create(project=self.project,
                                             accuracy=0.679,
                                           ) for i in range(5)]
        self.freqs = []
        for acc in self.accs:
            for label in self.labels:
                self.freqs.append(SampleFrequency.objects.create(label=label,
                                                        accuracy=acc,
                                                        frequency=25))

        Data.objects.create(content='content', url='url', project=self.project)
        response = self.client.get('/api/v1/projects/{pid}/accuracy'
                                   .format(pid=self.project.id),
                                   HTTP_AUTHORIZATION='Token {}'
                                   .format(self.token))

        
        self.assertEqual(response.status_code, 200)
        response = response.json()

        for i, acc in enumerate(self.accs):
            accuracies_json = response['content'][i]
            self.assertEqual(accuracies_json['id'], acc.id)
            self.assertEqual(accuracies_json['accuracy'], acc.accuracy)
            self.assertEqual(accuracies_json['date'], str(acc.date))
            self.assertEqual(accuracies_json['total_samples'],
                             SampleFrequency.objects.filter(accuracy=acc) \
                                          .aggregate(total=Sum('frequency'))\
                                          ["total"])
            cur_freqs = SampleFrequency.objects.filter(accuracy=acc)
            for j, freq in enumerate(cur_freqs):
                frequencies_json = accuracies_json['frequencies'][j]
                self.assertEqual(frequencies_json["label"], freq.label.label)
                self.assertEqual(frequencies_json["frequency"], freq.frequency)


class AccuracyLibTest(TestCase):

    def setUp(self):
        pass

    def test_wa_project(self):
        wa_type = DataType.objects.get_or_create(type_name='wa')[0]
        project = Project.objects.create(name='WA Project', data_type=wa_type)
        self.assertEqual(check_update_accuracy_state(project.id), 
                         INVALID_PROJECT_TYPE)

    def test_insufficient_data(self):
        text_type = DataType.objects.get_or_create(type_name='image')[0]
        project = Project.objects.create(name='VR Project',
                                         data_type=text_type)
        datas = [Data.objects.create(content=f'{i}',
                                     url=f'{i}',
                                     project=project) for i in range(10)]
        label1 = Label.objects.create(label='wasabi', project=project)
        label2 = Label.objects.create(label='shoyu', project=project)
        [Seed.objects.create(data=data,
                             label=label1 if i % 2 == 0 else label2)
                                for i, data in enumerate(datas)]
        self.assertEqual(check_update_accuracy_state(project.id), TRIED_STARTED_CLF)
