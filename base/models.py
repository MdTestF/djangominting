from distutils.command.upload import upload
from email import message
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import fields



class BigAutoField(fields.AutoField):
    def db_type(self, connection):
        if 'mysql' in connection._class.module_:
            return 'bigint AUTO_INCREMENT'
        return super(BigAutoField, self).db_type(connection)


# Create your models here.
class User(AbstractUser):
    is_boUser = models.BooleanField(default=False)
    is_norUser = models.BooleanField(default=False)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(max_length=300)

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:        
       db_table = 'User'


def upload_path(instance, filename):
    dateTime=str(instance.created).split(' ')
    date=dateTime[0]
    time=dateTime[1].split('.')
    fname = filename.split('.')
    filename=str(instance.user.id)+'_'+fname[0]+'_'+date+'_'+time[0]+'.'+fname[1]
    return ''.join(['',filename])



class Image(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(blank=True,null=True,upload_to=upload_path)
    url = models.URLField(max_length = 600,default='val')
    status = models.CharField(max_length=200, null=True,default='Uploaded')
    is_accept =  models.CharField(max_length=200, null=True,default='Pending')
    is_qcPassed = models.CharField(max_length=200, null=True,default='Not Passed')
    collectionName = models.CharField(max_length=200, null=True)
    collectionSym = models.CharField(max_length=200, null=True)
    is_readyForNft = models.CharField(max_length=200, null=True,default='Not yet')
    comment = models.TextField(default='No Comment')
    userWalletAddress = models.CharField(max_length=200, null=True)
    contractAddress = models.CharField(max_length=200, null=True)
    imageCID = models.CharField(max_length=200, null=True)
    jsonCID = models.CharField(max_length=200, null=True)
    pinataUpload = models.CharField(max_length=200, null=True,default='Not Yet')
    openSeaUpload = models.CharField(max_length=200, null=True,default='Not Yet')
    updated = models.DateTimeField(auto_now=True)
    minted = models.CharField(max_length=200, null=True,default='Not yet')
    soled = models.CharField(max_length=200, null=True,default='Not yet')
    sellOrder = models.CharField(max_length=200, null=True,default='Not yet')
    price = models.CharField(max_length=200, null=True,default=0)
    islocal=models.BooleanField()
    imageselltype=models.PositiveSmallIntegerField(blank=True, null=True)
    isgeneratevariation=models.BooleanField()

    product_title = models.CharField(max_length=200, null=False,default='title')
    price = models.PositiveBigIntegerField( null=True,default='0')
    sale_price = models.PositiveBigIntegerField(null=True,default='0')
    short_description = models.CharField(max_length=500, null=True)
    description = models.CharField(max_length=1200, null=True)


    class Meta:
        ordering = ['-updated', '-created']

class PinataUpload(models.Model):
    upImage = models.CharField(max_length=200, null=True)
    

class Role(models.Model):    
    role_name=models.CharField(max_length=150, null=False, unique=True)
    class Meta:        
        db_table = 'Role'

class RoleUser(models.Model):    
    role = models.ForeignKey(Role,on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=False)

    class Meta:
        unique_together = (('role', 'user'),)
        db_table = 'RoleUser'

class Action(models.Model):    
    form_name=models.CharField(max_length=200, null=False)
    action_control_name=models.CharField(max_length=200, null=True)
    action_name=models.CharField(max_length=200, null=False, unique=True)    
    action_description=models.CharField(max_length=700, null=True)
    
    class Meta:        
        db_table = 'Action'

class RoleAction(models.Model):    
    role = models.ForeignKey(Role,on_delete=models.CASCADE, null=False)
    action = models.ForeignKey(Action,on_delete=models.CASCADE, null=False)
    class Meta:
        unique_together = (('role', 'action'),)
        db_table = 'RoleAction'
