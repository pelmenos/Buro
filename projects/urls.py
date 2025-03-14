from django.urls import path, include
from rest_framework.routers import DefaultRouter

from projects import views

router = DefaultRouter(use_regex_path=False)
router.register('projects', views.ProjectViewSet, basename='project')
router.register('stages/<int:stage_id>/tasks', views.TaskViewSet, basename='task')
router.register('stages/<int:stage_id>/tasks/<int:task_id>/files', views.TaskFileViewSet, basename='taskfile')
router.register('stages/<int:stage_id>/tasks/<int:task_id>/comments', views.CommentViewSet, basename='comment')
router.register('stages/<int:stage_id>/tasks/<int:task_id>/users', views.TaskUserViewSet, basename='taskuser')

urlpatterns = [
    path('', include(router.urls)),
    path('projects/<int:project_id>/stages/', views.StageList.as_view()),
    path('projects/<int:pk>/report/', views.RetrieveProjectReport.as_view()),
    path('stages/<int:pk>/', views.StageDetail.as_view())
]