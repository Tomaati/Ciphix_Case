# Generated by Django 4.2.1 on 2023-05-28 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Topic_Summary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_keywords', models.CharField(max_length=100, unique=True)),
                ('topic_summary', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Topic_Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conversation', models.CharField(max_length=1000)),
                ('topic_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard_app.topic_summary')),
            ],
        ),
    ]
