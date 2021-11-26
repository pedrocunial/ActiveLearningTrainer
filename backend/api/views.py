import csv
import json

from django.http import JsonResponse, HttpResponse
from django.db.models import Max
from rest_framework.views import APIView

from api.models import (Data, Label, Seed, PredictProba,
                        Project, Pool, ProjectHasUser,
                        Accuracy, SampleFrequency)
from django.db.models import Sum
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from api.libs.classifier import update_seed
from api.libs.accuracy import ( 
    get_accuracy_history,
    get_samples_frequencies,
    check_update_accuracy_state
)
from api.utils.populate_db import populate_db
import api.libs.wao as wao
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated


class LoginView(APIView):
    def post(self, request):
        body = get_body(request)

        email = body.get("username")
        password = body.get("password")

        try:
            user = User.objects.get(
                email=email
            )
        except User.DoesNotExist:
            return JsonResponse(
                status=404,
                data=response_model("Incorrect credentials.", content=None)
            )

        if not user.check_password(password):
            return JsonResponse(
                status=404,
                data=response_model("Incorrect credentials.", content=None)
            )

        token = Token.objects.get_or_create(user=user)

        return JsonResponse(
            status=200,
            data={
                'token': token[0].key,
                'uid': user.id
            }
        )


class AccuracyView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        project_id = int(kwargs.get("pid"))

        try:
            projects_user = ProjectHasUser.objects \
                            .get(user__id=request.user.id, 
                                 project__id=project_id)
        except ProjectHasUser.DoesNotExist:
            
            return JsonResponse(
                status=404,
                data=response_model("You are not in this project", None)
            )
        else:
            if not (projects_user.permission == 1
                    or projects_user.permission == 2):
                return JsonResponse(
                    status=403,
                    data=response_model("Access forbidden", None)
                )
            else:
                msg = check_update_accuracy_state(project_id)
                accuracies = get_accuracy_history(project_id)

                if not accuracies.exists():
                    return JsonResponse(
                        status=204,
                        data=response_model(msg, None)
                    )

                content = []
                for acc in accuracies:
                    cur = {
                        "id" : acc.id,
                        "accuracy" : float(acc.accuracy),
                        "date" : str(acc.date),
                        "total_samples" : SampleFrequency.objects \
                            .filter(accuracy__id=acc.id) \
                            .aggregate(total=Sum('frequency'))["total"],
                        "frequencies" : []
                    }

                    samples_freq = get_samples_frequencies(acc.id)
                    for elem in samples_freq:
                        sub_cur = {
                            "label" : elem.label.label,
                            "frequency" : elem.frequency
                        }
                        cur["frequencies"].append(sub_cur)
                    content.append(cur)

                return JsonResponse(
                    status=200,
                    data=response_model(msg, content)
                )


class SampleFrequencyView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        accuracy_id = int(request.GET['id'])
        
        try:
            project_id = Accuracy.objects.get(id=accuracy_id).project.id
            projects_user = ProjectHasUser.objects \
                            .get(user__id=request.user.id, 
                                 project__id=project_id)
        except ProjectHasUser.DoesNotExist:
            return JsonResponse(
                status=404,
                data=response_model("You are not in this project", None)
            )
        else:
            if not (projects_user.permission == 1
                    or projects_user.permission == 2):
                return JsonResponse(
                    status=403,
                    data=response_model("Access forbidden", content)
                )
            else:
                samples_freq = get_samples_frequencies(accuracy_id)
                content = {
                    "frequencies" : []
                }
                for elem in samples_freq:
                    cur = {
                        "label" : elem.label.label,
                        "frequency" : elem.frequency
                    }
                    content["frequencies"].append(cur)
                return JsonResponse(
                    status=200,
                    data=response_model("OK", content)
                )


def response_model(message, content):
    return {
        "message": message,
        "content": content
    }


def get_body(request):
    return json.loads(request.body.decode("utf-8"))


class UserView(APIView):

    def get(self, request):
        users = User.objects.all()

        status = 200
        message = "Users found" if len(users) > 0 else "No users found"
        content = [
            {
                "id": user.id,
                "email": user.email
            }
            for user in users
        ]

        return JsonResponse(
            status=status,
            data=response_model(message, content)
        )

    def post(self, request):
        body = get_body(request)

        username = body.get("username")
        password = body.get("password")
        fullname = body.get("name")

        try:
            user = User.objects.get(email=username)
            status = 409
            message = "User already exists"
            content = None
        except User.DoesNotExist:
            created_user = User.objects.create(
                username=username,
                email=username,
                first_name=fullname,
                password=make_password(password, hasher="pbkdf2_sha256")
            )
            status = 201
            message = "User created"
            content = {
                "id": created_user.id
            }

        return JsonResponse(
            status=status,
            data=response_model(message, content)
        )


class UserDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        status = 0
        message = ""
        content = None

        try:
            user = User.objects.get(
                id=kwargs.get("uid")
            )

        except User.DoesNotExist:
            status = 404
            message = "User not found"
            content = None
        else:
            if kwargs.get("uid") == request.user.id:

                status = 200
                message = "User found"
                content = {
                    "id": user.id,
                    "email": user.email
                }
            else:
                status = 403
                message = "You cant access other users details"
                content = None

        return JsonResponse(
            status=status,
            data=response_model(message, content)
        )

    def put(self, request, **kwargs):
        status = 0
        message = ""
        content = None
        body = get_body(request)

        password = body.get("password")

        try:
            user = User.objects.get(id=kwargs.get("uid"))
        except User.DoesNotExist:
            status = 404
            message = "User not found"
            content = None
        else:
            if kwargs.get("uid") == request.user.id:

                status = 200
                if len(password) >= 1:
                    user.set_password(password)
                    status = 204
                    message = "Password changed"
                    content = None
                else:
                    status = 400
                    message = "Incorrect password length"
                    content = None

            else:
                status = 403
                message = "You cant modify other users passwords!"
                content = None

        return JsonResponse(
            status=status,
            data=response_model(message, content)
        )

    def delete(self, request, **kwargs):
        user = ""
        try:
            user = User.objects.get(id=kwargs.get("uid"))
        except User.DoesNotExist:
            status = 404
            message = "User not found"
            content = None
        else:
            if kwargs.get("uid") == request.user.id:
                user.delete()
                status = 204
                message = "User deleted"
                content = None
            else:
                status = 403
                message = "You cant delete other users!"
                content = None 
            
        return JsonResponse(
            status=status,
            data=response_model(message, content)
        )


class ProjectView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        '''
        Gets all projects from current user
        '''
        projects_user = ProjectHasUser.objects \
                        .filter(user__id=request.user.id)
        projects = [project.project for project in projects_user]

        status = 200
        message = "Projects found"
        content = [
            {
                'id': project.id,
                'name': project.name,
                'type': project.data_type.type_name,
                "data_count": Data.objects.filter(project=project.id).count(),
                "labelled_count": Seed.objects.filter(
                    data__project__id=project.id).count()
            }
            for project in projects
        ]

        return JsonResponse(
            status=status,
            data=response_model(message, content)
        )

    def post(self, request, format=None):
        """https://pfeibm.docs.apiary.io/#reference/0/projects/post"""

        body = get_body(request)

        name = body.get("name")
        data_type = body.get("type")
        uid = int(body.get("user_id"))
        workspace_id = body.get("classifier_credentials") \
                           .get("workspace_id", "")
        api_key = body.get("classifier_credentials").get("api_key", "")
        url = body.get("classifier_credentials").get("url", "")
        api_key_storage = body.get("storage_credentials") \
                              .get("api_key_storage", "")
        instance_id = body.get("storage_credentials").get("instance_id", "")
        bucket_name = body.get("storage_credentials").get("bucket_name", "")
        labels = body.get("labels", "")
        url_endpoint = body.get("storage_credentials").get("url_endpoint", 
            "https://s3.us-south.cloud-object-storage.appdomain.cloud")

        try:
            project_id = populate_db(
                project_name=name,
                data_type=data_type,
                labels=labels,
                uid=uid,
                workspace_id=workspace_id,
                api_key=api_key,
                url=url,
                api_key_storage=api_key_storage,
                instance_id=instance_id,
                bucket_name=bucket_name,
                url_endpoint=url_endpoint)
            status = 201
            message = "Project created"
            content = {
                "id": project_id
            }
        except ValueError as err:
            status = 400
            message = str(err)
            content = None

        return JsonResponse(
            status=status,
            data=response_model(message, content)
        )


class ProjectDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        status = 0
        message = ""
        content = None

        show_users = request.GET.get("users", "false")
        pid = kwargs.get("pid")

        try:
            projects_user = ProjectHasUser.objects \
                            .get(user__id=request.user.id, project__id=pid)
        except ProjectHasUser.DoesNotExist:
            status = 406
            message = "There is not such project"
            content = None
        else:
            if not (projects_user.permission == 1
                    or projects_user.permission == 2):
                status = 403
                message = "Access Forbidden"
                content = None

            else:
                try:
                    project = Project.objects.get(id=pid)
                    data_count = Data.objects.filter(project=pid).count()
                    seed_count = Seed.objects.filter(data__project__id=pid) \
                                             .count()
                    status = 200
                    message = "Project found"
                    content = {
                        "id": project.id,
                        "name": project.name,
                        "data_type": project.data_type.type_name,
                        "data_count": data_count,
                        "labelled_count": seed_count
                    }

                    if show_users.lower() == "true":
                        participations = ProjectHasUser.objects \
                                         .filter(project=pid)
                        content["users"] = []

                        for part in participations:
                            content["users"].append(
                                {
                                    "id": part.user.id,
                                    "permission": part.permission
                                }
                            )

                except Project.DoesNotExist:
                    status = 404
                    message = "Project not found"
                    content = None

        return JsonResponse(
            status=status,
            data=response_model(message, content)
        )

    def put(self, request, **kwargs):
        status = 0
        message = ""
        content = None

        body = get_body(request)
        name = body["name"]
        pid = kwargs.get("pid")

        try:
            projects_user = ProjectHasUser.objects \
                            .get(user__id=request.user.id, project__id=pid)
        except ProjectHasUser.DoesNotExist:
            status = 406
            message = "There is not such project"
            content = None
        else:
            if not (projects_user.permission == 1 
                    or projects_user.permission == 2):
                status = 403
                message = "Access Forbidden"
                content = None

            else:
                try:
                    project = Project.objects.get(
                        id=int(pid)
                    )

                    if len(name) >= 3:
                        project.name = name
                        status = 204
                        message = "Project name changed"
                        content = None

                    else:
                        status = 400
                        message = "Project name too short"
                        content = None

                except Project.DoesNotExist:
                    status = 404
                    message = "Project not found"
                    content = None

        return JsonResponse(
            status=status,
            data=response_model(message, content)
        )

    def delete(self, request, **kwargs):
        status = 0
        message = ""
        content = None

        pid = kwargs.get("pid")

        try:
            projects_user = ProjectHasUser.objects \
                            .get(user__id=request.user.id, project__id=pid) \
        
        except ProjectHasUser.DoesNotExist:
            status = 404
            message = "There is not such project"
            content = None
        else:
            if not (projects_user.permission == 1 
                    or projects_user.permission == 2):
                status = 403
                message = "Access Forbidden"
                content = None

            else:
                try:
                    project = Project.objects.get(
                        id=kwargs.get("pid")
                    )
                    project.delete()

                    status = 204
                    message = "Project deleted"
                    content = None

                except Project.DoesNotExist:
                    status = 404
                    message = "Project not found"
                    content = None

        return JsonResponse(
            status=status,
            data=response_model(message, content)
        )


