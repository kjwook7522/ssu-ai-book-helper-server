from django.db import models

class User(models.Model):
  student_id = models.IntegerField(primary_key=True)
  password = models.CharField(max_length=64, null=False)
  name = models.CharField(max_length=8, null=False)
  email = models.EmailField(max_length=20, null=False)
  phone = models.CharField(max_length=20, null=False)