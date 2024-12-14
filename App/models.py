from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Register(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    mobile = models.CharField(max_length=20, unique=True)  
    age = models.PositiveIntegerField()
    city = models.CharField(max_length=15)
    state = models.CharField(max_length=30)
    blood_group = models.CharField()
    gender = models.CharField()
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
class Profile_pictures(models.Model) :
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Request(models.Model):
    name = models.CharField(max_length=90)
    mobile = models.BigIntegerField()
    email = models.EmailField(max_length=100)
    city = models.CharField(max_length=15)
    state = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=5)
    urgency = models.CharField(max_length=100)
    donor = models.ForeignKey(Register, on_delete=models.SET_NULL, null=True, blank=True)
    

    def __str__(self):
        return f"{self.name} ({self.blood_group})"

class Blood_Donor(models.Model):
    donor_name=models.CharField(max_length=50)
    mobile = models.BigIntegerField()
    age=models.IntegerField()
    gender = models.CharField(max_length=20)
    blood_group=models.CharField(max_length=10)
    email=models.EmailField(max_length=50)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    image=models.ImageField(upload_to='donor_images/')

    def __str__(self):
        return self.donor_name


class Donate_Us(models.Model):
    user=models.ForeignKey(Register,on_delete=models.CASCADE)
    amount=models.DecimalField(default=0, decimal_places=2, max_digits=10)
    payment_id=models.CharField()

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name