class ParticipationView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        status = 0
        message = ""
        content = None

        uid = kwargs.get("uid")
        pid = kwargs.get("pid")
        show_details = request.GET.get("details", None)

        if uid:
            if uid == request.user.id:
                part = ProjectHasUser.objects.filter(
                    user=int(uid)
                )

                status = 200

                if len(part) > 0:
                    message = f"{len(part)} projects found"
                else:
                    message = "No projects found for this user"

                content = [
                    {
                        "id": p.project.id,
                        "name": p.project.name,
                        "type": p.project.data_type.type_name \
                            if show_details == "true" else "",
                        "data_count": Data.objects.filter(project=p.project.id) \
                                .count() if show_details == "true" else "",
                        "labelled_count": Seed.objects \
                                .filter(data__project__id=p.project.id).count() \
                            if show_details == "true" else "",
                        "permission": p.permission
                    }
                    for p in part
                ]
            else:
                status = 403
                message = "You cant access other user projects"
                content = None

        elif pid:
            try:
                projects_user = ProjectHasUser.objects \
                            .get(user__id=request.user.id, project__id=pid)
            except ProjectHasUser.DoesNotExist:
                status = 403
                message = "User not found"
                content = None
            else:
                if not (projects_user.permission == 1
                        or projects_user.permission == 2):
                    status = 403
                    message = "Access Forbidden"
                    content = None
                else:
                    part = ProjectHasUser.objects.filter(
                        project=int(pid)
                    )

                    status = 200
                    message = f"{len(part)} users found"
                    content = [
                        {
                            "id": p.user.id,
                            "name": p.user.first_name,
                            "permission": p.permission
                        }
                        for p in part
                    ]

        return JsonResponse(
            status=status,
            data=response_model(message, content)
        )

    def post(self, request, **kwargs):
        """
        {
            "email": "",
            "roles": {
                "owner": true,
                "admin": true
            }
        }
        """
        status = 0
        message = ""
        content = None

        uid = kwargs.get("uid")
        pid = kwargs.get("pid")

        body = get_body(request)

        if pid:
            try:
                projects_user = ProjectHasUser.objects \
                                .get(user__id=request.user.id, project__id=pid)
            except ProjectHasUser.DoesNotExist:
                status = 406
                message = "There is not such project or you cant view it"
                content = None
            else:
                if not (projects_user.permission == 1 
                        or projects_user.permission == 2):
                    status = 403
                    message = "Access Forbidden"
                    content = None
                else:

                    u = body.get("user")
                    project = Project.objects.get(id=pid)

                    try:
                        user = User.objects.get(email=u["username"])

                        try:
                            relation = ProjectHasUser.objects.get(
                                user=user,
                                project=project
                            )

                        except ProjectHasUser.DoesNotExist:
                            phu = ProjectHasUser.objects.create(
                                user=user,
                                project=project,
                                permission=u["permission"]
                            )

                            status = 201
                            message = "Participation created"
                            content = {
                                "id": phu.id
                            }

                        else:
                            status = 406
                            message = "User is already in project"
                            content = None

                    except User.DoesNotExist as exc:
                        status = 404
                        message = "User not found"
                        content = None

        elif uid:
            status = 405
            message = "Method not allowed"
            content = None

        return JsonResponse(
            status=status,
            data=response_model(message, content)
        )

    def put(self, request, **kwargs):
        """
        {
            "email": "",
            "roles": {
                "owner": true,
                "admin": true
            }
        }
        """
        status = 0
        message = ""
        content = None

        uid = kwargs.get("uid")
        pid = kwargs.get("pid")

        body = get_body(request)

        if pid:
            try:
                projects_user = ProjectHasUser.objects \
                                .get(user__id=request.user.id, project__id=pid)
            except ProjectHasUser.DoesNotExist:
                status = 406
                message = "There is not such project or you cant view it"
                content = None
            else:
                if not (projects_user.permission == 1 
                        or projects_user.permission == 2):
                    status = 403
                    message = "Access Forbidden"
                    content = None
                else:

                    u = body.get("user")
                    project = Project.objects.get(id=pid)

                    try:
                        user = User.objects.get(email=u["username"])

                        try:
                            relation = ProjectHasUser.objects.get(
                                user=user,
                                project=project
                            )

                            relation.permission = u["permission"]
                            relation.save()

                            status = 200
                            message = "Participation updated"
                            content = None

                        except ProjectHasUser.DoesNotExist:
                            status = 404
                            message = "User not found in project"
                            content = None


                    except User.DoesNotExist as exc:
                        status = 404
                        message = "User not found"
                        content = None

        elif uid:
            status = 405
            message = "Method not allowed"
            content = None

        return JsonResponse(
            status=status,
            data=response_model(message, content)
        )


class ParticipationDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        status = 200
        message = ""
        content = None

        uid = int(kwargs.get("uid"))
        pid = int(kwargs.get("pid"))

        try:
            participation = ProjectHasUser.objects.get(
                user=request.user.id,
                project=pid,
                permission__gte=1
            )
        except ProjectHasUser.DoesNotExist:
            status = 403
            message = "You are not an admin of this project"
            content = None
        else:
            try:
                participation = ProjectHasUser.objects.get(
                    user=uid,
                    project=pid
                )

                status = 200
                message = "Relation found"
                content = {
                    "project": pid,
                    "user": uid,
                    "permission": participation.permission
                }
            except ProjectHasUser.DoesNotExist:
                status = 404
                message = "Relation not found"
                content = None

        return JsonResponse(
            status=status,
            data=response_model(message, content)
        )

    def delete(self, request, **kwargs):
        uid = kwargs.get("uid")
        pid = kwargs.get("pid")

        try:
            participation = ProjectHasUser.objects.get(
                user=request.user.id,
                project=pid,
                permission__gte=1
            )
        except ProjectHasUser.DoesNotExist:
            status = 403
            message = "You are not an admin of this project"
            content = None
        else:
            try:
                part = ProjectHasUser.objects.get(
                    user=int(uid),
                    project=int(pid)
                )

                if  part.permission < 2:
                    part.delete()
                    status = 204
                    message = "Relation deleted"
                    content = None
                else:
                    status = 409
                    message = "Owner of project cannot be removed"
                    content = None
            except ProjectHasUser.DoesNotExist:
                status = 404
                message = "Participation not found"
                content = None

        return JsonResponse(
            status=status,
            data=response_model(message, content)
        )


