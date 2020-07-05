from django.db import models

# store customerID
class Customer(models.Model):
    username = models.CharField(max_length=30) 
    #add strict rules for username here
    stripe_customerID = models.CharField(max_length=25)
    password = models.CharField(max_length=50)
    #add strict rules for username here
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.name


