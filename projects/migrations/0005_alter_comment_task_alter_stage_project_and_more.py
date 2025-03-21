# Generated by Django 5.1.7 on 2025-03-13 23:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_comment_taskfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='projects.task'),
        ),
        migrations.AlterField(
            model_name='stage',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stages', to='projects.project'),
        ),
        migrations.AlterField(
            model_name='task',
            name='stage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='projects.stage'),
        ),
        migrations.AlterField(
            model_name='taskfile',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='projects.task'),
        ),
    ]
