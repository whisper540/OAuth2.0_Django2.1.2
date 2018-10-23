from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    cellphone = models.CharField(max_length=11, blank=True, null=True, verbose_name='手机号码')

    class Meta(AbstractUser.Meta):
        pass

    def __str__(self):
        return self.username

#授权主机列表
class Host(models.Model):
    client_id = models.CharField(max_length=40, null=False, verbose_name='主机ID')
    host_ip = models.GenericIPAddressField(null=False, default='0.0.0.0',verbose_name='IP地址')
    active_time = models.IntegerField(
        null=False, default='x', verbose_name="激活时间")
    user = models.ForeignKey(User, verbose_name="授权人",on_delete=models.CASCADE)

    class Meta:
        pass

    def __str__(self):
        pass

#授权码
class Authcode_log(models.Model):
    host = models.OneToOneField(Host, primary_key=True, on_delete=models.CASCADE)
    response_type = models.CharField(max_length=40, null=False, verbose_name='')
    # client_id = models.CharField(max_length=40, null=False, verbose_name='')
    redirect_uri = models.URLField(null=False, verbose_name='')
    scope = models.CharField(max_length=40, null=False, verbose_name='')
    state = models.CharField(max_length=40, default='x',null=False, verbose_name='')
    auth_code = models.CharField(null=False, default='x', max_length=40, verbose_name="授权码")
    exptime = models.IntegerField(null=False, default='x', verbose_name="过期时间")
    class Meta:
        pass

    def __str__(self):
        pass

#访问令牌
class Accesstoken(models.Model):
    host = models.OneToOneField(Host, primary_key=True, on_delete=models.CASCADE)
    is_alive = models.IntegerField(null=False, default=1, verbose_name="是否生存")
    access_token = models.CharField(null=False,default='x',max_length=40,verbose_name="授权码")
    exptime = models.IntegerField(null=False, default='x', verbose_name="过期时间")

    class Meta:
        pass

    def __str__(self):
        pass

#刷新令牌
class Refreshtoken(models.Model):
    host = models.OneToOneField(Host, primary_key=True, on_delete=models.CASCADE)
    is_alive = models.IntegerField(null=False, default=1, verbose_name="是否生存")
    refresh_token = models.CharField(null=False, default='x', max_length=40, verbose_name="刷新码")
    exptime = models.IntegerField(null=False, default='x', verbose_name="过期时间")

    class Meta:
        pass

    def __str__(self):
        pass

#组权限
class Group_Permission(models.Model):
    name = models.CharField(null=False, default='x',max_length=40, verbose_name="权限操作名")
    codename = models.CharField(null=False, default='x',max_length=40, verbose_name="操作名")
    

    class Meta:
        pass

    def __str__(self):
        pass

#主机所属组
class Host_Group(models.Model):
    name = models.CharField(max_length=40, null=False, verbose_name='组名')

    class Meta:
        pass

    def __str__(self):
        pass

#主机组权限
class Host_Group_Permissions(models.Model):
    host_group = models.OneToOneField(Host_Group, primary_key=True, on_delete=models.CASCADE)
    group_permissions = models.ManyToManyField(Group_Permission)

    class Meta:
        pass

    def __str__(self):
        pass
