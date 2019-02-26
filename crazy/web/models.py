
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin
)
class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,

    )
    name = models.CharField(max_length=64, verbose_name="姓名")
    host_to_remoteuser = models.ManyToManyField('HostToRemoteUser')
    host_group=models.ManyToManyField('HostGroup')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email
class Host(models.Model):
    name = models.CharField(max_length=32,unique=True)
    id_addr=models.GenericIPAddressField(unique=True)
    port=models.SmallIntegerField(default=22)
    idc=models.ForeignKey('IDC',on_delete=models.CASCADE)
    def __str__(self):
        return self.name
class RemoteUser(models.Model):
    auth_type_choices=((0,'ssh-password'),(1,'ssh-key'))
    auth_type=models.SmallIntegerField(choices=auth_type_choices)
    username = models.CharField(max_length=32)
    password=models.CharField(max_length=62,blank=True,null=True)
    def __str__(self):
        return self.username
    class Meta:
        unique_together=('auth_type','username','password')
class HostToRemoteUser(models.Model):
    host=models.ForeignKey('Host',on_delete=models.CASCADE)
    removeuser=models.ForeignKey('RemoteUser',on_delete=models.CASCADE)
    class Meta:
        unique_together=('host','removeuser')
    def __str__(self):
        return "%s%s"%(self.host,self.removeuser)
class HostGroup(models.Model):
    name = models.CharField(max_length=32)
    host_to_remoteuser = models.ManyToManyField('HostToRemoteUser')
    def __str__(self):
        return self.name
class IDC(models.Model):
    name=models.CharField(max_length=32)
    def __str__(self):
        return self.name
class AuditLog(models.Model):
    user=models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    host_to_remoteuser = models.ForeignKey('HostToRemoteUser',on_delete=models.CASCADE)
    log_type_choices=((0,'login'),(1,'cmd'),(3,'logout'))
    log_type=models.SmallIntegerField(choices=log_type_choices)
    date=models.DateTimeField(auto_now_add=True)
    content=models.CharField(max_length=255)
    def __str__(self):
        return "%s %s"%(self.host_to_remoteuser,self.content)
class Task(models.Model):
    task_type_choices=((0,'批量命令'),(1,'文件传输'))
    task_type=models.SmallIntegerField(choices=task_type_choices)
    content=models.CharField(max_length=255,verbose_name='任务内容')
    user=models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    def __str__(self):
        return "%s%s"%(self.task_type,self.content)
    date=models.DateTimeField(auto_now_add=True)
class TaskLogDetail(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    result=models.TextField(verbose_name='任务执行结果')
    task=models.ForeignKey('Task',on_delete=models.CASCADE)
    task_status_choices=((0,'initialized'),(2,'success'),(3,'failed'))
    task_status=models.SmallIntegerField(choices=task_status_choices,default=0)
    host_to_remoteuser = models.ForeignKey('HostToRemoteUser',on_delete=models.CASCADE)
    def __str__(self):
        return "%s%s"%(self.task,self.task_status)