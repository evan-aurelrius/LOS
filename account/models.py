from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

class CustomUserManager(UserManager):
    def create_user(self,email,password,**extra_fields):
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email,password,**extra_fields)

class User(AbstractUser):
    username = None
    email = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    branch = models.CharField(max_length=100, default='Pusat')

    # role
    is_admin = models.BooleanField(default=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user.is_admin=True

    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    
    if instance.is_superuser: return

    if created and instance.is_admin:
        Admin.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_superuser: return
    
    if instance.is_admin:
        instance.admin.save()