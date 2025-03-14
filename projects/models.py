from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)
    client = models.ForeignKey('clients.Client', on_delete=models.SET_NULL, null=True, blank=True)
    participants = models.ManyToManyField('users.User', related_name='projects', blank=True)

    def __str__(self):
        return self.name


class Stage(models.Model):
    project = models.ForeignKey(Project, related_name='stages', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    class STATUS(models.TextChoices):
        WAITING = 'waiting', "Waiting"
        PROCESSING = 'processing', "Processing"
        DONE = 'done', "Done"
    stage = models.ForeignKey(Stage, related_name='tasks', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    deadline = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS, default=STATUS.WAITING)
    participants = models.ManyToManyField('users.User', related_name='tasks', through='TaskUser', blank=True)

    def __str__(self):
        return self.name


class TaskUser(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    spent_time = models.DurationField()


class Comment(models.Model):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class TaskFile(models.Model):
    task = models.ForeignKey(Task, related_name='files', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/%d/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name