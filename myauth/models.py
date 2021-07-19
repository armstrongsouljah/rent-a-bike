from django.db import models
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
        return self.is_active

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
