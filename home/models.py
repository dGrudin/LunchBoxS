from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# тип пользователя, определяющий уровень доступности
# 0 - клиент
# 1 - сотрудник
# 2 - администратор
class Type(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Type.objects.create(user=instance)


class LunchBox(models.Model):
    title = models.CharField(max_length=255, unique=True)
    img = models.ImageField(upload_to="images/")
    description = models.CharField(max_length=1000)
    price = models.IntegerField()
    addition = models.CharField(max_length=50)


# Количество ланчбоксов, 0 по умолчанию
class NumberOfLunchBox(models.Model):
    lunchbox = models.OneToOneField(LunchBox, on_delete=models.CASCADE)
    number = models.IntegerField(default=0)

    @receiver(post_save, sender=LunchBox)
    def create_lunch_box(sender, instance, created, **kwargs):
        if created:
            NumberOfLunchBox.objects.create(lunchbox=instance)


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lunchbox = models.OneToOneField(LunchBox, on_delete=models.CASCADE)
    number = models.IntegerField(default=0)
    price = models.IntegerField(default=0)


class Order(models.Model):
    id = models.AutoField(primary_key = True)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField(default=0)


class OrderComposition(models.Model):
    order = models.ForeignKey(Order, related_name='order_compositions', on_delete=models.CASCADE)
    lunchbox = models.ForeignKey(LunchBox, related_name='lunchbox_info', on_delete=models.CASCADE)
    number = models.IntegerField()


class PastOrder(models.Model):
    id = models.AutoField(primary_key = True)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    price = models.IntegerField(default=0)
    employee = models.CharField(max_length=50, default="")


class PastOrderComposition(models.Model):
    order = models.ForeignKey(PastOrder, related_name='pastorder_compositions', on_delete=models.CASCADE)
    lunchbox = models.ForeignKey(LunchBox, related_name='pastlunchbox_info', on_delete=models.CASCADE)
    number = models.IntegerField()


class Status(models.Model):
    name = models.CharField(max_length=30)
    st = models.BooleanField(default=False)
