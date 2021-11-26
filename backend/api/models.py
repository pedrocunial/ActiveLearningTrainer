from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):
    url = models.TextField()
    label = models.CharField(max_length=100)


class DataType(models.Model):
    type_name = models.CharField(max_length=1024, unique=True)

    def __str__(self):
        return 'DataType: "%s"' % (self.type_name)


class Project(models.Model):
    name = models.CharField(max_length=1024, unique=True)
    data_type = models.ForeignKey(DataType, on_delete=models.CASCADE)
    is_updating_acc = models.BooleanField(default=False)

    def __str__(self):
        return 'Project "%s" of data type "%s"' % \
            (self.name, self.data_type.type_name)


class Accuracy(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    accuracy = models.DecimalField(max_digits=32, decimal_places=31,
                                   default=None, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return 'Accuracy of project "%s" at the time "%s" is "%s"' % \
            (self.project.name, self.date, self.accuracy)


class CredentialNLC(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=44)
    url = models.CharField(max_length=256)

    def __str__(self):
        return 'CredentialNLC(project={project}'.format(
            project=self.project.name)


class CredentialWA(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=44)
    url = models.CharField(max_length=256)

    def __str__(self):
        return 'CredentialWA(project={project}'.format(
            project=self.project.name)


class CredentialVR(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=44)

    def __str__(self):
        return 'CredentialVR(project={project}, api_key={api_key})'.format(
            project=self.project.name,
            api_key=self.api_key
        )


class CredentialObjectStorage(models.Model):
    project = models.OneToOneField(Project,
                                   on_delete=models.CASCADE,
                                   primary_key=True)
    api_key = models.CharField(max_length=255)
    instance_id = models.CharField(max_length=255)
    bucket_name = models.CharField(max_length=255)
    url = models.CharField(default="", max_length=255)


    def __str__(self):
        return 'CredentialVR(project={project}, api_key={api_key}, \
                instance_id={instance_id}, bucket_name={bucket_name}, \
                url={url})'.format(
                    project=self.project.name,
                    api_key=self.api_key,
                    instance_id=self.instance_id,
                    bucket_name=self.bucket_name,
                    url=self.url
                )



class Data(models.Model):
    content = models.CharField(max_length=1024)
    url = models.TextField(default="")
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return 'content: %s -- url %s -- type: %s -- project: %s' % \
            (self.content, self.url,
             self.project.data_type.type_name,
             self.project.name)


class Label(models.Model):
    label = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.label)

    class Meta:
        unique_together = (('label', 'project'),)


class SampleFrequency(models.Model):
    accuracy = models.ForeignKey(Accuracy, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    frequency = models.IntegerField(default=0)

    def __str__(self):
        return 'There are "%s" samples of label "%s" in the project "%s"' % \
            (self.frequency, self.label.label, self.accuracy.project.name)


class Pool(models.Model):
    data = models.OneToOneField(Data, on_delete=models.CASCADE,
                                primary_key=True)
    is_using = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % (self.data.content)


class PredictProba(models.Model):
    proba = models.DecimalField(max_digits=32, decimal_places=31)  # 1.0 = 100%
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE)

    def __str__(self):
        return '%s from data "%s": %.2f' % (self.label,
                                            self.pool,
                                            self.proba)

    class Meta:
        unique_together = (('label', 'pool'),)


class Seed(models.Model):
    data = models.OneToOneField(Data, on_delete=models.CASCADE,
                                primary_key=True)
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    is_train = models.NullBooleanField(default=None)

    def __str__(self):
        return '%s: %s: %s -- %s' % (self.data, self.label, self.date,
                                     self.is_train)


class Classifier(models.Model):
    ibm_classifier_id = models.CharField(max_length=255, primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    log_date = models.CharField(max_length=255, blank=True)
    is_accuracy = models.BooleanField(default=False)

    class Meta:
        '''
        a project can only have one "regular" classifier and a
        "accuracy calculator" one
        '''
        unique_together = (('is_accuracy', 'project'),)

    def __str__(self):
        return '%s %s %s %s' % (self.ibm_classifier_id,
                                self.project,
                                self.log_date,
                                self.is_accuracy)


class ProjectHasUser(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.IntegerField(default=0, choices=((0, "labeller"),
                                                         (1, "admin"),
                                                         (2, "owner")
                                                         ))

    class Meta:
        unique_together = (('project', 'user'),)

    def __str__(self):
        return 'User %s is permission %s at Project %s' % \
            (self.user.id,
             self.permission,
             self.project.id)