class LabelView(APIView):
    def post(self, request):
        body = get_body(request)
        project_id = request.GET["project"]

        label = body.get("label")
        existing_label = Label.objects.get(label=label)

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            status = 404
            message = "Project not found"
            content = {}
        else:
            if not existing_label:
                new_label = Label.objects.create(
                    label=label,
                    project=project
                )
                
                status = 201
                message = "Label created"
                content = {
                    "id": new_label.id
                }
            else: 
                status = 409
                message = "Label already exists"
                content = {
                    "id": existing_label.id   
                }

        return JsonResponse(
            status=status,
            data=response_model(message, content)
        )


class ClassifyView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        """
        Send one unlabeled instance.
        Received Arguments:
            project: <id>
        Returned JSON:
            {
                "type": ..., // Type of instance (text/image)
                "labels": [
                    {"label": ..., "id": ...}, // lavel value and id
                    {"label": ..., "id": ...},
                    ...
                ],
                "content": ..., // Content to be classified
                "id": ... // Instance id
            }
        """
        project_id = int(request.GET['project'])
        response = {}

        projects_user = ProjectHasUser.objects \
                                      .filter(user__id=request.user.id,
                                              project__id=project_id)

        if not projects_user.exists():
            response = {"error": "you cant receive samples from this project"}

        else:
            lc_sample = PredictProba.objects \
                                    .filter(pool__data__project__id=project_id) \
                                    .filter(pool__is_using=False) \
                                    .values('pool') \
                                    .annotate(max_proba=Max('proba')) \
                                    .order_by('max_proba')[0]['pool']
            pool = Pool.objects.get(data__id=lc_sample)
            pool.is_using = True
            pool.save()
            project_type = Project.objects.get(id=project_id) \
                                          .data_type.type_name

            content = Data.objects.get(id=lc_sample).content
            if project_type == "image":
                content = Data.objects.get(id=lc_sample).url
            response = {
                "type": project_type,
                "labels": [
                    {'label': x.label, 'id': x.id}
                    for x in Label.objects.filter(project=project_id).all()
                ],
                "content": content,
                "id": lc_sample
            }
        return JsonResponse(response)

    def post(self, request, format=None):
        """
        Receive one labeled instance.
        Received Arguments:
            project: <id>
        Received JSON:
            {
                "id": ..., // sample id
                "label": {
                    "label": ..., //label value
                    "id": ...,   //label id
                },
            }
        """

        body = json.loads(request.body.decode("utf-8"))
        project_id = request.GET["project"]

        projects_user = ProjectHasUser.objects \
                                      .filter(user__id=request.user.id,
                                              project__id=project_id)

        type_name = Project.objects.get(id=project_id).data_type.type_name

        if not projects_user.exists():
            return JsonResponse({
                "status": "You cant send labeled images for this project",
                "status_code": 403
            })

        else:
            if type_name == "wa":
                wao.update(body, project_id)
            else:
                update_seed(body["id"],
                            body["label"]["id"],
                            project_id,
                            body["label"]["label"])

            return JsonResponse({
                "status": "OK",
                "status_code": 200
            })


class DeployView(APIView):

    def get(self, request, format=None):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="seed.csv"'

        project_id = request.GET["project"]

        project_seeds = Seed.objects.filter(data__project__id=project_id)

        seed = [
            {
                "content": s.data.content,
                "label": s.label
            }
            for s in project_seeds
        ]

        wr = csv.DictWriter(response, ["content", "label"])
        for i in seed:
            wr.writerow(i)

        return response
