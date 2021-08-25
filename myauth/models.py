import jwt
from datetime import datetime
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager, PermissionsMixin)




# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
         """ 
          Create  a user and saves them to the Db

         """
         if not username:
             raise ValueError("Username is required")
        
         if not email:
            raise ValueError("User must have an email")

         user = self.model(
             email=self.normalize_email(email)
         )
         user.set_password(password)
         user.save(using=self._db)
         return user
    
    def create_staffuser(self, email, username, password=None):
        """ Creates a user that can log into the admin site """

        user = self.create_user(
            email=email,
            username=username,
            password=password
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """ Creates user with all privileges """
        user = self.create_user(
            email=email,
            username=username,
            password=password
        )
        user.admin = True
        user.staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Inherited manager from  base UserModel """
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', )

    def __str__(self):
        return f'{self.email} joined at {self.created_at}'

    @property
    def is_staff(self):
        return self.staff and self.is_admin
    
    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def generate_jwt_token(self):
        """This generates a JSON Web Token that stores"""
        token_string = str(self.email) + " " + str(self.username)
        token = jwt.encode(
            {
                'user_data': token_string,
                'exp': datetime.now() + timedelta(hours=5)
            }, settings.SECRET_KEY, algorithm='HS256'
        )
        return token

    def token(self):
        """This method allows us to get users' token by calling 'user.token'"""
        return self.generate_jwt_token()


class UserProfile(models.Model):
    """"
    Stores more information about a user."""
    GENDER_CHOICES = (
        (1, 'Male'),
        (2, 'Female')
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True,
        related_name='user_profile')
    first_name = models.CharField(max_length=240, blank=True, null=True)
    last_name = models.CharField(max_length=240, blank=True, null=True)
    gender = models.CharField(
        max_length=230, choices=GENDER_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'{self.user.email}'

@receiver(post_save, sender=User)
def generate_profile_on_signup(sender, instance, **kwargs):
    """Auto generate a profile for a new user """
    UserProfile.objects.get_or_create(user=instance)
