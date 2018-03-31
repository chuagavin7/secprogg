from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(null=False, unique=True, max_length=255)
    password = models.CharField(null=False, max_length=255)
    contact_num = models.CharField(null=True, max_length=20)
    billingAdd = models.CharField(null=True, max_length=1024)
    shippingAdd = models.CharField(null=True, max_length=1024)
    name = models.CharField(null=False, max_length=1024)
    date_joined = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        return self.name

    def is_staff(self):
        try:
            Staff.objects.get(user=self.id)
            return True
        except Staff.DoesNotExist:
            pass
        return False

    def get_type(self):
        try:
            return Staff.objects.get(user=self.id).type
        except Staff.DoesNotExist:
            pass
        return 3

    def string_type(self):
        if self.is_staff():
            return Staff.choices[self.get_type()][1]
        else:
            return "Customer"


class Staff(models.Model):
    choices = ((0, 'Admin'), (1, 'Product Manager'), (2, 'Accounts Manager'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    type = models.IntegerField(default=0, choices=choices)

    def __str__(self):
        return self.choices[self.type][1]
