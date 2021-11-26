from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


# router = DefaultRouter()
# router.register('', )

urlpatterns = [
    path('users', views.UserView.as_view()),
    path('users/<int:uid>', views.UserDetailView.as_view()),
    path('users/<int:uid>/projects', views.ParticipationView.as_view()),
    path('users/<int:uid>/projects/<int:pid>',
         views.ParticipationDetailView.as_view()),
    path('projects', views.ProjectView.as_view()),
    path('projects/<int:pid>', views.ProjectDetailView.as_view()),
    path('projects/<int:pid>/users', views.ParticipationView.as_view()),
    path('projects/<int:pid>/users/<int:uid>',
         views.ParticipationDetailView.as_view()),
    path('classify', views.ClassifyView.as_view()),
    path('deploy', views.DeployView.as_view()),
    path('login', views.LoginView.as_view()),
    path('projects/<int:pid>/accuracy', views.AccuracyView.as_view()),
    path('frequency', views.SampleFrequencyView.as_view()),
    path('deploy', views.DeployView.as_view()),
    path('labels', views.LabelView.as_view())
]
