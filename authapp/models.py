from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

class User(AbstractUser):
    username = None  #  Remove username
    email = models.EmailField(unique=True)  # Make email the unique identifier
    dob = models.DateField(null=True, blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    USERNAME_FIELD = 'email'  # Use email instead of username
    REQUIRED_FIELDS = ['name', 'dob']  # Other required fields

    def __str__(self):
        return self.email  # Return email instead of username
    
    class Meta:
        db_table = 'auth_user'
    
    
