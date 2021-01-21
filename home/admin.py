from django.contrib import admin
from .models import Type, LunchBox, Order, NumberOfLunchBox, Basket, OrderComposition, PastOrderComposition, PastOrder, Status

admin.site.register(Type)
admin.site.register(LunchBox)
admin.site.register(Order)
admin.site.register(NumberOfLunchBox)
admin.site.register(OrderComposition)
admin.site.register(Basket)
admin.site.register(PastOrderComposition)
admin.site.register(PastOrder)
admin.site.register(Status)