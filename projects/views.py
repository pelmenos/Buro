from rest_framework import viewsets, mixins
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404, \
    RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from projects.models import Project, Stage, Task, TaskFile, Comment, TaskUser
from projects.serializers import ProjectSerializer, StageSerializer, TaskSerializer, TaskFileSerializer, \
    CommentSerializer, TaskUserSerializer, ProjectReportSerializer
from users.permissions import IsAdminOrManagerOrReadOnly


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManagerOrReadOnly]


class StageList(ListCreateAPIView):
    serializer_class = StageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Stage.objects.none()
        return Stage.objects.filter(project_id=self.kwargs['project_id'])

    def perform_create(self, serializer):
        serializer.save(project=get_object_or_404(Project, pk=self.kwargs['project_id']))


class StageDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = StageSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManagerOrReadOnly]
    queryset = Stage.objects.all()


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Task.objects.none()
        return Task.objects.filter(stage_id=self.kwargs['stage_id'])

    def perform_create(self, serializer):
        serializer.save(stage=get_object_or_404(Stage, pk=self.kwargs['stage_id']))


class TaskFileViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    serializer_class = TaskFileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return TaskFile.objects.none()

        return TaskFile.objects.filter(task_id=self.kwargs['task_id'])

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, task=get_object_or_404(Task, pk=self.kwargs['task_id']))


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     GenericViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Comment.objects.none()

        return Comment.objects.filter(task_id=self.kwargs['task_id'])

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, task=get_object_or_404(Task, pk=self.kwargs['task_id']))


class TaskUserViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      mixins.UpdateModelMixin,
                      GenericViewSet):
    serializer_class = TaskUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return TaskUser.objects.none()
        return TaskUser.objects.filter(task_id=self.kwargs['task_id'])

    def perform_create(self, serializer):
        serializer.save(task=get_object_or_404(Task, pk=self.kwargs['task_id']))


class RetrieveProjectReport(RetrieveAPIView):
    serializer_class = ProjectReportSerializer
    queryset = Project.objects.all()


