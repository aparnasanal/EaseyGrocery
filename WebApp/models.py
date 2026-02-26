from django.db import models

# Create your models here.

class ContactDb(models.Model):
    Name = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    Message = models.TextField()

class SignupDb(models.Model):
    Username = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    Password = models.CharField(max_length=100)
    C_Password = models.CharField(max_length=100)

class CartDb(models.Model):
    Username = models.CharField(max_length=100)
    Product_Name = models.CharField(max_length=100)
    Price = models.FloatField()
    Quantity = models.IntegerField()
    Total_Price = models.FloatField()
    Product_Image = models.ImageField(upload_to="Cart Images", null=True, blank=True)
