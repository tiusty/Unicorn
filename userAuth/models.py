from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin
from houseDatabase.models import RentDatabaseModel


class MyUserManager(BaseUserManager):

    def _create_user(self, email, password, is_superuser, is_admin, **extra_fields):
        """
        Creates and saves a User with the given email and password
        :param email:
        :param password:
        :param is_staff:
        :param is_superuser:
        :param extra_fields:
        :return:
        """

        now = timezone.now()

        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, is_active=True,
                          is_superuser=is_superuser, is_admin=is_admin,
                          last_login=now,
                          joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, True, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


# noinspection PyAbstractClass
class MyUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user class
    """
    email_user = models.EmailField('email address', unique=True, db_index=True)
    joined_user = models.DateField(auto_now_add=True)
    is_active_user = models.BooleanField(default=True)
    is_admin_user = models.BooleanField(default=False)
    is_superuser_user = models.BooleanField(default=False)
    first_name_user = models.CharField(max_length=200)
    last_name_user = models.CharField(max_length=200)

    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email_user

    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name_user, self.last_name_user)

    @property
    def email(self):
        return self.email_user

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin_user


class UserProfile(models.Model):
    user = models.OneToOneField(MyUser, related_name="userProfile", on_delete=models.CASCADE, default='none')
    favorites = models.ManyToManyField(RentDatabaseModel, related_name="favorite_list", blank=True)
    visit_list = models.ManyToManyField(RentDatabaseModel, related_name="visit_list", blank=True)

    def __str__(self):
        return self.user.email


# noinspection PyUnusedLocal
def create_user_profile(sender, instance, created, **kwargs):
    if created:
            UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=MyUser)
