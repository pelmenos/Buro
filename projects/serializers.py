import datetime
from datetime import timedelta

from django.db.models import Sum
from django.utils.duration import duration_string
from rest_framework import serializers

from projects.models import Project, Stage, Task, TaskFile, Comment, TaskUser
from users.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()

    def get_progress(self, obj):
        done_tasks = 0
        all_tasks = 0
        for stage in obj.stages.all():
            done_tasks += stage.tasks.filter(status=Task.STATUS.DONE).count()
            all_tasks += stage.tasks.all().count()
        if done_tasks == 0:
            return 0
        return float(done_tasks / all_tasks * 100)

    class Meta:
        model = Project
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['participants'] = UserSerializer(instance.participants.all(), many=True).data
        return representation


class StageSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()

    def get_progress(self, obj):
        done_tasks = 0
        all_tasks = 0
        done_tasks += obj.tasks.filter(status=Task.STATUS.DONE).count()
        all_tasks += obj.tasks.all().count()
        if done_tasks == 0:
            return 0
        return int(done_tasks / all_tasks * 100)

    class Meta:
        model = Stage
        fields = '__all__'
        read_only_fields = ('project',)


class TaskUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskUser
        fields = '__all__'
        read_only_fields = ('task',)


class TaskSerializer(serializers.ModelSerializer):
    participants = TaskUserSerializer(many=True, read_only=True, source='taskuser_set')

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('stage',)


class TaskFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskFile
        fields = '__all__'
        read_only_fields = ('task', 'user')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('task', 'user')


class ProjectReportSerializer(serializers.ModelSerializer):
    total_tasks = serializers.SerializerMethodField()
    total_done_tasks = serializers.SerializerMethodField()
    total_waiting_tasks = serializers.SerializerMethodField()
    total_spent_time = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    def get_total_tasks(self, obj):
        total = 0
        for stage in obj.stages.all():
            total += stage.tasks.count()
        return total

    def get_total_done_tasks(self, obj):
        done_tasks = 0
        for stage in obj.stages.all():
            done_tasks += stage.tasks.filter(status=Task.STATUS.DONE).count()
        return done_tasks

    def get_total_waiting_tasks(self, obj):
        waiting_tasks = 0
        for stage in obj.stages.all():
            waiting_tasks += stage.tasks.exclude(status=Task.STATUS.DONE).count()
        return waiting_tasks

    def get_total_spent_time(self, obj):
        spent_time = timedelta()
        for stage in obj.stages.all():
            for task in stage.tasks.all():
                spent_time += task.taskuser_set.all().aggregate(spent_time=Sum('spent_time'))['spent_time'] or timedelta()
        return duration_string(spent_time)

    def get_progress(self, obj):
        total_done = self.get_total_done_tasks(obj)
        if total_done == 0:
            return 0
        total = self.get_total_tasks(obj)
        return total_done / total * 100

    class Meta:
        model = Project
        fields = ['name', 'total_tasks', 'total_done_tasks', 'total_waiting_tasks', 'total_spent_time', 'progress']
