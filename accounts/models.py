from django.db import models

# Create your models here.


# we'll create a class (a similar table will be created in database). The objects of the class will be stored as rows in the database.

class Customer (models.Model):
    name = models.CharField (max_length=200, null=True)         # CharFied == string; can set null value to the field
    phone = models.CharField (max_length=200, null=True)
    email = models.CharField (max_length=200, null=True)        # OR USE EmailField
    date_created = models.DateTimeField (auto_now_add=True, null=True)         # automatically captures the system date and time at the time of object creation


    # __str__(object) method in python is the toString() method in java
    def __str__ (self):
        return self.name


'''------------------------------------------------------------------------------------------------------'''


class Tag (models.Model):
    name = models.CharField (max_length=200, null=True)         # CharFied == string; can set null value to the field
    
    # __str__(object) method in python is the toString() method in java
    def __str__ (self):
        return self.name

'''------------------------------------------------------------------------------------------------------'''


class Product (models.Model):
    CATEGORY = (
                    ('Indoor', 'Indoor'),
                    ('Out Door', 'Out Door')
               )

    name = models.CharField (max_length=200, null=True)
    price = models.FloatField (null=True)                           # or use DecimalField
    category = models.CharField (max_length=200, null=True, choices=CATEGORY)
    description = models.CharField (max_length=200, null=True, blank=True)
    date_created = models.DateTimeField (auto_now_add=True, null=True)
    tags = models.ManyToManyField (Tag)

    def __str__ (self):
        return self.name


'''------------------------------------------------------------------------------------------------------'''


class Order (models.Model):
    STATUS = (
                ('Pending', 'Pending'),
                ('Out for delivery', 'Out for delivery'),
                ('Delivered', 'Delivered') 
             )
    customer = models.ForeignKey (Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey (Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField (auto_now_add=True, null=True)
    status = models.CharField (max_length=200, null=True, choices=STATUS)          # choice to create a dropdown menu

    def __str__ (self):
        return self.product.name + " : " + self.customer.name