# Generated by Django 3.1.7 on 2021-02-23 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnnoTool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resume', models.FileField(blank=True, null=True, upload_to='uploaded/%Y/%M/%D')),
                ('name', models.CharField(max_length=100)),
                ('degree', models.CharField(max_length=100)),
                ('college', models.CharField(max_length=100)),
                ('organization', models.CharField(max_length=100)),
                ('designation', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('summary', models.CharField(max_length=1000)),
            ],
        ),
    ]
