from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.IndexView, name = 'index'),
    path('project/<str:pk>', views.DetailView, name = 'detailview'),
    path('create-project/', views.CreateProject, name = 'create-project'),
    path('update-project/<str:pk>', views.UpdateProject, name = 'update-project'),
    path('delete-project/<str:pk>', views.DeleteProject, name = 'delete-project'),

]