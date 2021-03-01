from django.db import models

# Create your models here.


class AnnoTool(models.Model):
#    id = models.
    resume = models.FileField(blank=True, null=True, upload_to='uploaded')
    name = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    college = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    date_of_birth = models.DateField(auto_now_add=False)
    summary = models.CharField(max_length=1000)

    def __str__(self):
        return self.name
