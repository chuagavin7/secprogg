from django.db import models

# Create your models here.
from User.models import User


class Product(models.Model):
    choices = ((0, 'Analog Watch'), (1, 'Digital Watch'), (2, 'Smart Watch'))

    name = models.CharField(max_length=250)
    description = models.CharField(max_length=500)
    quantity = models.PositiveIntegerField(default=0)
    price = models.FloatField(default=0)
    type = models.IntegerField(default=0, choices=choices)
    picture = models.ImageField(upload_to='item/%Y/%m/%d/', default='item/default_item.jpg')

    def __str__(self):
        return self.name

    def is_buyer(self, user):
        try:
            Transaction.objects.get(user=user, product=self.id)
            return True
        except Transaction.DoesNotExist:
            pass
        return False

    def has_review(self):
        try:
            Review.objects.get(product=self.id)
            return True
        except Review.DoesNotExist:
            pass
        return False

    def string_type(self):
        return self.choices[self.type][1]


class Review(models.Model):
    title = models.CharField(max_length=250)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.CharField(max_length=1000)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=0)
    credit_card = models.CharField(null=False, max_length=100)