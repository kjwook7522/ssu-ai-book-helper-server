from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
  use_in_migrations = True

  def create_superuser(self, student_id, name, email, password, phone):
    user = self.create_user(
      student_id=student_id,
      name=name,
      email=email,
      password=password,
      phone=phone
    )

    user.is_superuser = True
    user.save(using=self._db)
    return user

  def create_user(self, student_id, name, email, password, phone):
    user = self.model(
      student_id=student_id,
      name=name,
      email=self.normalize_email(email),
      phone=phone
    )

    user.set_password(password)
    user.save(using=self._db)
    return user

class User(AbstractBaseUser, PermissionsMixin):
  student_id = models.IntegerField(unique=True)
  name = models.CharField(max_length=10)
  email = models.EmailField(max_length=30)
  is_superuser = models.BooleanField(default=False)
  phone = models.CharField(max_length=30)
  token = models.CharField(max_length=256, null=True)
  date_joined = models.DateTimeField(default=timezone.now)

  objects = UserManager()
  
  USERNAME_FIELD = 'student_id'
  EMAIL_FIELD = 'email'
  REQUIRED_FIELDS = ['name', 'phone', 'email']

  def __str__(self):
      return self.email

  def get_full_name(self):
    return self.name

  def get_short_name(self):
    return self.name
  
  def is_staff(self):
    return self.is_superuser
  

class Book(models.Model):
  id = models.AutoField(primary_key=True)
  year = models.IntegerField()
  rank = models.IntegerField()
  title = models.CharField(max_length=200)
  author = models.CharField(max_length=50)
  review = models.IntegerField()
  description = models.TextField(max_length=1000, null=True)
  price = models.CharField(max_length=10)
  tags = models.CharField(max_length=200)
  ratings = models.FloatField()
  genre = models.CharField(max_length=200)
  barcode = models.IntegerField()
  publisher = models.CharField(max_length=50)
  date = models.CharField(max_length=200)
